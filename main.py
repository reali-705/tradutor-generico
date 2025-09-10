"""
Aplicação Principal para Transcrição e Tradução Genética.

Este script oferece uma interface de linha de comando para executar o pipeline
completo de biologia computacional, permitindo a execução de múltiplas
tarefas (geração aleatória, pseudoaleatória e leitura de arquivo) em uma
única chamada.
"""

import argparse
import sys
from pathlib import Path
from src import (
    criar_transcritor_dna_rna,
    criar_ribossomo,
    gerar_dna_aleatorio,
    gerar_dna_pseudoaleatorio,
    escrever_arquivo,
    ler_arquivo
)

# --- Constantes Globais ---
LARGURA_LINHA = 100
PREVIA_CADEIA = 60
INPUT_PATH = Path("./data/input/")
OUTPUT_PATH = Path("./data/output/")
CODONS_PSEUDOALEATORIO_DEFAULT = 1000
BASES_ALEATORIO_DEFAULT = 10000

# --- Configuração e Execução ---

def setup_parser() -> argparse.ArgumentParser:
    """
    Configura o parser de argumentos da linha de comando.
    
    Define os argumentos -p, -a, e -l, que podem ser usados em conjunto
    para executar múltiplas tarefas.
    
    Returns:
        argparse.ArgumentParser: O objeto parser configurado.
    """
    parser = argparse.ArgumentParser(
        description="Tradutor Genético: Converte DNA em Proteínas usando Teoria dos Autômatos.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "-p", "--pseudoaleatorio",
        type=int,
        nargs='?',
        const=CODONS_PSEUDOALEATORIO_DEFAULT,
        default=None,
        metavar="N_CODONS",
        help=f"Gera DNA pseudoaleatório com N_CODONS (padrão: {CODONS_PSEUDOALEATORIO_DEFAULT})."
    )
    parser.add_argument(
        "-a", "--aleatorio",
        type=int,
        nargs='?',
        const=BASES_ALEATORIO_DEFAULT,
        default=None,
        metavar="N_BASES",
        help=f"Gera DNA aleatório com N_BASES (padrão: {BASES_ALEATORIO_DEFAULT})."
    )
    parser.add_argument(
        "-l", "--ler-arquivo",
        type=str,
        metavar="ARQUIVO",
        help="Lê uma cadeia de DNA a partir de um arquivo (ex: 'meu_dna.txt' ou 'data/input/meu_dna.txt')."
    )
    return parser

# --- Funções de Processamento ---

def processar_cadeia(dna: str, nome_base_arquivo: str):
    """
    Função central que executa o pipeline de transcrição e tradução para uma
    dada cadeia de DNA e salva os arquivos de SAÍDA (output).

    Args:
        dna (str): A cadeia de DNA a ser processada.
        nome_base_arquivo (str): O nome base para os arquivos de saída (ex: 'aleatorio').
    
    Raises:
        ValueError: Se a cadeia de DNA contiver caracteres inválidos.
    """
    # Passo 1: Validação e Limpeza da Cadeia de DNA
    print("-> Validando e limpando DNA...")
    cadeia_dna = "".join(filter(str.isalpha, dna)).upper()
    if not all(base in 'ATCG' for base in cadeia_dna):
        raise ValueError("DNA contém bases inválidas. Use apenas A, T, C, G.")
    
    # Passo 2: Transcrição para RNA usando o Transdutor Finito
    print("-> Transcrevendo DNA para RNA...")
    transcritor = criar_transcritor_dna_rna()
    cadeia_rna = transcritor.transcrever(cadeia_dna)

    # Passo 3: Tradução para Proteína usando o Autômato de Pilha
    print("-> Traduzindo RNA para Proteína...")
    ribossomo = criar_ribossomo()
    cadeia_proteina = ""
    if ribossomo.validar(cadeia_rna):
        cadeia_proteina = ribossomo.cadeia_saida()[::-1] # Reverte a cadeia de saída conforme projetado
        print("-> Tradução bem-sucedida.")
    else:
        print("-> AVISO: Nenhuma estrutura de gene válida (AUG...STOP) foi encontrada no RNA. Nenhuma proteína foi produzida.")

    # Passo 4: Exibição dos resultados no terminal
    print("\n" + " RESULTADOS ".center(LARGURA_LINHA, "="))
    previa_dna = f"{cadeia_dna[:PREVIA_CADEIA]}..." if len(cadeia_dna) > PREVIA_CADEIA else cadeia_dna
    previa_rna = f"{cadeia_rna[:PREVIA_CADEIA]}..." if len(cadeia_rna) > PREVIA_CADEIA else cadeia_rna
    proteinas = cadeia_proteina.split(" ")
    previa_proteina = [
        f"{proteina[:PREVIA_CADEIA]}..." if len(proteina) > PREVIA_CADEIA else proteina
        for proteina in proteinas if proteina
    ]

    proteina_gerada = '\n    '.join(previa_proteina) if previa_proteina else 'N/A'
    
    print(f"DNA Processado ({len(cadeia_dna)} bases):\n    {previa_dna}")
    print(f"RNA Transcrito ({len(cadeia_rna)} bases):\n    {previa_rna}")
    print(f"Proteína(s) Gerada(s):\n    {proteina_gerada}")
    print("=" * LARGURA_LINHA)

    # Passo 5: Salvando os resultados em arquivos de SAÍDA (output)
    print("\n-> Salvando arquivos de saída...")
    escrever_arquivo(OUTPUT_PATH / f"{nome_base_arquivo}_rna.txt", cadeia_rna)
    escrever_arquivo(OUTPUT_PATH / f"{nome_base_arquivo}_proteina.txt", cadeia_proteina)
    print("-> Arquivos de RNA e Proteína salvos em 'data/output/'.")


def main() -> None:
    """
    Ponto de entrada principal do script.
    
    Orquestra a análise dos argumentos da linha de comando e executa as
    tarefas solicitadas na ordem definida: pseudoaleatório, aleatório e leitura de arquivo.
    """
    parser = setup_parser()
    
    # Se nenhum argumento for passado, exibe a ajuda e encerra.
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nERRO: Você deve fornecer pelo menos uma ação (-p, -a, ou -l).")
        return

    args = parser.parse_args()
    print("\n" + " Início da Execução ".center(LARGURA_LINHA, "="))

    try:
        # Executa as tarefas em uma ordem pré-definida, se os argumentos estiverem presentes.
        if args.pseudoaleatorio is not None:
            print("\n" + " MODO: DNA PSEUDOALEATÓRIO ".center(LARGURA_LINHA, "#"))
            dna_gerado = gerar_dna_pseudoaleatorio(args.pseudoaleatorio)
            # MELHORIA: Salva o DNA de ENTRADA aqui, no contexto da geração.
            print("-> Salvando DNA gerado em 'data/input/'...")
            escrever_arquivo(INPUT_PATH / "pseudoaleatorio_dna.txt", dna_gerado)
            processar_cadeia(dna_gerado, "pseudoaleatorio")

        if args.aleatorio is not None:
            print("\n" + " MODO: DNA ALEATÓRIO ".center(LARGURA_LINHA, "#"))
            dna_gerado = gerar_dna_aleatorio(args.aleatorio)
            # MELHORIA: Salva o DNA de ENTRADA aqui, no contexto da geração.
            print("-> Salvando DNA gerado em 'data/input/'...")
            escrever_arquivo(INPUT_PATH / "aleatorio_dna.txt", dna_gerado)
            processar_cadeia(dna_gerado, "aleatorio")

        if args.ler_arquivo:
            print("\n" + " MODO: LEITURA DE ARQUIVO ".center(LARGURA_LINHA, "#"))
            
            # Lógica robusta para encontrar o arquivo de entrada
            caminho_proposto = Path(args.ler_arquivo)
            if not caminho_proposto.exists():
                caminho_final = INPUT_PATH / caminho_proposto.with_suffix('.txt').name
            else:
                caminho_final = caminho_proposto

            if not caminho_final.exists():
                raise FileNotFoundError(f"Arquivo não encontrado. Verificado em '{caminho_proposto}' e '{caminho_final}'.")

            print(f"-> Lendo arquivo: {caminho_final}")
            dna_lido = ler_arquivo(caminho_final)
            nome_base = caminho_final.stem
            processar_cadeia(dna_lido, nome_base)

    except (ValueError, FileNotFoundError) as e:
        print(f"\nERRO: {e}")
    except Exception as e:
        print(f"\nERRO INESPERADO: {e}")
    finally:
        print("\n" + " Execução Finalizada ".center(LARGURA_LINHA, "=") + "\n")

if __name__ == "__main__":
    # Garante que os diretórios de dados existam antes de qualquer operação
    INPUT_PATH.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    main()
