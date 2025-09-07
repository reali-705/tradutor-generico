"""
Módulo principal do pacote 'src'.

Este arquivo __init__.py serve como o ponto de entrada para o pacote,
disponibilizando as principais funções e classes para serem importadas
em outras partes do projeto.
"""

from .automata import TransdutorFinito, Automato_Pilha
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
