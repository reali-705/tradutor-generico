"""
Testes para o Transdutor Finito (Máquina de Mealy).

Verifica se a transcrição de DNA para RNA está funcionando corretamente,
substituindo cada base pela sua correspondente na fita de RNA.
"""
import pytest
from src import criar_transcritor_dna_rna

# Instância única do transdutor para ser usada em todos os testes deste arquivo.
transcritor = criar_transcritor_dna_rna()

# Lista de casos de teste no formato: (descricao, dna_entrada, rna_esperado)
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
    """Testa a transcrição de DNA para RNA para múltiplos cenários."""
    # Executa a transcrição
    resultado = transcritor.transcrever(entrada)
    
    # Verifica se o resultado é o esperado.
    assert resultado == esperado