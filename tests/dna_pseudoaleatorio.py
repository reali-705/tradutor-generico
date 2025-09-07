"""
Script de teste para o fluxo de geração e transcrição de DNA.

Este script executa os seguintes passos:
1. Gera uma cadeia de DNA pseudoaleatória com um códon de início e fim.
2. Salva a cadeia de DNA em um arquivo de texto.
3. Lê o arquivo de DNA para verificar a integridade dos dados.
4. Transcreve a cadeia de DNA para uma cadeia de RNA usando um Transdutor Finito.
5. Salva a cadeia de RNA resultante em outro arquivo de texto.
6. Opcionalmente, limpa os arquivos gerados após a execução.

Argumentos da Linha de Comando:
-c, --codons      : Define o número de códons na cadeia de DNA gerada.
-k, --keep-files  : Se presente, impede a limpeza dos arquivos gerados.
"""

import argparse
from pathlib import Path
from src import gerar_dna_pseudoaleatorio, escrever_arquivo, ler_arquivo, criar_transcritor_dna_rna

def setup_parser() -> argparse.Namespace:
    """
    Configura e retorna o parser de argumentos da linha de comando.
    
    Returns:
        argparse.Namespace: Um objeto contendo os argumentos processados.
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
        help="Mantém os arquivos (cadeia_DNA.txt e cadeia_RNA.txt) após o teste."
    )
    return parser.parse_args()

def main() -> None:
    """
    Função principal que orquestra a execução completa do teste.
    """
    # --- Configuração Inicial ---
    args = setup_parser()
    LARGURA_LINHA = 100
    caminho_dna = Path("./data/input/dna_pseudoaleatorio_test.txt")
    caminho_rna = Path("./data/output/rna_pseudoaleatorio_transcrito_test.txt")
    num_codons = args.codons
    
    print("=" * LARGURA_LINHA)
    print("Iniciando teste de Geração e Transcrição de DNA".center(LARGURA_LINHA))
    print("=" * LARGURA_LINHA)

    try:
        # Garante que os diretórios de destino existam antes de usá-los.
        caminho_dna.parent.mkdir(parents=True, exist_ok=True)
        caminho_rna.parent.mkdir(parents=True, exist_ok=True)

        # --- 1. Geração do DNA ---
        print(f"\n[1] Gerando DNA com {num_codons} códons...")
        cadeia_dna = gerar_dna_pseudoaleatorio(num_codons)
        print(f"    -> DNA Gerado: {cadeia_dna[:60]}...")
        
        tamanho_esperado = num_codons * 3
        tamanho_cadeia = len(cadeia_dna)
        assert tamanho_cadeia == tamanho_esperado, \
            f"Tamanho da cadeia de DNA incorreto. Esperado: {tamanho_esperado}, Obtido: {tamanho_cadeia}"
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
        print(f"    -> RNA Transcrito: {cadeia_rna[:60]}...")

        assert cadeia_rna.startswith("AUG"), "A transcrição para RNA não começou com 'AUG' como esperado."
        assert len(cadeia_rna) == len(cadeia_dna), "O tamanho da cadeia de RNA não é compatível com a de DNA."
        print("    -> OK: Transcrição parece correta.")

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