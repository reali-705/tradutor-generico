"""
Testes para o Autômato de Pilha (Ribossomo).

Verifica a lógica de tradução de RNA para proteína em diversos cenários,
incluindo genes simples, múltiplos genes, cadeias com "lixo" genético
e casos extremos, validando a gramática implementada.
"""

import pytest
from src import criar_ribossomo, formatar_proteina

# Instância única do ribossomo para ser usada em todos os testes.
ribossomo = criar_ribossomo()

# Casos de teste no formato: (descricao, rna_de_entrada, proteina_esperada)
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
    """Testa a tradução de RNA para proteína em múltiplos cenários."""
    proteina = ribossomo.transcrever_pilha(rna)
    assert saida_esperada == formatar_proteina(proteina)