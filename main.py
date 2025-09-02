"""
Tradutor de DNA em aminoácidos usando Gramatica Livre de Contexto
definida como: G = (V, Σ, R, S), onde:
V = {A, C, G, T, U}
Σ = {A, C, G, T, U}
R = {A -> U, C -> G, G -> C, T -> A}
S = {A, C, G, T, U}
A gramática está errada, pois o símbolo inicial S preisa ser único e não pode ser igual ao conjunto de variáveis V.
Além disso, usar gramático não serviria, seria um autômato de pilha.
"""

"""
Autômato de Pilha (AP) para tradução de DNA em aminoácidos
M = (Q, Σ, Γ, δ, q0, Z0, F), onde:
Q = {q0, q1, q2} (conjunto de estados)
E = {A, C, G, T, U} (alfabeto de entrada)
Γ = {A, C, G, T, U, Z0} (alfabeto da pilha)
δ = função de transição (definida nas funções do código)
q0 = estado inicial
Z0 = símbolo inicial da pilha
F = {q2} (conjunto de estados de aceitação)
"""