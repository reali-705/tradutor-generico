"""
Código do autômato de pilha (AP) para tradução de DNA em aminoácidos
M = (Q, Σ, Γ, δ, q0, Z0, F), onde:
Q = {q0, q1, q2} (conjunto de estados)
Σ = {A, C, G, T, U} (alfabeto de entrada)
Γ = {A, C, G, T, U, Z0} (alfabeto da pilha)
δ = função de transição (definida nas funções do código)    
q0 = estado inicial
Z0 = símbolo inicial da pilha
F = {q2} (conjunto de estados de aceitação)
"""

from classe import Automato_Pilha

#Falta ainda definir as transições do autômato de pilha
#Farei isso mais tarde
transcritor = Automato_Pilha(
    Q=set(),
    Σ={'A', 'C', 'G', 'T', 'U'},
    Γ={'A', 'C', 'G', 'T', 'U', 'Z0'},
    δ={},
    q0='q0',
    Z0='Z0',
    F=set()
)