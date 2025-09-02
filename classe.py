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
class Pilha[ty]:
    def __init__(self, iteravel: list[ty] = []):
        self.__itens__ = list(reversed(iteravel))
        self.length = 0
        
    def empilhar(self, item):
        self.__itens__.append(item)
        self.length += 1
        return self
        
    def desempilhar(self):
        if not self.esta_vazia():
            self.length -= 1
            return self.__itens__.pop()
        return None
    
    def esta_vazia(self):
        return self.length == 0
    
    def cadeia_saida(self):
        return ''.join(map(str,self.__itens__))

#Classe do Autômato de Pilha
class Automato_Pilha:
    def __init__(self, Q: set[str], Σ: set[str], Γ: set[str], δ: dict[tuple[str, str, str], tuple[str, str]], q0: str, Z0:  str, F: set[str]):
        self.pilha = Pilha[str]([Z0])
        self.estados = Q
        self.alfabeto_entrada = Σ
        self.transicoes = δ
        self.alfabeto_pilha = Γ
        self.estado_atual = q0
        self.estados_finais = F
        
    def processar_entrada(self, entrada: str):
        for simbolo in entrada:
            if simbolo not in self.alfabeto_entrada or self.pilha.esta_vazia():
                return False
            tupla = (self.estado_atual, simbolo, str(self.pilha.desempilhar()))
            nova_tupla = self.transicoes.get(tupla, None)
            if nova_tupla is None:
                return False
            self.estado_atual = nova_tupla[0]
            self.pilha.empilhar(nova_tupla[1])
        
        return self.estado_atual in self.estados_finais or self.pilha.esta_vazia()
            
            