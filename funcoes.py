import random

def gerar_dna_pseudoaleatorio(numero_codons: int) -> str:
    codon_start = "TAC"  # Códon de início no DNA (gera AUG no RNA)
    codon_stop = ["ATC", "ACT", "ATT"]  # Códons de parada no DNA (geram UAG, UGA, UAA no RNA)
    bases = ['A', 'C', 'G', 'T']
    # Gera códons intermediários, evitando códons de parada
    codons_intermediarios = []
    for _ in range(numero_codons - 2):
        while True:
            codon = ''.join(random.choices(bases, k=3))
            if codon not in codon_stop:
                codons_intermediarios.append(codon)
                break
    return codon_start + ''.join(codons_intermediarios) + random.choice(codon_stop)

def transcrever_dna(dna: str) -> str:
    # Transcrição considerando fita molde (complementar): A->U, T->A, C->G, G->C
    rna = {
        'A': 'U',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }
    return ''.join([rna[base] for base in dna])

