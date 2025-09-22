import pytest
from src import criar_ribossomo, formatar_proteina

ribossomo = criar_ribossomo()

test_cases = [
    ("Gene simples", "AUGUUUUAA", "Met-Phe"),
    ("Gene com lixo no início", "GCUAGCAUGUUUUAA", "Met-Phe"),
    ("Gene com lixo no fim", "AUGUUUUAAGCUAGC", "Met-Phe"),
    ("Dois genes", "AUGUUUUAAAUGCCCUAG", "Met-Phe Met-Pro"),
    ("Cadeia vazia", "", ""),
    ("Sem códon de início", "UUUCCCUUU", ""),
    ("Gene incompleto no final", "AUGUUU", ""),
    ("Apenas códon de início e parada", "AUGUAA", "Met"),
    ("Apenas lixo genético", "GCUAGCUAG", "")
]

@pytest.mark.parametrize("descricao, rna, saida_esperada", test_cases)
def test_ribossomo(descricao, rna, saida_esperada):
    proteina = ribossomo.transcrever_pilha(rna)
    assert saida_esperada == formatar_proteina(proteina)