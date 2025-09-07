"""
Ponto de entrada para o teste de geração de DNA pseudoaleatório.

Este script configura os argumentos da linha de comando específicos para a geração
de DNA pseudoaleatório e, em seguida, invoca o executor de teste genérico para
realizar o fluxo completo de validação e transcrição.
"""

import argparse
from pathlib import Path
from src import gerar_dna_pseudoaleatorio
from ._modelo_testes import run_transcription_test

def setup_parser() -> argparse.Namespace:
    """
    Configura e processa os argumentos da linha de comando para este teste.

    Define os argumentos para o número de códons a serem gerados e a opção
    de manter os arquivos de saída.

    Returns:
        argparse.Namespace: Um objeto contendo os argumentos fornecidos pelo usuário.
    """
    parser = argparse.ArgumentParser(description="Teste de geração de DNA pseudoaleatório e transcrição para RNA")
    parser.add_argument(
        "-c", "--codons",
        type=int,
        default=10,
        help="Número de códons a serem gerados na cadeia de DNA (padrão: 10)."
    )
    parser.add_argument(
        "-k", "--keep-files",
        action="store_true",
        default=False,
        help="Mantém os arquivos gerados após o teste."
    )
    return parser.parse_args()

def main() -> None:
    """
    Função principal que configura e executa o teste de DNA pseudoaleatório.

    Esta função lê os argumentos da linha de comando e chama o executor de
    teste genérico (`run_transcription_test`) com os parâmetros apropriados
    para o teste de DNA pseudoaleatório.
    """
    args = setup_parser()
    
    # Chama o executor de teste genérico com as configurações específicas
    # para a geração de DNA pseudoaleatório.
    run_transcription_test(
        nome_teste="Pseudoaleatória",
        tipo_teste='pseudo',
        dna_path=Path("./data/input/dna_pseudoaleatorio_test.txt"),
        rna_path=Path("./data/output/rna_pseudoaleatorio_transcrito_test.txt"),
        funcao_geradora=gerar_dna_pseudoaleatorio,
        argumento_funcao=args.codons,
        keep_files=args.keep_files
    )

if __name__ == "__main__":
    main()