"""
Testes para as funções de geração de DNA.

Valida as propriedades das cadeias de DNA geradas pelas funções
`gerar_dna_aleatorio` e `gerar_dna_pseudoaleatorio`.
"""
import pytest
from src import gerar_dna_aleatorio, gerar_dna_pseudoaleatorio

# Lista de tamanhos usada para parametrizar os testes.
TAMANHOS = [10, 100, 1000, 10000]

# --- Testes para gerar_dna_aleatorio ---

@pytest.mark.parametrize("tamanho", TAMANHOS)
def test_dna_aleatorio_tamanho(tamanho):
    """Verifica se o DNA aleatório gerado tem o comprimento solicitado."""
    dna = gerar_dna_aleatorio(tamanho)
    assert len(dna) == tamanho

def test_dna_aleatorio_alfabeto():
    """Verifica se o DNA aleatório contém apenas as bases válidas (A, T, C, G)."""
    dna = gerar_dna_aleatorio(1000)
    assert set(dna).issubset(set("ATCG"))

def test_dna_aleatorio_aleatoriedade():
    """Verifica se duas chamadas geram resultados diferentes (teste básico de aleatoriedade)."""
    dna1 = gerar_dna_aleatorio(TAMANHOS[2])
    dna2 = gerar_dna_aleatorio(TAMANHOS[2])
    assert dna1 != dna2

# --- Testes para gerar_dna_pseudoaleatorio ---

# O número de códons é derivado da lista de tamanhos para fornecer uma variedade de entradas.
# Garante que o número de códons seja no mínimo 2 para incluir início e parada.
@pytest.mark.parametrize("codons", filter(lambda x: x >= 2, map(lambda x: x // 3, TAMANHOS)))
def test_dna_pseudoaleatorio_tamanho(codons):
    """Verifica se o DNA pseudoaleatório tem o comprimento total correto (codons = bases / 3)."""
    dna = gerar_dna_pseudoaleatorio(codons)
    assert len(dna) == codons * 3

def test_dna_pseudoaleatorio_estrutura():
    """Verifica a estrutura do gene na fita molde: início com TAC e fim com algum códon de parada (ATC, ACT, ATT)."""
    # Gera uma cadeia com um número suficiente de códons para análise.
    dna = gerar_dna_pseudoaleatorio(TAMANHOS[2] // 3)
    assert dna.startswith("TAC")
    assert dna[-3:] in ["ATC", "ACT", "ATT"]

def test_dna_pseudoaleatorio_alfabeto_meio():
    """Verifica se o 'miolo' do gene (entre início e parada) contém apenas bases válidas."""
    dna = gerar_dna_pseudoaleatorio(TAMANHOS[2] // 3)
    
    # Isola a parte do meio da cadeia de DNA.
    meio_dna = dna[3:-3]
    
    # Verifica se o miolo contém apenas as bases do alfabeto de DNA.
    assert set(meio_dna).issubset(set("ATCG"))
    
    # Garante que o miolo também é composto por códons completos.
    assert len(meio_dna) % 3 == 0