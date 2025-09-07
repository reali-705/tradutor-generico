"""
Módulo utilitário que contém um executor de teste genérico para o fluxo de transcrição.

Este módulo abstrai a lógica repetida de geração, escrita, leitura, transcrição e
limpeza de arquivos, permitindo que os scripts de teste individuais apenas configurem
e chamem a função principal.
"""
from pathlib import Path
from typing import Callable

from src import escrever_arquivo, ler_arquivo, criar_transcritor_dna_rna

def run_transcription_test(
    nome_teste: str,
    tipo_teste: str,
    dna_path: Path,
    rna_path: Path,
    funcao_geradora: Callable[[int], str],
    argumento_funcao: int,
    keep_files: bool
) -> None:
    """
    Executa um fluxo de teste de transcrição genérico e valida os resultados.

    Args:
        nome_teste (str): O nome do teste para exibição.
        tipo_teste (str): O modo de teste ('aleatorio' ou 'pseudo') para validações específicas.
        dna_path (Path): O caminho para o arquivo de DNA de saída.
        rna_path (Path): O caminho para o arquivo de RNA de saída.
        funcao_geradora (Callable[[int], str]): A função a ser chamada para gerar o DNA.
        argumento_funcao (int): O argumento numérico para a função de geração (número de bases ou códons).
        keep_files (bool): Se True, os arquivos gerados não são apagados ao final.
    
    Raises:
        ValueError: Se um `tipo_teste` desconhecido for fornecido.
        AssertionError: Se qualquer uma das validações durante o teste falhar.
    """
    # --- Configuração Inicial ---
    LARGURA_LINHA = 100
    PREVIA_CADEIA = 50
    dna_path.parent.mkdir(parents=True, exist_ok=True)
    rna_path.parent.mkdir(parents=True, exist_ok=True)

    print("=" * LARGURA_LINHA)
    print(f"Iniciando teste de Geração ({nome_teste}) e Transcrição de DNA".center(LARGURA_LINHA))
    print("=" * LARGURA_LINHA)

    try:
        # --- 1. Geração e Validação do DNA ---
        print(f"\n[1] Gerando e validando DNA...")
        cadeia_dna = funcao_geradora(argumento_funcao)
        previa_dna = f"{cadeia_dna[:PREVIA_CADEIA]}..." if len(cadeia_dna) > PREVIA_CADEIA else cadeia_dna
        print(f"    -> DNA Gerado: {previa_dna}")

        if tipo_teste == 'pseudo':
            tamanho_esperado = argumento_funcao * 3
            assert len(cadeia_dna) == tamanho_esperado, f"Tamanho incorreto. Esperado: {tamanho_esperado}, Obtido: {len(cadeia_dna)}"
        elif tipo_teste == 'aleatorio':
            assert len(cadeia_dna) == argumento_funcao, f"Tamanho incorreto. Esperado: {argumento_funcao}, Obtido: {len(cadeia_dna)}"
        else:
            raise ValueError(f"Modo de teste desconhecido: '{tipo_teste}'")
        print("    -> OK: Tamanho da cadeia de DNA está correto.")

        # --- 2. Escrita e Leitura do DNA ---
        print("\n[2] Escrevendo e lendo o arquivo de DNA...")
        escrever_arquivo(dna_path, cadeia_dna)
        cadeia_dna_lida = ler_arquivo(dna_path)
        assert cadeia_dna_lida == cadeia_dna, "Conteúdo lido não corresponde ao gerado."
        print(f"    -> OK: Arquivo '{dna_path}' lido com sucesso.")

        # --- 3. Transcrição e Validação do RNA ---
        print("\n[3] Transcrevendo e validando RNA...")
        transcritor = criar_transcritor_dna_rna()
        cadeia_rna = transcritor.transcrever(cadeia_dna_lida)
        previa_rna = f"{cadeia_rna[:PREVIA_CADEIA]}..." if len(cadeia_rna) > PREVIA_CADEIA else cadeia_rna
        print(f"    -> RNA Transcrito: {previa_rna}")

        # --- Validações Específicas do RNA ---
        if tipo_teste == 'pseudo':
            assert cadeia_rna.startswith("AUG"), "RNA não começou com 'AUG' como esperado."
        assert len(cadeia_rna) == len(cadeia_dna), "Tamanho da cadeia de RNA incompatível com a de DNA."
        print("    -> OK: Transcrição parece correta.")

        # --- 4. Escrita do RNA ---
        print("\n[4] Escrevendo arquivo de RNA...")
        escrever_arquivo(rna_path, cadeia_rna)
        print(f"    -> OK: Arquivo '{rna_path}' escrito com sucesso.")

        print("\n" + " TESTE CONCLUÍDO COM SUCESSO ".center(LARGURA_LINHA, "="))

    except Exception as e:
        print(f"\nERRO DURANTE O TESTE: {e}")

    finally:
        # --- 5. Limpeza dos Arquivos ---
        print("\n[5] Finalizando execução...")
        if keep_files:
            print("    -> Mantendo arquivos de teste conforme solicitado (--keep-files).")
        else:
            print("    -> Limpando arquivos de teste...")
            if dna_path.exists():
                dna_path.unlink()
                print(f"       - Arquivo '{dna_path}' removido.")
            if rna_path.exists():
                rna_path.unlink()
                print(f"       - Arquivo '{rna_path}' removido.")
        print("=" * LARGURA_LINHA)