"""
Código do autômato de pilha (AP) para tradução de DNA em aminoácidos
M = (Q, Σ, Γ, δ, q0, Z, F), onde:
Q = {q0, q1, q2} (conjunto de estados)
Σ = {A, C, G, T, U} (alfabeto de entrada)
Γ = {A, C, G, T, U, Z} (alfabeto da pilha)
δ = função de transição (definida nas funções do código)    
q0 = estado inicial
Z0 = símbolo inicial da pilha
F = {q2} (conjunto de estados de aceitação)
"""

from classe import Automato_Pilha

# Falta ainda definir as transições do autômato de pilha, além dos estados
# Farei isso mais tarde
transcritor = Automato_Pilha(
    Q = {'q0'},
    Σ = {'A', 'C', 'G', 'T'},
    Γ = {'A', 'C', 'G', 'U', 'Z'},
    δ = {
        ('q0', 'A', 'Z') : ('q0', 'U'), ('q0', 'C', 'Z') : ('q0', 'G'), ('q0', 'G', 'Z') : ('q0', 'C'), ('q0', 'T', 'Z') : ('q0', 'A'), 
        ('q0', 'A', 'A') : ('q0', 'UA'), ('q0', 'C', 'A') : ('q0', 'GA'), ('q0', 'G', 'A') : ('q0', 'CA'), ('q0', 'T', 'A') : ('q0', 'AA'), 
        ('q0', 'A', 'C') : ('q0', 'UC'), ('q0', 'C', 'C') : ('q0', 'GC'), ('q0', 'G', 'C') : ('q0', 'CC'), ('q0', 'T', 'C') : ('q0', 'AC'), 
        ('q0', 'A', 'G') : ('q0', 'UG'), ('q0', 'C', 'G') : ('q0', 'GG'), ('q0', 'G', 'G') : ('q0', 'CG'), ('q0', 'T', 'G') : ('q0', 'AG'), 
        ('q0', 'A', 'U') : ('q0', 'UU'), ('q0', 'C', 'U') : ('q0', 'GU'), ('q0', 'G', 'U') : ('q0', 'CU'), ('q0', 'T', 'U') : ('q0', 'AU'), 
        },
    q0 = 'q0',
    Z0 = 'Z',
    F = {'q0'}
)

