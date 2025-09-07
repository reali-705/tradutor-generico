"""
Módulo que implementa o Transdutor Finito como Máquina de Mealy.

Um transdutor finito do tipo Mealy é um autômato finito que, para cada transição de estado,
também produz um símbolo de saída, permitindo transformar cadeias de entrada em cadeias de saída.
"""

class TransdutorFinito:
    """
    Classe que representa um Transdutor Finito baseado na Máquina de Mealy.

    A máquina de Mealy é uma 6-tupla (Q, Σ, Γ, δ, λ, q0) onde:
        - Q: é um conjunto finito de estados.
        - Σ: é um conjunto finito de símbolos, o alfabeto de entrada.
        - Γ: é um conjunto finito de símbolos, o alfabeto de saída.
        - δ: é a função de transição de estados (Q × Σ → Q).
        - λ: é a função de saída (Q × Σ → Γ).
        - q0: é o estado inicial, um elemento de Q.
    """

    def __init__(
        self,
        Q: set[str],
        Σ: set[str],
        Γ: set[str],
        δ: dict[tuple[str, str], str],
        λ: dict[tuple[str, str], str],
        q0: str,
    ):
        """
        Inicializa e valida o transdutor finito com os componentes da máquina de Mealy.

        Args:
            Q (set[str]): O conjunto de estados.
            Σ (set[str]): O alfabeto de entrada.
            Γ (set[str]): O alfabeto de saída.
            δ (dict): A função de transição, mapeando (estado, símbolo_entrada) -> proximo_estado.
            λ (dict): A função de saída, mapeando (estado, símbolo_entrada) -> símbolo_saída.
            q0 (str): O estado inicial.
        
        Raises:
            ValueError: Se a definição da máquina for inconsistente (e.g., estado inicial
                        inválido, funções de transição/saída inconsistentes, ou uso de
                        estados/símbolos não definidos nos alfabetos).
        """
        # --- Validação da Definição da Máquina ---
        if q0 not in Q:
            raise ValueError("O estado inicial q0 deve pertencer ao conjunto de estados Q.")

        # Para uma Máquina de Mealy, as funções de transição e saída devem ser definidas
        # para o mesmo conjunto de pares (estado, símbolo).
        if δ.keys() != λ.keys():
            raise ValueError("As chaves das funções de transição (δ) e saída (λ) devem ser idênticas.")
        
        # Valida as regras da função de transição (δ)
        for (estado, simbolo), estado_seguinte in δ.items():
            if estado not in Q:
                raise ValueError(f"O estado '{estado}' na função de transição não pertence ao conjunto de estados Q.")
            if simbolo not in Σ:
                raise ValueError(f"O símbolo '{simbolo}' na função de transição não pertence ao alfabeto de entrada Σ.")
            if estado_seguinte not in Q:
                raise ValueError(f"O estado de destino '{estado_seguinte}' não pertence ao conjunto de estados Q.")
        
        # Valida os resultados da função de saída (λ)
        for (estado, simbolo), simbolo_saida in λ.items():
            if simbolo_saida not in Γ:
                raise ValueError(f"O símbolo de saída '{simbolo_saida}' não pertence ao alfabeto de saída Γ.")

        # --- Atribuição dos Componentes ---
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
            cadeia (str): A cadeia de entrada a ser processada.

        Returns:
            str: A cadeia de saída gerada pelo transdutor.

        Raises:
            ValueError: Se a cadeia contiver um símbolo que não pertence ao alfabeto de entrada,
                        ou se uma regra de transição/saída não for definida para um par
                        (estado, símbolo) encontrado.
        """
        resultado = []
        estado_atual = self.estado_inicial
        
        # Itera sobre cada símbolo da cadeia de entrada
        for simbolo in cadeia:
            # Valida se o símbolo pertence ao alfabeto de entrada
            if simbolo not in self.alfabeto_entrada:
                raise ValueError(f"Símbolo '{simbolo}' na cadeia de entrada não pertence ao alfabeto de entrada Σ.")

            tupla_transicao = (estado_atual, simbolo)

            # Verifica se existe uma regra definida para o estado e símbolo atuais
            if tupla_transicao not in self.funcao_transicao:
                raise ValueError(f"Regra de transição/saída não definida para o estado '{estado_atual}' com o símbolo '{simbolo}'.")

            # Como a regra existe, acessa diretamente os dicionários para obter a saída e o próximo estado
            saida = self.funcao_saida[tupla_transicao]
            estado_proximo = self.funcao_transicao[tupla_transicao]

            # Adiciona o símbolo de saída ao resultado e atualiza o estado
            resultado.append(saida)
            estado_atual = estado_proximo

        return ''.join(resultado)
