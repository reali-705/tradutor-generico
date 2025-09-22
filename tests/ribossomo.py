"""
Script de teste para o Automato_Pilha configurado como um ribossomo.

Este teste valida a capacidade do autômato de:
1. Reconhecer e traduzir uma fita de RNA com um único gene.
2. Reconhecer e traduzir múltiplos genes na mesma fita.
3. Rejeitar fitas de RNA malformadas ou incompletas.
4. Lidar com "lixo" genético antes, entre e depois dos genes.
"""

from src import criar_ribossomo
import re

def formatando_proteina(proteina: list[str]) -> str:
    """
    Converte a lista de saída bruta do autômato em uma string de proteína formatada.

    Exemplo: ['Met', 'Phe', 'Stop'] -> "Met-Phe"

    Args:
        proteina: A lista de símbolos retornada pelo método transcrever_pilha.

    Returns:
        Uma string formatada representando a(s) proteína(s) traduzida(s).
    """
    if not proteina:
        return ""
    # Junta todos os itens com '-', substitui 'Stop' por um espaço e remove espaços extras.
    return re.sub(r'(-)?Stop(-)?', ' ', '-'.join(proteina)).strip()

def run_tests():
    """Executa uma série de testes de validação no autômato do ribossomo."""
    print("="*80)
    print("INICIANDO TESTES DO AUTÔMATO DE PILHA (RIBOSSOMO)".center(80))
    print("="*80)

    ribossomo = criar_ribossomo()

    # Casos de teste no formato: (descrição, rna_entrada, proteina_formatada_esperada)
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
            # 1. Executa o autômato para obter a lista de símbolos da pilha.
            resultado_pilha = ribossomo.transcrever_pilha(rna)
            # 2. Formata a lista de saída para a string de comparação.
            cadeia_proteina = formatando_proteina(resultado_pilha)
            # 3. Compara o resultado obtido com o esperado.
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