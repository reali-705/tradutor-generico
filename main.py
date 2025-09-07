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
'''
from transcritor import transcritor
from src.funcoes import reversed_str

# Pegar cadeias de DNA
with open("cadeia_DNA.txt", "r") as file:
    cadeias = list(map(str.strip,file.readlines()))

# Limpar arquivo
with open("cadeia_RNA.txt", "w") as f:
    f.write("")

with open("cadeia_RNA.txt", "a") as arquivo:
    for item in cadeias:
        if transcritor.processar_entrada(item):
            arquivo.write(reversed_str(transcritor.cadeia_saida()) + "\n")
        else:
            arquivo.write("\n")
'''

'''
TODO
## Input e Output
    - Arquivo que lê inputs e escreve arquivos output
## transdutor finito
    - Um autômato para validar a cadeia de DNA e transforma a cadeia de RNA
## Autômato de pilha
    - Um autômato para validar a cadeia de RNA e transformar em proteínas

# Definição para cargos
## Reali
- [] Input e Output
- [] transdutor finito

## Gian
- [] autômato de pilha
'''
