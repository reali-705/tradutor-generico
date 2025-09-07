"""
Módulo que implementa o Transdutor Finito como Máquina de Mealy.

Um transdutor finito do tipo Mealy é um autômato finito que, para cada transição de estado,
também produz um símbolo de saída, permitindo transformar cadeias de entrada em cadeias de saída.
"""

class TransdutorFinito:
    """
    Classe que representa um Transdutor Finito baseado na Máquina de Mealy.

    A máquina de Mealy é definida por:
        - Q: conjunto de estados
        - Σ: alfabeto de entrada
        - Γ: alfabeto de saída
        - δ: função de transição de estados (Q × Σ → Q)
        - λ: função de saída (Q × Σ → Γ)
        - q0: estado inicial
    """

    def __init__(
        self,
        Q: set[str],                    # Conjunto de estados
        Σ: set[str],                    # Alfabeto de entrada
        Γ: set[str],                    # Alfabeto de saída
        δ: dict[tuple[str, str], str],  # Função de transição de estados: (estado, símbolo) -> novo_estado
        λ: dict[tuple[str, str], str],  # Função de saída: (estado, símbolo) -> símbolo de saída
        q0: str,                        # Estado inicial
    ):
        """
        Inicializa o transdutor finito com os componentes da máquina de Mealy.

        Args:
            Q (set[str]): Conjunto de estados.
            Σ (set[str]): Alfabeto de entrada.
            Γ (set[str]): Alfabeto de saída.
            δ (dict[tuple[str, str], str]): Função de transição de estados.
            λ (dict[tuple[str, str], str]): Função de saída.
            q0 (str): Estado inicial.
        """
        self.estados = Q
        self.alfabeto_entrada = Σ
        self.alfabeto_saida = Γ
        self.funcao_transicao = δ
        self.funcao_saida = λ
        self.estado_inicial = q0

    def transcrever(self, cadeia: str) -> str:
        """
        Processa uma cadeia de entrada e retorna a cadeia de saída correspondente,
        conforme as funções de transição e saída da máquina de Mealy.

        Args:
            cadeia (str): Cadeia de entrada a ser processada.

        Returns:
            str: Cadeia de saída gerada pelo transdutor.

        Raises:
            ValueError: Se encontrar símbolo inválido, transição ou saída indefinida.
        """
        resultado = []
        estado_atual = self.estado_inicial
        
        for simbolo in cadeia:
            # Verifica se o símbolo pertence ao alfabeto de entrada
            if simbolo not in self.alfabeto_entrada:
                raise ValueError(f"Símbolo '{simbolo}' não pertence ao alfabeto de entrada.")

            tupla = (estado_atual, simbolo)
            # Obtém o próximo estado a partir da função de transição
            estado_proximo = self.funcao_transicao.get(tupla, None)
            if estado_proximo is None:
                raise ValueError(f"Transição não definida para {tupla}.")
            # Obtém o símbolo de saída correspondente
            saida = self.funcao_saida.get(tupla, None)
            if saida is None:
                raise ValueError(f"Saída não definida para {tupla}.")

            resultado.append(saida)
            estado_atual = estado_proximo  # Atualiza o estado atual para o próximo estado

        return ''.join(resultado)
