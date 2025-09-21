"""
Script de teste para o Automato_Pilha_Deterministico_ε configurado como um ribossomo.

Este teste valida a capacidade do autômato de:
1. Reconhecer e traduzir uma fita de RNA com um único gene.
2. Reconhecer e traduzir múltiplos genes na mesma fita.
3. Rejeitar fitas de RNA malformadas ou incompletas.
4. Lidar com "lixo" genético antes, entre e depois dos genes.
"""

from src import criar_ribossomo
import re

def formatando_proteina(proteina: list[str]) -> str:
    if not proteina:
        return ""
    return re.sub(r'(-)?Stop(-)?', ' ', '-'.join(proteina)).strip() # Remove "Stop" se houver

def run_tests():
    """Executa uma série de testes de validação no autômato do ribossomo."""
    print("="*80)
    print("INICIANDO TESTES DO AUTÔMATO DE PILHA (RIBOSSOMO)".center(80))
    print("="*80)

    ribossomo = criar_ribossomo()

    # Formato: (descrição, rna_entrada, proteina_formatada_esperada)
    test_cases = [
        ("Gene simples", "AUGUUUUAA", "Met-Phe"),
        ("Gene com lixo no início", "CCCAUGUUUUAG", "Met-Phe"),
        ("Gene com lixo no final", "AUGUUUUAGCCC", "Met-Phe"),
        ("Dois genes", "AUGUUUUAAAUGCUCUAG", "Met-Phe Met-Leu"),
        ("Dois genes com lixo entre eles", "AUGUUUUAAAAAAUGCUCUAG", "Met-Phe Met-Leu"),
        ("Gene sem códon de parada", "AUGUUU", ""),
        ("Gene sem códon de início", "UUUUAG", ""),
        ("Cadeia vazia", "", ""),
        ("Apenas códon de início", "AUG", ""),
        ("Apenas códon de parada", "UAA", ""),
        ("Cadeia com apenas 2 bases", "AU", ""),
    ]

    testes_passaram = 0
    for i, (descricao, rna, esperado_proteina) in enumerate(test_cases):
        print(f"\n--- Teste {i+1}: {descricao} ---")
        print(f"    RNA de entrada: '{rna}'")
        
        try:
            cadeia_proteina = formatando_proteina(ribossomo.transcrever_pilha(rna))
            assert cadeia_proteina == esperado_proteina, f"Esperado: '{esperado_proteina}', Obtido: '{cadeia_proteina}'"
            
            print("    -> SUCESSO")
            testes_passaram += 1

        except Exception as e:
            print(f"    -> FALHA: Ocorreu um erro inesperado: {e}")

    print("\n" + "="*80)
    print(f"TESTES CONCLUÍDOS: {testes_passaram}/{len(test_cases)} passaram.".center(80))
    print("="*80)

if __name__ == "__main__":
    run_tests()