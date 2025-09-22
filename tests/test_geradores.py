import pytest
from src import gerar_dna_aleatorio, gerar_dna_pseudoaleatorio

TAMANHOS = [10, 100, 1000, 10000]

@pytest.mark.parametrize("tamanho", TAMANHOS)
def test_dna_aleatorio_tamanho(tamanho):
    dna = gerar_dna_aleatorio(tamanho)
    assert len(dna) == tamanho

def test_dna_aleatorio_alfabeto():
    dna = gerar_dna_aleatorio(1000)
    assert set(dna).issubset(set("ATCG"))

def test_dna_aleatorio_aleatoriedade():
    dna1 = gerar_dna_aleatorio(TAMANHOS[2])
    dna2 = gerar_dna_aleatorio(TAMANHOS[2])
    assert dna1 != dna2

@pytest.mark.parametrize("codons", map(lambda x: x // 3, TAMANHOS))
def test_dna_pseudoaleatorio_tamanho(codons):
    dna = gerar_dna_pseudoaleatorio(codons)
    assert len(dna) == codons * 3

def test_dna_pseudoaleatorio_estrutura():
    dna = gerar_dna_pseudoaleatorio(TAMANHOS[2] // 3)
    assert dna.startswith("TAC")
    assert dna[-3:] in ["ATC", "ACT", "ATT"]

def test_dna_pseudoaleatorio_alfabeto_meio():
    dna = gerar_dna_pseudoaleatorio(TAMANHOS[2] // 3)
    assert set(dna[3:-3]).issubset(set("ATCG"))