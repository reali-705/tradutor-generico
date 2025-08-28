class TradutorDNA:
    def __init__(self):
        self.V = {'A', 'C', 'G', 'T', 'U'}
        self.Σ = {'A', 'C', 'G', 'T', 'U'}
        self.R = {'A': 'U', 'C': 'G', 'G': 'C', 'T': 'A'}
        self.S = {'A', 'C', 'G', 'T', 'U'}

    def traduzir(self, dna):
        return ''.join(self.R.get(base, base) for base in dna)