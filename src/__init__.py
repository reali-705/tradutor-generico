"""
Módulo principal do pacote 'src'.

Este arquivo __init__.py serve como o ponto de entrada para o pacote,
disponibilizando as principais funções e classes para serem importadas
em outras partes do projeto.
"""

from .automata import TransdutorFinito, Automato_Pilha
from .utils import gerar_dna_aleatorio, gerar_dna_pseudoaleatorio, ler_arquivo, escrever_arquivo, formatar_proteina
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
    """
    Cria e retorna uma instância do Automato_Pilha configurado para simular
    um ribossomo, traduzindo uma fita de RNA em proteínas.

    O autômato implementa uma estratégia Z0-cêntrica, onde o símbolo 'Z0' é
    mantido no topo da pilha na maior parte do tempo para padronizar as transições.

    A lógica é dividida em 4 fases:
    1. Busca: Procura pelo códon de início 'AUG'.
    2. Tradução: Converte códons de 3 bases em aminoácidos.
    3. Rollback: Limpa a pilha em caso de um gene incompleto no final da cadeia.
    4. Finalização: Move o autômato para o estado de aceitação.

    Returns:
        Automato_Pilha: Uma instância do autômato pronta para uso.
    """
    aminoacidos = set(TABELA_CODONS.values())
    Q = {'q_inicial', 'q_achouA', 'q_achouAU', 'q_traduz', 'q_baseXA', 'q_baseXU', 'q_baseXC', 'q_baseXG', 'q_rollback', 'q_final'}
    Σ = {'A', 'C', 'G', 'U', None} # Alfabeto de entrada, incluindo ε (None)
    q0 = 'q_inicial'
    Z0 = 'Z0'
    F = {'q_final'}
    Γ = aminoacidos.union(Σ).union({Z0}).union({None}) # Alfabeto da pilha
    δ = {}

    # --- FASE 1: BUSCA PELO CÓDON DE INÍCIO (AUG) ---
    # Estas regras assumem que Z0 está no topo. Isso significa que o autômato
    # só encontrará o primeiro gene. Para múltiplos genes, seria necessário
    # generalizar para outros topos de pilha (ex: 'Stop').
    estados_busca = {'q_inicial', 'q_achouA', 'q_achouAU'}
    for base in Σ:
        for estado in estados_busca:
            # Regra geral: se não for 'A', volta para o início da busca.
            if base != 'A':
                δ[(estado, base, Z0)] = ('q_inicial', [Z0])
            # Se for 'A', avança para o estado 'q_achouA'.
            else:
                δ[(estado, base, Z0)] = ('q_achouA', [Z0])
            
            # Regra específica: se viu 'A' e agora vê 'U', avança para 'q_achouAU'.
            if estado == 'q_achouA' and base == 'U':
                δ[(estado, base, Z0)] = ('q_achouAU', [Z0])
            # Regra específica: se viu 'AU' e agora vê 'G', a busca teve sucesso.
            # Empilha 'Met' e 'Z0' para iniciar a tradução com Z0 no topo.
            if estado == 'q_achouAU' and base == 'G':
                δ[(estado, base, Z0)] = ('q_traduz', ['Met', Z0])
    
    # --- FASE 2: TRADUÇÃO DOS CÓDONS ---
    # Implementa a lógica de (pilha, estado, entrada) para ler 3 bases.
    bases = {'A', 'U', 'C', 'G'}
    for base1 in bases:
        # Lê a 1ª base: espera Z0 no topo, empilha a base lida.
        # A pilha fica [..., aminoacido_anterior, base1]
        δ[('q_traduz', base1, Z0)] = ('q_traduz', [base1])
        for base2 in bases:
            # Lê a 2ª base: o topo é a base1. Muda de estado para "lembrar" a base2.
            # A pilha não muda. O estado agora é 'q_baseX' + base2.
            δ[('q_traduz', base2, base1)] = (f'q_baseX{base2}', [base1])
            for base3 in bases:
                # Lê a 3ª base: combina (topo=base1, estado=base2, entrada=base3) para formar o códon.
                aminoacido = TABELA_CODONS[f'{base1}{base2}{base3}']
                # Se for um códon de parada, empilha 'Stop' e 'Z0', e volta a buscar.
                if aminoacido == 'Stop':
                    δ[(f'q_baseX{base2}', base3, base1)] = ('q_inicial', ['Stop', Z0])
                # Senão, empilha o aminoácido e 'Z0', e volta a traduzir.
                else:
                    δ[(f'q_baseX{base2}', base3, base1)] = ('q_traduz', [aminoacido, Z0])
    
    # --- FASE 3: ROLLBACK (LIMPEZA DE GENE INCOMPLETO) ---
    # Acionado por uma transição ε (None) se a cadeia acabar no meio da tradução.
    δ[('q_traduz', None, Z0)] = ('q_rollback', []) # Estava esperando a 1ª base.
    for base in bases:
        δ[('q_traduz', None, base)] = ('q_rollback', []) # Leu a 1ª base, limpa e entra em rollback.
        for base_estado in bases:
            δ[(f'q_baseX{base_estado}', None, base)] = ('q_rollback', []) # Leu a 2ª base, limpa e entra em rollback.

    # Lógica de limpeza: apaga todos os aminoácidos até encontrar um 'Stop'.
    for aminoacido in aminoacidos:
        if aminoacido == 'Stop':
            # Se encontra 'Stop', para de limpar o gene anterior e restaura Z0.
            δ[('q_rollback', None, aminoacido)] = ('q_rollback', [Z0])
        else:
            # Se for um aminoácido normal, apenas o remove da pilha.
            δ[('q_rollback', None, aminoacido)] = ('q_rollback', [])

    # --- FASE 4: FINALIZAÇÃO (ACEITAÇÃO) ---
    # Condições para mover para o estado final 'q_final'.
    δ[('q_rollback', None, Z0)] = ('q_final', []) # Termina após um rollback bem-sucedido.
    δ[('q_rollback', None, None)] = ('q_final', []) # Termina se o rollback esvaziar a pilha.
    for estado in estados_busca:
        # Termina se a cadeia acabar durante a fase de busca.
        δ[(estado, None, Z0)] = ('q_final', [])


    return Automato_Pilha(Q, Σ, Γ, δ, q0, Z0, F)
