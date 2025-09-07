"""
Script de teste para o fluxo de geração de DNA aleatório e transcrição.

Este script executa os seguintes passos:
1. Gera uma cadeia de DNA completamente aleatória com um tamanho definido.
2. Salva a cadeia de DNA em um arquivo de texto.
3. Lê o arquivo para verificar a integridade dos dados.
4. Transcreve a cadeia de DNA para uma cadeia de RNA usando um Transdutor Finito.
5. Salva a cadeia de RNA resultante em outro arquivo de texto.
6. Opcionalmente, limpa os arquivos gerados após a execução.

Argumentos da Linha de Comando:
-b, --bases       : Define o número de bases (tamanho) da cadeia de DNA.
-k, --keep-files  : Se presente, impede a limpeza dos arquivos gerados.
"""

import argparse
from pathlib import Path
from src import gerar_dna_aleatorio, escrever_arquivo, ler_arquivo, criar_transcritor_dna_rna

def setup_parser() -> argparse.Namespace:
    """
    Configura e retorna o parser de argumentos da linha de comando.
    
    Returns:
        argparse.Namespace: Um objeto contendo os argumentos processados.
    """
    parser = argparse.ArgumentParser(description="Teste de geração de DNA aleatório e transcrição para RNA")
    parser.add_argument(
        "-b", "--bases",
        type=int,
        default=50,
        help="Número de bases a serem geradas na cadeia de DNA (padrão: 50)."
    )
    parser.add_argument(
        "-k", "--keep-files",
        action="store_true",
        default=False,
        help="Mantém os arquivos (cadeia_DNA.txt e cadeia_RNA.txt) após o teste."
    )
    return parser.parse_args()

def main() -> None:
    """
    Função principal que orquestra a execução completa do teste.
    
    Realiza a geração de uma cadeia de DNA aleatória, sua escrita em arquivo,
    leitura, transcrição para RNA e, finalmente, a escrita do RNA em outro arquivo,
    validando cada etapa do processo.
    """
    # --- Configuração Inicial ---
    args = setup_parser()
    num_bases = args.bases
    LARGURA_LINHA = 100
    PREVIA_CADEIA = 50
    caminho_dna = Path("./data/input/dna_aleatorio_test.txt")
    caminho_rna = Path("./data/output/rna_aleatorio_transcrito_test.txt")

    # Garante que os diretórios de destino existam antes de usá-los.
    caminho_dna.parent.mkdir(parents=True, exist_ok=True)
    caminho_rna.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * LARGURA_LINHA)
    print("Iniciando teste de Geração (Aleatória) e Transcrição de DNA".center(LARGURA_LINHA))
    print("=" * LARGURA_LINHA)

    try:
        # --- 1. Geração do DNA ---
        print(f"\n[1] Gerando DNA com {num_bases} bases...")
        cadeia_dna = gerar_dna_aleatorio(num_bases)
        previa_dna = f"{cadeia_dna[:PREVIA_CADEIA]}..." if len(cadeia_dna) > PREVIA_CADEIA else cadeia_dna
        print(f"    -> DNA Gerado: {previa_dna}")

        tamanho_cadeia = len(cadeia_dna)
        assert tamanho_cadeia == num_bases, \
            f"Tamanho da cadeia gerada ({tamanho_cadeia}) não corresponde ao esperado ({num_bases})."
        print("    -> OK: Tamanho da cadeia de DNA está correto.")

        # --- 2. Escrita e Leitura do DNA ---
        print("\n[2] Escrevendo e lendo o arquivo de DNA...")
        escrever_arquivo(caminho_dna, cadeia_dna)
        cadeia_dna_lida = ler_arquivo(caminho_dna)
        
        assert cadeia_dna_lida == cadeia_dna, "O conteúdo lido do arquivo de DNA não corresponde ao gerado."
        print(f"    -> OK: Arquivo '{caminho_dna}' lido com sucesso.")

        # --- 3. Transcrição para RNA ---
        print("\n[3] Transcrevendo DNA para RNA...")
        transcritor = criar_transcritor_dna_rna()
        cadeia_rna = transcritor.transcrever(cadeia_dna_lida)
        previa_rna = f"{cadeia_rna[:PREVIA_CADEIA]}..." if len(cadeia_rna) > PREVIA_CADEIA else cadeia_rna
        print(f"    -> RNA Transcrito: {previa_rna}")

        assert len(cadeia_rna) == len(cadeia_dna), "O tamanho da cadeia de RNA não é compatível com a de DNA."
        print("    -> OK: Transcrição concluída.")

        # --- 4. Escrita do RNA ---
        print("\n[4] Escrevendo arquivo de RNA...")
        escrever_arquivo(caminho_rna, cadeia_rna)
        print(f"    -> OK: Arquivo '{caminho_rna}' escrito com sucesso.")

        print("\n" + " TESTE CONCLUÍDO COM SUCESSO ".center(LARGURA_LINHA, "="))

    except Exception as e:
        print(f"\nERRO DURANTE O TESTE: {e}")
        
    finally:
        # --- 5. Limpeza dos Arquivos ---
        print("\n[5] Finalizando execução...")
        if args.keep_files:
            print("    -> Mantendo arquivos de teste conforme solicitado (--keep-files).")
        else:
            print("    -> Limpando arquivos de teste...")
            if caminho_dna.exists():
                caminho_dna.unlink()
                print(f"       - Arquivo '{caminho_dna}' removido.")
            if caminho_rna.exists():
                caminho_rna.unlink()
                print(f"       - Arquivo '{caminho_rna}' removido.")

        print("=" * LARGURA_LINHA)


if __name__ == "__main__":
    main()