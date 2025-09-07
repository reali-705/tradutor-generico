"""
Módulo principal do pacote 'src'.

Este arquivo __init__.py serve como o ponto de entrada para o pacote,
disponibilizando as principais funções e classes para serem importadas
em outras partes do projeto.
"""

from .automata import TransdutorFinito, Automato_Pilha_Deterministico_ε
from .utils import gerar_dna_aleatorio, gerar_dna_pseudoaleatorio, ler_arquivo, escrever_arquivo
from .tabela_codons import TABELA_CODONS

def criar_transcritor_dna_rna() -> TransdutorFinito:
    """
    Cria e retorna uma instância configurada do TransdutorFinito (Máquina de Mealy)
    para realizar a transcrição de uma fita de DNA para uma fita de RNA.

    A transcrição segue a regra de complementaridade:
    - A (DNA) -> U (RNA)
    - T (DNA) -> A (RNA)
    - C (DNA) -> G (RNA)
    - G (DNA) -> C (RNA)

    Returns:
        TransdutorFinito: Uma instância da máquina de Mealy pronta para uso.
    """
    # Definição dos componentes da Máquina de Mealy
    Q = {'q0'}                      # Conjunto de estados (apenas um estado é necessário)
    Σ = {'A', 'C', 'G', 'T'}        # Alfabeto de entrada (bases do DNA)
    Γ = {'A', 'C', 'G', 'U'}        # Alfabeto de saída (bases do RNA)
    
    # Função de transição (δ): sempre permanece no mesmo estado
    δ = {
        ('q0', 'A'): 'q0',
        ('q0', 'C'): 'q0',
        ('q0', 'G'): 'q0',
        ('q0', 'T'): 'q0'
    }
    
    # Função de saída (λ): mapeia a base do DNA para a base complementar do RNA
    λ = {
        ('q0', 'A'): 'U',
        ('q0', 'C'): 'G',
        ('q0', 'G'): 'C',
        ('q0', 'T'): 'A'
    }
    
    q0 = 'q0'                       # Estado inicial

    # Retorna a instância do transdutor configurada
    return TransdutorFinito(Q, Σ, Γ, δ, λ, q0)


def criar_sinteze_proteica() -> Automato_Pilha_Deterministico_ε:
    """
     Q: set[str],                                       # conjunto de estados
        Σ: set[str],                                       # alfabeto de entrada
        Γ: set[str],                                       # alfabeto da pilha
        δ: dict[tuple[str, str | None, str], tuple[str, list[str]]],    # função de transição
        q0: str,                                           # estado inicial
        Z0: str,                                           # símbolo inicial da pilha
        F: set[str]): 
    """
    
    Q = {"q0", "q1", "q2", "q3"}
    Σ = {"U", "A", "G", "C"}
    Γ = set(set(TABELA_CODONS.values()).union({"Z0", " ", "-"}))
    δ = {
        ("q0", "U", "Z0") : ("q0", ["Z0"]), ("q0", "G", "Z0") : ("q0", ["Z0"]), ("q0", "C", "Z0") : ("q0", ["Z0"]), ("q0", "A", "Z0") : ("q1", ["Z0"]),
        ("q1", "A", "Z0") : ("q0", ["Z0"]), ("q1", "G", "Z0") : ("q0", ["Z0"]), ("q1", "C", "Z0") : ("q0", ["Z0"]), ("q1", "U", "Z0") : ("q2", ["Z0"]),
        ("q2", "A", "Z0") : ("q0", ["Z0"]), ("q2", "U", "Z0") : ("q0", ["Z0"]), ("q2", "C", "Z0") : ("q0", ["Z0"]), ("q2", "G", "Z0") : ("q3", ["met", "-"]),
        ("q3", "")
    }
    q0 = "q0"
    Z0 = "Z0"
    F = {"q0"}
    
    return Automato_Pilha_Deterministico_ε(Q, Σ, Γ, δ, q0, Z0, F)


    