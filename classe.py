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
    #Inicia a pilha com uma possível lista inicial
    def __init__(self, iteravel: list = []):
        self.__itens__ : list[str] = list(reversed(iteravel))
        self.length = len(self.__itens__)
    
    #Função de emplhar itens
    #Ela funciona da forma como o autõmato pilha
    #Na transição (q0, ba, ZF) |- (q0, a, APF)
    #O autômato leu b e o consumiu
    #E também leu a pilha Z e o consumiu, deixando no lugar AP que juntou com F
    def empilhar(self, *item: str):
        self.__itens__ = list(item) + self.__itens__
        self.length += 1
        return self
    
    #Recupera o item mais e cima
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
        self.pilha = Pilha()
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
            tripla = (self.estado_atual, simbolo, str(self.pilha.desempilhar()))
            tupla = self.transicoes.get(tripla, None)
            if tupla is None:
                return False
            self.estado_atual = tupla[0]
            self.pilha.empilhar(*tupla[1])
        return self.estado_atual in self.estados_finais or self.pilha.esta_vazia()
            
            