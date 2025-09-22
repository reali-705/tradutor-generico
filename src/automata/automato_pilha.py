class Automato_Pilha:
    """
    Representa um Autômato de Pilha (AP), uma máquina de estados finitos
    com uma pilha como memória auxiliar.

    Esta classe implementa a lógica para validar a definição do autômato e
    simular seu comportamento em uma cadeia de entrada.
    """
    def __init__(self,
        Q: set[str],                                            # conjunto de estados
        Σ: set[str],                                            # alfabeto de entrada
        Γ: set[str],                                            # alfabeto da pilha
        δ: dict[tuple[str, str, str], tuple[str, list[str]]],   # função de transição
        q0: str,                                                # estado inicial
        Z0: str,                                                # símbolo inicial da pilha
        F: set[str]                                             # estados finais
    ):
        """
        Inicializa e valida a definição do Autômato de Pilha.

        Args:
            Q: Um conjunto de strings representando todos os estados possíveis.
            Σ: Um conjunto de strings representando o alfabeto de entrada.
            Γ: Um conjunto de strings representando o alfabeto da pilha.
            δ: Um dicionário que mapeia uma 3-tupla (estado, entrada, topo_pilha)
               para uma 2-tupla (novo_estado, [simbolos_a_empilhar]).
            q0: O estado inicial do autômato.
            Z0: O símbolo que estará na pilha no início da computação.
            F: Um conjunto de strings representando os estados de aceitação/finais.

        Raises:
            TypeError: Se qualquer componente da definição do autômato for inválido
                       (ex: um estado não pertence a Q, um símbolo não pertence a Σ ou Γ).
        """
        if q0 not in Q:
            raise TypeError("Estado inicial não pertence ao conjunto dos estados")
        
        if not F.issubset(Q):
            raise TypeError("Conjunto dos estados finais não é subconjunto dos estados")
        
        if (Z0 not in Γ):
            raise TypeError("Símbolo inicial da pilha não pertence ao alfabeto da pilha")
        
        for (estado_origem, simbolo_entrada, simbolo_pilha), (estado_destino, simbolos_pilha) in δ.items():
            trinca = (estado_origem, simbolo_entrada, simbolo_pilha)
            dupla = (estado_destino, simbolos_pilha)
            if estado_origem not in Q:
                raise TypeError(f"A transição {trinca} -> {dupla}. {estado_origem} não pertence ao conjunto de estados")

            if simbolo_entrada not in Σ:
                raise TypeError(f"A transição {trinca} -> {dupla}. {simbolo_entrada} não pertence ao alfabeto de entrada")

            if simbolo_pilha not in Γ:
                raise TypeError(f"A transição {trinca} -> {dupla}. {simbolo_pilha} não pertence ao alfabeto da pilha")
            
            if estado_destino not in Q:
                raise TypeError(f"A transição {trinca} -> {dupla}. {estado_destino} não pertence ao conjunto de estados")
            
            if not set(simbolos_pilha).issubset(Γ):
                raise TypeError(f"A transição {trinca} -> {dupla}. {simbolos_pilha} não pertence(m) ao alfabeto da pilha")

        self.estados = Q
        self.alfabeto_entrada = Σ
        self.alfabeto_pilha = Γ
        self.transicoes = δ
        self.estado_inicial = q0
        self.estado_inicial_pilha = Z0
        self.estados_finais = F

    def _transitar(self, trinca: tuple[str, str, str], pilha: list[str]) -> str:
        """
        Executa uma única transição, atualizando a pilha e retornando o novo estado.

        Args:
            trinca: A tupla (estado, entrada, topo_pilha) que acionou a transição.
            pilha: A pilha atual do autômato, que será modificada.

        Returns:
            O novo estado do autômato após a transição.
        """
        novo_estado, novos_simbolos_pilha = self.transicoes[trinca]
        if novos_simbolos_pilha:
            pilha.extend(novos_simbolos_pilha)
        return novo_estado

    def validar(self, cadeia: str) -> bool:
        """
        Simula o autômato como um reconhecedor para validar se a cadeia é aceita.

        Args:
            cadeia: A string de entrada a ser validada.

        Returns:
            True se a cadeia for aceita pelo autômato, False caso contrário.
        """
        estado_atual = self.estado_inicial
        pilha = [self.estado_inicial_pilha] 
        
        indice_cadeia = 0
        while indice_cadeia < len(cadeia):
            simbolo_entrada = cadeia[indice_cadeia]
            if simbolo_entrada not in self.alfabeto_entrada:
                return False # Símbolo inválido

            # Estratégia de leitura destrutiva: remove o topo para inspecioná-lo.
            topo_pilha = pilha.pop() if pilha else None

            trinca_com_entrada = (estado_atual, simbolo_entrada, topo_pilha)
            trinca_sem_entrada = (estado_atual, None, topo_pilha)

            if trinca_com_entrada in self.transicoes:
                # Prioriza consumir um símbolo da entrada se possível.
                estado_atual = self._transitar(trinca_com_entrada, pilha)
                indice_cadeia += 1 # Avança na cadeia de entrada.
            
            elif trinca_sem_entrada in self.transicoes:
                # Se não, tenta uma transição em vazio (ε).
                estado_atual = self._transitar(trinca_sem_entrada, pilha)
                # Não incrementa o indice_cadeia, pois não consumiu entrada.
            
            else:
                # Se nenhuma transição foi encontrada, restaura a pilha e rejeita.
                pilha.append(topo_pilha) if topo_pilha else None
                return False

        # Após consumir a cadeia, processa transições ε restantes.
        while True:
            topo_pilha = pilha.pop() if pilha else None
            trinca_sem_entrada = (estado_atual, None, topo_pilha)
            
            if trinca_sem_entrada in self.transicoes:
                estado_atual = self._transitar(trinca_sem_entrada, pilha)
            else:
                # Se não há mais transições ε, restaura a pilha e para.
                pilha.append(topo_pilha) if topo_pilha else None
                break 

        # A cadeia é válida se o autômato parou em um estado final.
        return estado_atual in self.estados_finais

    def transcrever_pilha(self, cadeia: str) -> list[str]:
        """
        Simula o autômato como um transdutor/parser, retornando o estado final da pilha.

        Diferente de `validar`, este método não rejeita a cadeia se uma transição
        não for encontrada; em vez disso, ele ignora o símbolo de entrada e continua,
        permitindo o processamento de "lixo" entre sequências válidas.

        Args:
            cadeia: A string de entrada a ser processada.

        Returns:
            Uma lista de strings representando o conteúdo final da pilha.
        
        Raises:
            RuntimeError: Se o autômato travar em um estado não final sem
                          mais transições em vazio para processar.
        """
        estado_atual = self.estado_inicial
        pilha = [self.estado_inicial_pilha]
        
        indice_cadeia = 0
        while indice_cadeia < len(cadeia):
            simbolo_entrada = cadeia[indice_cadeia]
            if simbolo_entrada not in self.alfabeto_entrada:
                raise ValueError(f"Símbolo '{simbolo_entrada}' na cadeia de entrada não pertence ao alfabeto de entrada Σ.")
            
            # Estratégia de leitura destrutiva.
            topo_pilha = pilha.pop() if pilha else None

            trinca_com_entrada = (estado_atual, simbolo_entrada, topo_pilha)
            trinca_sem_entrada = (estado_atual, None, topo_pilha)

            if trinca_com_entrada in self.transicoes:
                estado_atual = self._transitar(trinca_com_entrada, pilha)
                indice_cadeia += 1
            
            elif trinca_sem_entrada in self.transicoes:
                estado_atual = self._transitar(trinca_sem_entrada, pilha)
            
            else:
                # Se não há transição, restaura a pilha e ignora o símbolo de entrada.
                pilha.append(topo_pilha) if topo_pilha else None
                indice_cadeia += 1

        # Após consumir a cadeia, processa transições ε (ex: rollback/limpeza).
        while estado_atual not in self.estados_finais:
            topo_pilha = pilha.pop() if pilha else None
            trinca_sem_entrada = (estado_atual, None, topo_pilha)
            
            if trinca_sem_entrada in self.transicoes:
                estado_atual = self._transitar(trinca_sem_entrada, pilha)
            else:
                # Restaura a pilha antes de levantar o erro.
                pilha.append(topo_pilha) if topo_pilha else None
                raise RuntimeError(f"Autômato travado no estado '{estado_atual}' sem mais transições ε para chegar a um estado final.")
            
        return pilha