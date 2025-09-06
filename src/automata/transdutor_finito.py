"""
Módulo que implementa o Transdutor Finito.

Este autômato é responsável pelo primeiro estágio do pipeline:
a transcrição de uma sequência de DNA para uma sequência de RNA.
Ele valida a cadeia de entrada e realiza a substituição de bases.
"""

class TransdutorFinito:
    """
    Um Transdutor Finito que valida e transcreve DNA para RNA.

    A tarefa de transcrição é regular, pois cada base é substituída
    independentemente do seu contexto, tornando este o modelo teórico ideal.
    """
    def __init__(self):
        """
        Inicializa o transdutor com as regras de transcrição.
        """
        self.regras_transcricao = {
            'A': 'U',
            'T': 'A',
            'C': 'G',
            'G': 'C'
        }
        self.alfabeto_dna = set(self.regras_transcricao.keys())

    def transcrever(self, sequencia_dna):
        """
        Valida e transcreve uma única sequência de DNA para RNA.

        Args:
            sequencia_dna (str): A string contendo a sequência de DNA.

        Returns:
            str: A sequência de RNA transcrita.
            None: Se a sequência de DNA for inválida (contém caracteres não-padrão).
        """
        rna_resultante = []
        for base in sequencia_dna.upper():
            if base not in self.alfabeto_dna:
                print(f"Erro de Transcrição: Caractere inválido '{base}' encontrado na sequência de DNA.")
                return None
            
            rna_resultante.append(self.regras_transcricao[base])
        
        return "".join(rna_resultante)