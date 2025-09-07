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


def criar_ribossomo() -> Automato_Pilha_Deterministico_ε:

    
    Q = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18", "q19", "q20"}
    Σ = {"U", "A", "G", "C"}
    Γ = {"Z0", " ", "-", "teM", "ehP", "ueL", "elI", "laV", "reS", "orP", "rhT", "alA", "ryT", "siH", "nlG", "nsA", "syL", "psA", "ulG", "syC", "prT", "grA", "ylG"}
    δ = {
        ("q0", "U", "Z0") : ("q0", ["Z0"]), ("q0", "G", "Z0") : ("q0", ["Z0"]), ("q0", "C", "Z0") : ("q0", ["Z0"]), ("q0", "A", "Z0") : ("q1", ["Z0"]),
        ("q1", "A", "Z0") : ("q0", ["Z0"]), ("q1", "G", "Z0") : ("q0", ["Z0"]), ("q1", "C", "Z0") : ("q0", ["Z0"]), ("q1", "U", "Z0") : ("q2", ["Z0"]),
        ("q2", "A", "Z0") : ("q0", ["Z0"]), ("q2", "U", "Z0") : ("q0", ["Z0"]), ("q2", "C", "Z0") : ("q0", ["Z0"]), ("q2", "G", "Z0") : ("q3", ["teM", "-"]),
        ("q3", "C", "-") : ("q4", ["-"]), ("q4", "U", "-") : ("q5", ["-", "ueL", "-"]), ("q5", "A", "-") : ("q3", ["-"]), ("q5", "U", "-") : ("q3", ["-"]),
        ("q5", "C", "-") : ("q3", ["-"]), ("q5", "G", "-") : ("q3", ["-"]), ("q4", "C", "-") : ("q5", ["-", "orP", "-"]), ("q4", "G", "-") : ("q5", ["-", "grA", "-"]),
        ("q4", "A", "-") : ("q6", ["-"]), ("q6", "U", "-") : ("q3", ["-", "siH", "-"]), ("q6", "C", "-") : ("q3", ["-", "siH", "-"]), ("q6", "A", "-") : ("q3", ["-", "nlG", "-"]),
        ("q6", "G", "-") : ("q3", ["-", "nlG", "-"]), ("q3", "G", "-") : ("q7", ["-"]), ("q7", "U", "-") : ("q5", ["-", "laV", "-"]), ("q7", "C", "-") : ("q5", ["-", "alA", "-"]),
        ("q7", "G", "-") : ("q5", ["-", "ylG", "-"]), ("q7", "A", "-") : ("q8", ["-"]), ("q8", "U", "-") : ("q3", ["-", "psA", "-"]), ("q8", "C", "-") : ("q3", ["-", "psA", "-"]),
        ("q8", "A", "-") : ("q3", ["-", "ulG", "-"]), ("q8", "G", "-") : ("q3", ["-", "ulG", "-"]), ("q3", "A", "-") : ("q9", ["-"]), ("q9", "C", "-") : ("q5", ["-", "rhT", "-"]),
        ("q9", "G", "-") : ("q10", ["-", "rhT", "-"]), ("q10", "U", "-") : ("q3", ["-", "reS", "-"]), ("q10", "C", "-") : ("q3", ["-", "reS", "-"]), ("q10", "A", "-") : ("q3", ["-", "grA", "-"]),
        ("q10", "G", "-") : ("q3", ["-", "grA", "-"]), ("q9", "A", "-") : ("q11", ["-"]), ("q11", "U", "-") : ("q3", ["-", "nsA", "-"]), ("q11", "C", "-") : ("q3", ["-", "nsA", "-"]),
        ("q11", "A", "-") : ("q3", ["-", "syL", "-"]), ("q11", "G", "-") : ("q3", ["-", "syL", "-"]), ("q9", "U", "-") : ["q12", ["-"]], ("q12", "G", "-") : ("q3", ["-", "teM", "-"]),
        ("q12", "C", "-") : ("q3", ["-", "elI", "-"]), ("q12", "A", "-") : ("q3", ["-", "elI", "-"]), ("q12", "U", "-") : ("q3", ["-", "elI", "-"]), ("q3", "U", "-") : ("q13", ["-"]),
        ("q13", "C", "-") : ("q5", ["-", "reS", "-"]), ("q13", "U", "-") : ("q14", ["-"]), ("q14", "U", "-") : ("q3", ["-", "ehP", "-"]), ("q14", "C", "-") : ("q3", ["-", "ehP", "-"]),
        ("q14", "A", "-") : ("q3", ["-", "ueL", "-"]), ("q14", "G", "-") : ("q3", ["-", "ueL", "-"]), ("q13", "A", "-") : ("q15", ["-"]), ("q15", "U", "-") : ("q3", ["-", "ryT", "-"]),
        ("q15", "C", "-") : ("q3", ["-", "ryT", "-"]), ("q15", "A", "-") : ("q17", [" "]), ("q15", "G", "-") : ("q17", [" "]), ("q13", "G", "-") : ("q16", ["-"]),
        ("q16", "U", "-") : ("q3", ["-", "syC", "-"]), ("q16", "C", "-") : ("q3", ["-", "syC", "-"]), ("q16", "G", "-") : ("q3", ["-", "prT", "-"]), ("q16", "A", "-") : ("q17", [" "]),
        ("q17", "U", " ") : ("q17", [" "]), ("q17", "G", " ") : ("q17", [" "]), ("q17", "C", " ") : ("q17", [" "]), ("q17", "A", " ") : ("q18", [" "]),
        ("q18", "A", " ") : ("q17", [" "]), ("q18", "G", " ") : ("q17", [" "]), ("q18", "C", " ") : ("q17", [" "]), ("q18", "U", " ") : ("q19", [" "]),
        ("q19", "A", " ") : ("q17", [" "]), ("q19", "U", " ") : ("q17", [" "]), ("q19", "C", " ") : ("q17", [" "]), ("q19", "G", " ") : ("q3", [" ", "teM", "-"]),
        ("q17", "", " ") : ("q20", []), ("q18", "", " ") : ("q20", []), ("q19", "", " ") : ("q20", []),
    }
    q0 = "q0"
    Z0 = "Z0"
    F = {"q20"}
    
    return Automato_Pilha_Deterministico_ε(Q, Σ, Γ, δ, q0, Z0, F)
