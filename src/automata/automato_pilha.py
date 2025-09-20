class Automato_Pilha_Deterministico_ε:
    def __init__(self,
        Q: set[str],                                            # conjunto de estados
        Σ: set[str],                                            # alfabeto de entrada
        Γ: set[str],                                            # alfabeto da pilha
        δ: dict[tuple[str, str, str], tuple[str, list[str]]],   # função de transição
        q0: str,                                                # estado inicial
        Z0: str,                                                # símbolo inicial da pilha
        F: set[str]                                             # estados finais
    ):
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
        novo_estado, novos_simbolos_pilha = self.transicoes[trinca]
        if novos_simbolos_pilha:
            pilha.extend(novos_simbolos_pilha[::-1])
        return novo_estado

    def validar(self, cadeia: str) -> bool:
        estado_atual = self.estado_inicial
        pilha = [self.estado_inicial_pilha] 
        
        indice_cadeia = 0
        while indice_cadeia < len(cadeia):
            simbolo_entrada = cadeia[indice_cadeia]
            if simbolo_entrada not in self.alfabeto_entrada:
                return False # Símbolo inválido

            topo_pilha = pilha[-1] if pilha else None

            trinca_com_entrada = (estado_atual, simbolo_entrada, topo_pilha)
            trinca_sem_entrada = (estado_atual, None, topo_pilha)

            if trinca_com_entrada in self.transicoes:
                # Prioriza consumir um símbolo da entrada se possível
                pilha.pop()
                estado_atual = self._transitar(trinca_com_entrada, pilha)
                indice_cadeia += 1 # Avança na cadeia de entrada
            
            elif trinca_sem_entrada in self.transicoes:
                # Se não há transição para a entrada, tenta uma transição ε
                pilha.pop()
                estado_atual = self._transitar(trinca_sem_entrada, pilha)
                # Não incrementa o indice_cadeia, pois não consumiu entrada
            
            else:
                # Nenhuma transição possível, a cadeia é rejeitada
                return False

        # Após consumir toda a cadeia, processa as transições ε restantes
        while True:
            topo_pilha = pilha[-1] if pilha else None
            # Apenas transições sem entrada (ε) são possíveis aqui
            trinca_sem_entrada = (estado_atual, None, topo_pilha)
            
            if trinca_sem_entrada in self.transicoes:
                pilha.pop()
                estado_atual = self._transitar(trinca_sem_entrada, pilha)
            else:
                break # Sai do loop se não houver mais transições ε

        # A cadeia é válida se, no final, o estado atual for um estado final
        # E a pilha estiver vazia (aceitação por estado final E pilha vazia)
        # Ou apenas por estado final, dependendo da definição. Vamos usar apenas estado final.
        return estado_atual in self.estados_finais
