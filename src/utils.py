import random
import re
from pathlib import Path

# --- CONSTANTES DO MÓDULO ---
BASES_DNA = ('A', 'C', 'G', 'T')            # Tupla de bases nitrogenadas do DNA
CODON_START_DNA = "TAC"                     # Corresponde ao códon de início AUG no RNA
CODONS_STOP_DNA = {"ATC", "ACT", "ATT"}     # Correspondem aos códons de parada UAG, UGA, UAA no RNA
CODONS_INTERMEDIARIOS_VALIDOS = [           # Lista pré-calculada de todos os códons válidos (exceto os de parada)
    a + b + c
    for a in BASES_DNA
    for b in BASES_DNA
    for c in BASES_DNA
    if (a + b + c) not in CODONS_STOP_DNA
]

def gerar_dna_pseudoaleatorio(numero_codons: int) -> str:
    """
    Gera uma sequência de DNA com estrutura de gene (início, meio, fim).

    Args:
        numero_codons (int): O número total de códons na sequência.

    Returns:
        str: A sequência de DNA gerada.

    Raises:
        ValueError: Se o número de códons for menor que 2.
    """
    if numero_codons < 2:
        raise ValueError("O número de códons deve ser no mínimo 2.")
    
    codons_meio = random.choices(CODONS_INTERMEDIARIOS_VALIDOS, k=numero_codons - 2)
    codon_final = random.choice(list(CODONS_STOP_DNA))
    
    return CODON_START_DNA + "".join(codons_meio) + codon_final

def gerar_dna_aleatorio(tamanho: int = 1000) -> str:
    """
    Gera uma sequência aleatória de DNA com um tamanho específico.

    Args:
        tamanho (int): O comprimento desejado para a sequência de DNA.

    Returns:
        str: A sequência de DNA aleatória.
    """
    return "".join(random.choices(BASES_DNA, k=tamanho))

def nome_arquivo_valido(nome_arquivo: str) -> bool:
    """
    Verifica se um nome de arquivo é válido para o sistema de arquivos do Windows.

    Args:
        nome_arquivo (str): O nome do arquivo a ser validado.

    Returns:
        bool: True se o nome for válido, False caso contrário.
    """
    return bool(nome_arquivo.strip()) and not re.search(r'[<>:"/\\|?*]', nome_arquivo)

def escrever_arquivo(caminho_arquivo: str | Path, conteudo: str) -> None:
    """
    Escreve um conteúdo de texto em um arquivo.

    Args:
        caminho_arquivo (str | Path): O caminho completo onde o arquivo será salvo.
        conteudo (str): O texto a ser escrito no arquivo.

    Raises:
        ValueError: Se o nome do arquivo contiver caracteres inválidos.
        FileNotFoundError: Se o diretório de destino não existir.
    """
    caminho = Path(caminho_arquivo)
    if not nome_arquivo_valido(caminho.name):
        raise ValueError(f"Nome de arquivo inválido: {caminho.name}")
    
    if not caminho.parent.exists():
        raise FileNotFoundError(f"O diretório de destino '{caminho.parent}' não existe.")
    
    caminho.write_text(conteudo, encoding='utf-8')

def ler_arquivo(caminho_arquivo: str | Path) -> str:
    """
    Lê o conteúdo de texto de um arquivo.

    Args:
        caminho_arquivo (str | Path): O caminho completo do arquivo a ser lido.

    Returns:
        str: O conteúdo do arquivo.

    Raises:
        ValueError: Se o nome do arquivo contiver caracteres inválidos.
        FileNotFoundError: Se o arquivo não for encontrado no caminho especificado.
    """
    caminho = Path(caminho_arquivo)
    if not nome_arquivo_valido(caminho.name):
        raise ValueError(f"Nome de arquivo inválido: {caminho.name}")
    if not caminho.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    
    return caminho.read_text(encoding='utf-8')
