import pytest
from src import criar_transcritor_dna_rna

transcritor = criar_transcritor_dna_rna()

test_cases = [
    ("Cadeia simples", "ATCG", "UAGC"),
    ("Cadeia longa", "GATTACA", "CUAAUGU"),
    ("Apenas uma base A", "AAAA", "UUUU"),
    ("Apenas uma base T", "TTTT", "AAAA"),
    ("Apenas uma base C", "CCCC", "GGGG"),
    ("Apenas uma base G", "GGGG", "CCCC"),
    ("Cadeia vazia", "", ""),
    ("Cadeia mista", "AGCTTGCAA", "UCGAACGUU")
]

@pytest.mark.parametrize("descricao, entrada, esperado", test_cases)
def test_transcritor(descricao, entrada, esperado):
    resultado = transcritor.transcrever(entrada)
    assert resultado == esperado, f"Falha no teste: {descricao}"