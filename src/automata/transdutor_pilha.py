# -*- coding: utf-8 -*-
"""
Módulo que implementa o Transdutor de Pilha.

Este autômato é responsável pelo segundo estágio do pipeline:
a validação sintática e a tradução de uma sequência de RNA para uma proteína.
"""
from ..tabela_codons import TABELA_CODONS

class TransdutorPilha:
    """
    Um Transdutor de Pilha que valida e traduz RNA para uma cadeia de aminoácidos.

    Este modelo é ideal para reconhecer a estrutura gramatical de um gene
    (INÍCIO-CORPO-FIM), que é uma linguagem livre de contexto. A pilha é usada
    simbolicamente aqui para construir a proteína durante a validação.
    """
    def __init__(self):
        """
        Inicializa o tradutor com os códons de início e parada.
        """
        self.codon_inicio = 'AUG'
        self.codons_parada = {'UAA', 'UAG', 'UGA'}
        self.tabela_codons = TABELA_CODONS

    def traduzir(self, sequencia_rna):
        """
        Valida e traduz uma única sequência de RNA para uma proteína.

        Args:
            sequencia_rna (str): A string contendo a sequência de RNA.

        Returns:
            str: A cadeia de aminoácidos (proteína).
            None: Se a sequência de RNA não tiver uma estrutura traduzível válida.
        """
        try:
            # 1. Encontrar o primeiro códon de início 'AUG'
            start_index = sequencia_rna.find(self.codon_inicio)
            if start_index == -1:
                print("Erro de Tradução: Códon de início 'AUG' não encontrado.")
                return None

            proteina = []
            # Começa a ler a partir do códon de início
            for i in range(start_index, len(sequencia_rna), 3):
                # Garante que temos um códon completo de 3 bases
                if i + 3 > len(sequencia_rna):
                    print("Aviso de Tradução: Sequência terminou sem um códon de parada claro.")
                    break
                
                codon = sequencia_rna[i:i+3]
                
                # 2. Verifica se o códon é de parada
                if codon in self.codons_parada:
                    # Tradução bem-sucedida, encontrou o fim.
                    return "-".join(proteina)
                
                # 3. Traduz o códon e adiciona à "pilha" (nossa lista de proteína)
                aminoacido = self.tabela_codons.get(codon, '?') # '?' para códons desconhecidos
                proteina.append(aminoacido)
            
            # Se o loop terminar sem encontrar um códon de parada
            print("Aviso de Tradução: A tradução percorreu a sequência inteira sem encontrar um códon de parada.")
            return "-".join(proteina)

        except Exception as e:
            print(f"Um erro inesperado ocorreu durante a tradução: {e}")
            return None
