'''
Criar uma gramática livre de contexto não é fácil, nem útil, pois podemos fazer tudo por autômato de pilha.
A gramática será na parte teórica.
class TradutorDNA:
    def __init__(self):
        self.V = {'A', 'C', 'G', 'T', 'U'}
        self.Σ = {'A', 'C', 'G', 'T', 'U'}
        self.R = {'A': 'U', 'C': 'G', 'G': 'C', 'T': 'A'}
        self.S = {'A', 'C', 'G', 'T', 'U'}

    def traduzir(self, dna):
        return ''.join([self.R.get(base, base) for base in dna])
'''

# Classe genérica de Pilha
class Pilha:
    def __init__(self, iteravel: list = []):
        self.__itens__ : list[str] = list(reversed(iteravel))
        self.length = len(self.__itens__)
        
    def empilhar(self, item: str):
        self.__itens__.insert(0, item)
        self.length += 1
        return self
        
    def desempilhar(self):
        if not self.esta_vazia():
            self.length -= 1
            return self.__itens__.pop(0)
        return ""
    
    def esta_vazia(self):
        return self.length == 0



#Classe do Autômato de Pilha
class Automato_Pilha:
    def __init__(self, Q: set[str], Σ: set[str], Γ: set[str], δ: dict[tuple[str, str, str], tuple[str, str]], q0: str, Z0:  str, F: set[str]):
        self.pilha = Pilha([Z0])
        self.estados = Q
        self.Z0 = Z0
        self.alfabeto_entrada = Σ
        self.transicoes = δ
        self.alfabeto_pilha = Γ
        self.estado_atual = q0
        self.estados_finais = F
    
    def cadeia_saida(self):
        return ''.join(map(str,self.pilha.__itens__))
    
    def processar_entrada(self, entrada: str):
        self.pilha = Pilha([self.Z0])
        for simbolo in entrada:
            if simbolo not in self.alfabeto_entrada or self.pilha.esta_vazia():
                return False
            tupla = (self.estado_atual, simbolo, str(self.pilha.desempilhar()[0]))
            nova_tupla = self.transicoes.get(tupla, None)
            if nova_tupla is None:
                return False
            self.estado_atual = nova_tupla[0]
            for character in nova_tupla[1][::-1]:
                self.pilha.empilhar(character)
        return self.estado_atual in self.estados_finais or self.pilha.esta_vazia()
            
            