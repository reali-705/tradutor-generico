from typing import Iterable

class Pushdown:
    #A classe push down é uma classe de pilha especificamente para strings
    def __init__(self, iteravel : Iterable = []):
        self.__pilha: list[str] = list(iteravel)
        self.__length = 0

    def push(self, character: str):
        self.__pilha.insert(0, character)
        self.__length += 1
    
    def top(self) -> str :
        if (self.isEmpty()):
            raise Exception("Pilha vazia")
        self.__length -= 1
        return self.__pilha.pop(0)
    
    def clear(self):
        while self.__length != 0:
            self.top()
    
    def isEmpty(self) -> bool :
        return self.__length == 0
    
    def tam(self):
        return self.__length
    
    def __iter__(self):
        for char in self.__pilha:
            yield char

#Autômato de pilha determinístico com transição em vazio
class Automato_Pilha_Deterministico_ε :
    def __init__(self,
        Q: set[str],                                       # conjunto de estados
        Σ: set[str],                                       # alfabeto de entrada
        Γ: set[str],                                       # alfabeto da pilha
        δ: dict[tuple[str, str, str], tuple[str, list[str]]],    # função de transição
        q0: str,                                           # estado inicial
        Z0: str,                                           # símbolo inicial da pilha
        F: set[str]):                                      # estados finais
#------------------------------------------------------------------------------------#
            self.__pilha = Pushdown()
            self.__estados = Q
            self.__simbolo_inicial_pilha = Z0
            self.__alfabeto_entrada = Σ
            self.__transicoes = δ
            self.__alfabeto_pilha = Γ
            self.__estado_inicial = q0
            self.__estados_finais = F
            
            if self.__estado_inicial not in self.__estados:
                raise TypeError("Estado inicial não pertence ao conjunto dos estados")
            
            if not self.__estados_finais.issubset(self.__estados):
                raise TypeError("Conjunto dos estados finais não é subconjunto dos estados")
            
            if (self.__simbolo_inicial_pilha not in self.__alfabeto_pilha):
                raise TypeError("Símbolo inicial da pilha não pertence ao alfabeto da pilha")
            
            
            for trinca in self.__transicoes.keys():
                if trinca[0] not in self.__estados:
                    error = f"A transição {trinca} -> {self.__transicoes[trinca]}. {trinca[0]} não pertence ao conjunto de estados"
                    raise TypeError(error)
                    
                if trinca[1] not in self.__alfabeto_entrada and trinca[1] != "":
                    erro = f"A transição {trinca} -> {self.__transicoes[trinca]}. {trinca[1]} não pertence ao alfabeto de entrada"
                    raise TypeError(erro)

                if trinca[2] not in self.__alfabeto_pilha:
                    erro = f"A transição {trinca} -> {self.__transicoes[trinca]}. {trinca[2]} não pertence ao alfabeto da pilha"
                    raise TypeError(erro)
     
    def __inicializar(self):
        self.__pilha.clear()
        self.__pilha.push(self.__simbolo_inicial_pilha)
        
    def cadeia_saida(self):
        return "".join(self.__pilha)
    
    def validar(self, cadeia : str) -> bool:
        self.__inicializar()
        estado_atual = self.__estado_inicial
        n = 0
        while n < len(cadeia):
            if self.__pilha.isEmpty():
                return False
            
            trinca = (estado_atual, cadeia[n], self.__pilha.top())
            dupla = self.__transicoes.get(trinca, None)
            
            if dupla == None:
                dupla = self.__transicoes.get((trinca[0], "", trinca[2]), None)
                if dupla == None:
                    return False
            else:
                n += 1
            
            estado_atual = dupla[0]
            for character in dupla[1]:
                self.__pilha.push(character)
             
        while not (estado_atual in self.__estados_finais or self.__pilha.isEmpty()):
            trinca = (estado_atual, "", self.__pilha.top())
            dupla = self.__transicoes.get(trinca, None)
            if dupla == None:
                return False
            estado_atual = dupla[0]
            for character in dupla[1]:
                self.__pilha.push(character)
        return True
