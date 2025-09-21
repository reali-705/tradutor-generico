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
    δ = {('q0', 'A'): 'q0', ('q0', 'C'): 'q0', ('q0', 'G'): 'q0', ('q0', 'T'): 'q0'}
    
    # Função de saída (λ): mapeia a base do DNA para a base complementar do RNA
    λ = {('q0', 'A'): 'U', ('q0', 'C'): 'G', ('q0', 'G'): 'C', ('q0', 'T'): 'A'}
    
    q0 = 'q0'                       # Estado inicial

    # Retorna a instância do transdutor configurada
    return TransdutorFinito(Q, Σ, Γ, δ, λ, q0)


def criar_ribossomo() -> Automato_Pilha:
    aminoacidos = set(TABELA_CODONS.values())
    Q = {'q_inicial', 'q_achouA', 'q_achouAU', 'q_traduz', 'q_baseXA', 'q_baseXU', 'q_baseXC', 'q_baseXG', 'q_rollback', 'q_final'}
    Σ = {'A', 'C', 'G', 'U', None}
    q0 = 'q_inicial'
    Z0 = 'Z0'
    F = {'q_final'}
    Γ = aminoacidos.union(Σ).union({Z0}).union({None})
    δ = {}

    # fase de busca pelo códon de início (AUG)
    estados_busca = {'q_inicial', 'q_achouA', 'q_achouAU'}
    for base in Σ:
        for estado in estados_busca:
            # filtro para que toda leitura que não seja A na fase de busca volte para o estado inicial
            if base != 'A':
                δ[(estado, base, Z0)] = ('q_inicial', [Z0])
            # filtro caso a leitura seja A, segue para o estado q_achouA
            else:
                δ[(estado, base, Z0)] = ('q_achouA', [Z0])
            # transições específicas para parte do códon de início (AUG)
            if estado == 'q_achouA' and base == 'U':
                δ[(estado, base, Z0)] = ('q_achouAU', [Z0])
            # transição final do códon de início (AUG)
            if estado == 'q_achouAU' and base == 'G':
                δ[(estado, base, Z0)] = ('q_traduz', ['Met', Z0])
    
    # fase de tradução dos códons
    bases = {'A', 'U', 'C', 'G'}
    for base1 in bases:
        # transição referente à leitura da primeira base do códon
        δ[('q_traduz', base1, Z0)] = ('q_traduz', [base1])
        for base2 in bases:
            # transição referente à leitura da segunda base do códon
            δ[('q_traduz', base2, base1)] = (f'q_baseX{base2}', [base1])
            for base3 in bases:
                # transição referente à leitura da terceira base do códon
                aminoacido = TABELA_CODONS[f'{base1}{base2}{base3}']
                # se for um códon de parada, volta para o estado inicial
                if aminoacido == 'Stop':
                    δ[(f'q_baseX{base2}', base3, base1)] = ('q_inicial', ['Stop', Z0])
                # se for um aminoácido, empilha o aminoácido e Z0
                else:
                    δ[(f'q_baseX{base2}', base3, base1)] = ('q_traduz', [aminoacido, Z0])
    
    # fase de rollback (desempilha os aminoacidos que não formaram uma proteina completa)
    δ[('q_traduz', None, Z0)] = ('q_rollback', []) # base0, vai direto pro rollback
    for base in bases:
        δ[('q_traduz', None, base)] = ('q_rollback', []) # base1, apaga a base1 e vai pro rollback
        for base_estado in bases:
            δ[(f'q_baseX{base_estado}', None, base)] = ('q_rollback', []) # baseX, apaga a base1 e a baseX depois vai pro rollback

    for aminoacido in aminoacidos:
        if aminoacido == 'Stop':
            δ[('q_rollback', None, aminoacido)] = ('q_rollback', [Z0]) # desempilha o Stop e empilha Z0
        else:
            δ[('q_rollback', None, aminoacido)] = ('q_rollback', []) # desempilha o aminoacido e continua no rollback

    # fase de finalização (aceitação)
    δ[('q_rollback', None, Z0)] = ('q_final', []) # desempilha o Z0 e vai para o estado final
    δ[('q_rollback', None, None)] = ('q_final', []) # aceita se a pilha estiver vazia
    for estado in estados_busca:
        δ[(estado, None, Z0)] = ('q_final', []) # aceita se estiver na fase de busca e a pilha só tiver Z0


    return Automato_Pilha(Q, Σ, Γ, δ, q0, Z0, F)
