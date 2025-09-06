# Dicionário completo de códons de mRNA para aminoácidos (Tabela do Código Genético Padrão)
# As chaves são os códons e os valores são os aminoácidos correspondentes.

tabela_codons = {
    # Metionina (Met) / CÓDON DE INÍCIO
    'AUG': 'Met',

    # CÓDONS DE PARADA (Stop)
    'UAA': 'Stop', 'UAG': 'Stop', 'UGA': 'Stop',

    # Fenilalanina (Phe)
    'UUU': 'Phe', 'UUC': 'Phe',

    # Leucina (Leu)
    'UUA': 'Leu', 'UUG': 'Leu',
    'CUU': 'Leu', 'CUC': 'Leu', 'CUA': 'Leu', 'CUG': 'Leu',

    # Isoleucina (Ile)
    'AUU': 'Ile', 'AUC': 'Ile', 'AUA': 'Ile',

    # Valina (Val)
    'GUU': 'Val', 'GUC': 'Val', 'GUA': 'Val', 'GUG': 'Val',

    # Serina (Ser)
    'UCU': 'Ser', 'UCC': 'Ser', 'UCA': 'Ser', 'UCG': 'Ser',
    'AGU': 'Ser', 'AGC': 'Ser',

    # Prolina (Pro)
    'CCU': 'Pro', 'CCC': 'Pro', 'CCA': 'Pro', 'CCG': 'Pro',

    # Treonina (Thr)
    'ACU': 'Thr', 'ACC': 'Thr', 'ACA': 'Thr', 'ACG': 'Thr',

    # Alanina (Ala)
    'GCU': 'Ala', 'GCC': 'Ala', 'GCA': 'Ala', 'GCG': 'Ala',

    # Tirosina (Tyr)
    'UAU': 'Tyr', 'UAC': 'Tyr',

    # Histidina (His)
    'CAU': 'His', 'CAC': 'His',

    # Glutamina (Gln)
    'CAA': 'Gln', 'CAG': 'Gln',

    # Asparagina (Asn)
    'AAU': 'Asn', 'AAC': 'Asn',

    # Lisina (Lys)
    'AAA': 'Lys', 'AAG': 'Lys',

    # Ácido Aspártico (Asp)
    'GAU': 'Asp', 'GAC': 'Asp',

    # Ácido Glutâmico (Glu)
    'GAA': 'Glu', 'GAG': 'Glu',

    # Cisteína (Cys)
    'UGU': 'Cys', 'UGC': 'Cys',

    # Triptofano (Trp)
    'UGG': 'Trp',

    # Arginina (Arg)
    'CGU': 'Arg', 'CGC': 'Arg', 'CGA': 'Arg', 'CGG': 'Arg',
    'AGA': 'Arg', 'AGG': 'Arg',

    # Glicina (Gly)
    'GGU': 'Gly', 'GGC': 'Gly', 'GGA': 'Gly', 'GGG': 'Gly'
}
