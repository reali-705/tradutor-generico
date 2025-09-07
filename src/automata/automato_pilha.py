from typing import Iterable

class Pushdown:
    """
    Implementa uma estrutura de dados de Pilha (Stack) LIFO (Last-In, First-Out).
    
    Esta classe auxiliar é usada como a memória principal do autômato de pilha.
    """
    def __init__(self, iteravel: Iterable = []):
        """Inicializa a pilha, opcionalmente com elementos de um iterável."""
        self.__pilha: list[str] = list(iteravel)
        self.__length = len(self.__pilha)

    def push(self, character: str):
        """Adiciona um elemento no topo da pilha."""
        self.__pilha.insert(0, character)
        self.__length += 1
    
    def top(self) -> str:
        """
        Remove e retorna o elemento do topo da pilha (comportamento de 'pop').
        
        Raises:
            Exception: Se a pilha estiver vazia.
        """
        if self.isEmpty():
            raise Exception("Pilha vazia")
        self.__length -= 1
        return self.__pilha.pop(0)
    
    def clear(self):
        """Remove todos os elementos da pilha."""
        while self.__length != 0:
            self.top()
    
    def isEmpty(self) -> bool:
        """Verifica se a pilha está vazia."""
        return self.__length == 0
    
    def tam(self) -> int:
        """Retorna o número de elementos na pilha."""
        return self.__length
    
    def __iter__(self):
        """Permite a iteração sobre os elementos da pilha, do topo para a base."""
        for char in self.__pilha:
            yield char

class Automato_Pilha_Deterministico_ε:
    """
    Implementa um Autômato de Pilha Determinístico com transições em vazio (DPDA-ε).

    Um DPDA-ε é uma 7-tupla (Q, Σ, Γ, δ, q0, Z0, F) que reconhece linguagens
    livres de contexto determinísticas.
    """
    def __init__(self,
        Q: set[str],                                            # conjunto de estados
        Σ: set[str],                                            # alfabeto de entrada
        Γ: set[str],                                            # alfabeto da pilha
        δ: dict[tuple[str, str, str], tuple[str, list[str]]],   # função de transição
        q0: str,                                                # estado inicial
        Z0: str,                                                # símbolo inicial da pilha
        F: set[str]                                             # estados finais
    ):
        """
        Inicializa e valida a definição formal do autômato de pilha.

        Args:
            Q: Conjunto de estados.
            Σ: Alfabeto de entrada.
            Γ: Alfabeto da pilha.
            δ: Função de transição mapeando (estado, símbolo_entrada, topo_pilha) -> (novo_estado, [simbolos_a_empilhar]).
               Para transições em vazio, o símbolo_entrada deve ser "".
            q0: Estado inicial.
            Z0: Símbolo inicial da pilha.
            F: Conjunto de estados de aceitação.
        
        Raises:
            TypeError: Se a definição do autômato for inconsistente.
        """
        # --- Atribuição dos Componentes ---
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
        """(Privado) Reseta o autômato para sua configuração inicial."""
        self.__pilha.clear()
        self.__pilha.push(self.__simbolo_inicial_pilha)
        
    def cadeia_saida(self) -> str:
        """
        Retorna o conteúdo final da pilha como uma string.
        
        No contexto do ribossomo, isso representa a sequência de proteínas traduzidas.
        """
        return "".join(self.__pilha)
    
    def validar(self, cadeia: str) -> bool:
        """
        Processa uma cadeia de entrada para determinar se ela é aceita pelo autômato.

        Args:
            cadeia (str): A cadeia de entrada a ser validada.

        Returns:
            bool: True se a cadeia for aceita, False caso contrário.
        """
        self.__inicializar()
        estado_atual = self.__estado_inicial
        n = 0
        
        # Loop principal: consome a cadeia de entrada
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
                
        # A cadeia é aceita se, e somente se, o estado final for um estado de aceitação.
        return estado_atual in self.__estados_finais
