"""
Script de teste para o Automato_Pilha_Deterministico_ε configurado como um ribossomo.

Este teste valida a capacidade do autômato de:
1. Reconhecer e traduzir uma fita de RNA com um único gene.
2. Reconhecer e traduzir múltiplos genes na mesma fita.
3. Rejeitar fitas de RNA malformadas ou incompletas.
4. Lidar com "lixo" genético antes, entre e depois dos genes.
"""
from src import criar_ribossomo

def formatar_proteina(pilha_bruta: str) -> str:
    """
    Limpa e formata a string bruta da pilha para uma representação legível da proteína.
    Exemplo: " ueL-teM- ehP-teM-Z0" -> "Met-Phe Met-Leu"
    """
    # Remove o marcador inicial e os hifens
    limpa = pilha_bruta.replace("Z0", "").replace("-", "")
    # Divide as proteínas (separadas por espaço) e inverte cada aminoácido
    proteinas = [
        "".join([amino[::-1] for amino in parte.split()])
        for parte in limpa.split(" ") if parte
    ]
    # Junta os aminoácidos com hifens e as proteínas com espaços
    return " ".join(["-".join(p) for p in reversed(proteinas)])

def run_tests():
    """Executa uma série de testes de validação no autômato do ribossomo."""
    print("="*80)
    print("INICIANDO TESTES DO AUTÔMATO DE PILHA (RIBOSSOMO)".center(80))
    print("="*80)

    ribossomo = criar_ribossomo()

    # Formato: (descrição, rna_entrada, validacao_esperada, proteina_formatada_esperada)
    test_cases = [
        ("Gene simples", "AUGUUUUAA", True, "Met-Phe"),
        ("Gene com lixo no início", "CCCAUGUUUUAG", True, "Met-Phe"),
        ("Gene com lixo no final", "AUGUUUUAGCCC", True, "Met-Phe"),
        ("Dois genes", "AUGUUUUAAAUGCUCUAG", True, "Met-Phe Met-Leu"),
        ("Dois genes com lixo entre eles", "AUGUUUUAAXXXAUGCUCUAG", True, "Met-Phe Met-Leu"),
        ("Gene sem códon de parada", "AUGUUU", False, ""),
        ("Gene sem códon de início", "UUUUAG", False, ""),
        ("Cadeia vazia", "", False, ""),
        ("Apenas códon de início", "AUG", False, ""),
        ("Apenas códon de parada", "UAA", False, ""),
        ("Cadeia com apenas 2 bases", "AU", False, ""),
    ]

    testes_passaram = 0
    for i, (descricao, rna, esperado_bool, esperado_proteina) in enumerate(test_cases):
        print(f"\n--- Teste {i+1}: {descricao} ---")
        print(f"    RNA de entrada: '{rna}'")
        
        try:
            resultado_bool = ribossomo.validar(rna)
            pilha_bruta = ribossomo.cadeia_saida()
            resultado_proteina = formatar_proteina(pilha_bruta)

            print(f"    Validação: {resultado_bool} (Esperado: {esperado_bool})")
            print(f"    Proteína: '{resultado_proteina}' (Esperada: '{esperado_proteina}')")

            assert resultado_bool == esperado_bool, "Resultado da validação booleana incorreto!"
            if esperado_bool:
                assert resultado_proteina == esperado_proteina, "Proteína gerada incorreta!"
            
            print("    -> SUCESSO")
            testes_passaram += 1

        except Exception as e:
            print(f"    -> FALHA: Ocorreu um erro inesperado: {e}")

    print("\n" + "="*80)
    print(f"TESTES CONCLUÍDOS: {testes_passaram}/{len(test_cases)} passaram.".center(80))
    print("="*80)

if __name__ == "__main__":
    run_tests()