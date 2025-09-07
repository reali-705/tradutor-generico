"""
Script de teste para o Automato_Pilha_Deterministico_ε configurado como um ribossomo.

Este teste valida a capacidade do autômato de:
1. Reconhecer e traduzir uma fita de RNA com um único gene.
2. Reconhecer e traduzir múltiplos genes na mesma fita.
3. Rejeitar fitas de RNA malformadas.
"""

# Importa a função fábrica que cria nosso autômato
from src import criar_ribossomo

def run_tests():
    """Executa uma série de testes de validação no autômato do ribossomo."""
    print("="*80)
    print("INICIANDO TESTES DO AUTÔMATO DE PILHA (RIBOSSOMO)".center(80))
    print("="*80)

    # 1. Cria a instância do ribossomo
    ribossomo = criar_ribossomo()

    # 2. Define os casos de teste
    # (cadeia_rna, resultado_esperado_validacao, proteina_esperada_bruta)
    test_cases = [
        (
            "AUGUUUUAA", 
            True, 
            " ehP-teM-Z0", 
            "Gene simples (Met-Phe-Stop)"
        ),
        (
            "CCCAUGUUUUAG", 
            True, 
            " ehP-teM-Z0", 
            "Gene simples com lixo no início"
        ),
        (
            "AUGUUUUAAAUGCUCUAG", 
            True, 
            " ueL-teM- ehP-teM-Z0", 
            "Dois genes na mesma fita"
        ),
        (
            "AUGUUU", 
            False, 
            "", 
            "Gene sem códon de parada (deve falhar)"
        ),
        (
            "UUUUAG", 
            False, 
            "", 
            "Gene sem códon de início (deve falhar)"
        ),
        (
            "",
            False,
            "",
            "Cadeia vazia (deve falhar)"
        )
    ]

    # 3. Executa e valida cada caso de teste
    for i, (rna, esperado_bool, esperado_proteina, descricao) in enumerate(test_cases):
        print(f"\n--- Teste {i+1}: {descricao} ---")
        print(f"    RNA de entrada: '{rna}'")
        
        try:
            # Executa a validação
            resultado_bool = ribossomo.validar(rna)
            
            # Pega a saída da pilha
            resultado_proteina = ribossomo.cadeia_saida()

            print(f"    Resultado da validação: {resultado_bool} (Esperado: {esperado_bool})")
            print(f"    Conteúdo da pilha: '{resultado_proteina}' (Esperado: '{esperado_proteina}')")

            # Verifica se os resultados estão corretos
            assert resultado_bool == esperado_bool, "O resultado da validação booleana está incorreto!"
            
            # Só verifica a proteína se a validação for um sucesso esperado
            if esperado_bool:
                assert resultado_proteina == esperado_proteina, "A proteína gerada na pilha está incorreta!"
            
            print("    -> OK: Teste passou!")

        except Exception as e:
            print(f"    -> ERRO INESPERADO: O teste falhou com a exceção: {e}")

    print("\n" + "="*80)
    print("TESTES DO RIBOSSOMO CONCLUÍDOS".center(80))
    print("="*80)


if __name__ == "__main__":
    run_tests()