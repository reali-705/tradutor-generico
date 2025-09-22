"""
Aplicação Principal para Transcrição e Tradução Genética.

Este script oferece uma interface de linha de comando para executar o pipeline
completo de biologia computacional, permitindo a execução de múltiplas
tarefas (geração aleatória, pseudoaleatória e leitura de arquivo) em uma
única chamada.
"""

import argparse
import sys
import logging
from pathlib import Path
from src import (
    criar_transcritor_dna_rna,
    criar_ribossomo,
    gerar_dna_aleatorio,
    gerar_dna_pseudoaleatorio,
    escrever_arquivo,
    ler_arquivo,
    formatar_proteina
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
    Configura e retorna o parser de argumentos da linha de comando.
    
    Define os argumentos que o usuário pode passar ao script, como -p, -a, e -l,
    juntamente com suas ajudas e comportamentos.

    Returns:
        argparse.ArgumentParser: O objeto parser configurado e pronto para uso.
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
    Executa o pipeline completo de processamento para uma cadeia de DNA.

    Esta função orquestra a validação, transcrição para RNA, tradução para
    proteína, exibição dos resultados e salvamento dos arquivos de saída.

    Args:
        dna (str): A cadeia de DNA a ser processada.
        nome_base_arquivo (str): O nome base para os arquivos de saída (ex: 'aleatorio').
    
    Raises:
        ValueError: Se a cadeia de DNA contiver caracteres inválidos.
    """
    # Passo 1: Validação e Limpeza da Cadeia de DNA
    logging.info("Validando e limpando DNA...")
    cadeia_dna = "".join(filter(str.isalpha, dna)).upper()
    if not all(base in 'ATCG' for base in cadeia_dna):
        raise ValueError("DNA contém bases inválidas. Use apenas A, T, C, G.")
    
    # Passo 2: Transcrição para RNA usando o Transdutor Finito
    logging.info("Transcrevendo DNA para RNA...")
    transcritor = criar_transcritor_dna_rna()
    cadeia_rna = transcritor.transcrever(cadeia_dna)

    # Passo 3: Tradução para Proteína usando o Autômato de Pilha
    logging.info("Traduzindo RNA para Proteína...")
    ribossomo = criar_ribossomo()
    
    resultado_pilha = ribossomo.transcrever_pilha(cadeia_rna)
    cadeia_proteina = formatar_proteina(resultado_pilha)

    if cadeia_proteina:
        logging.info("Tradução bem-sucedida.")
    else:
        logging.warning("Nenhuma estrutura de gene válida (AUG...STOP) foi encontrada no RNA. Nenhuma proteína foi produzida.")

    # Passo 4: Exibição dos resultados formatados no terminal
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

    # Passo 5: Salvando os resultados em arquivos de saída
    logging.info("Salvando arquivos de saída...")
    escrever_arquivo(OUTPUT_PATH / f"{nome_base_arquivo}_rna.txt", cadeia_rna)
    escrever_arquivo(OUTPUT_PATH / f"{nome_base_arquivo}_proteina.txt", cadeia_proteina)
    logging.info(f"Arquivos de RNA e Proteína salvos em '{OUTPUT_PATH}'.")


def main() -> None:
    """
    Ponto de entrada principal do script.
    
    Orquestra a análise dos argumentos da linha de comando e executa as
    tarefas solicitadas na ordem definida: pseudoaleatório, aleatório e leitura de arquivo.
    """
    # Configura o sistema de logging para toda a aplicação.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    parser = setup_parser()
    
    # Se nenhum argumento for passado, exibe a ajuda e encerra.
    if len(sys.argv) == 1:
        parser.print_help()
        logging.error("Você deve fornecer pelo menos uma ação (-p, -a, ou -l).")
        return

    args = parser.parse_args()
    logging.info("Início da Execução")

    try:
        # Executa a tarefa de geração de DNA pseudoaleatório se solicitada.
        if args.pseudoaleatorio is not None:
            print("\n" + " MODO: DNA PSEUDOALEATÓRIO ".center(LARGURA_LINHA, "#"))
            dna_gerado = gerar_dna_pseudoaleatorio(args.pseudoaleatorio)
            logging.info(f"Salvando DNA gerado em '{INPUT_PATH}'...")
            escrever_arquivo(INPUT_PATH / "pseudoaleatorio_dna.txt", dna_gerado)
            processar_cadeia(dna_gerado, "pseudoaleatorio")

        # Executa a tarefa de geração de DNA aleatório se solicitada.
        if args.aleatorio is not None:
            print("\n" + " MODO: DNA ALEATÓRIO ".center(LARGURA_LINHA, "#"))
            dna_gerado = gerar_dna_aleatorio(args.aleatorio)
            logging.info(f"Salvando DNA gerado em '{INPUT_PATH}'...")
            escrever_arquivo(INPUT_PATH / "aleatorio_dna.txt", dna_gerado)
            processar_cadeia(dna_gerado, "aleatorio")

        # Executa a tarefa de leitura de arquivo se solicitada.
        if args.ler_arquivo:
            print("\n" + " MODO: LEITURA DE ARQUIVO ".center(LARGURA_LINHA, "#"))
            
            caminho_proposto = Path(args.ler_arquivo)
            # Tenta encontrar o arquivo no diretório de input se não for encontrado no caminho exato.
            if not caminho_proposto.exists():
                caminho_final = INPUT_PATH / caminho_proposto.with_suffix('.txt').name
            else:
                caminho_final = caminho_proposto

            if not caminho_final.exists():
                raise FileNotFoundError(f"Arquivo não encontrado. Verificado em '{caminho_proposto}' e '{caminho_final}'.")

            logging.info(f"Lendo arquivo: {caminho_final}")
            dna_lido = ler_arquivo(caminho_final)
            nome_base = caminho_final.stem
            processar_cadeia(dna_lido, nome_base)

    except (ValueError, FileNotFoundError) as e:
        # Captura erros esperados (ex: DNA inválido, arquivo não encontrado) e os loga como erro.
        logging.error(f"{e}")
    except Exception as e:
        # Captura qualquer outro erro inesperado e o loga como crítico, incluindo o traceback.
        logging.critical(f"Ocorreu um erro inesperado: {e}", exc_info=True)
    finally:
        # Esta mensagem será logada sempre, mesmo que ocorra um erro.
        logging.info("Execução Finalizada")

if __name__ == "__main__":
    # Garante que os diretórios de input e output existam antes de executar.
    INPUT_PATH.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    main()
