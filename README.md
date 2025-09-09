# Tradutor Genético: DNA para Proteínas com Teoria dos Autômatos

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)

## 📖 Sobre o Projeto
Este projeto, desenvolvido para a disciplina de **Linguagens Formais e Autômatos**, demonstra a aplicação prática de conceitos teóricos da ciência da computação para resolver um problema fundamental da bioinformática: a tradução de sequências de DNA em proteínas.

O sistema implementa um pipeline de dois estágios principais:
1.  **Transcrição (DNA → RNA):** Utiliza um **Transdutor Finito (Máquina de Mealy)** para converter uma fita de DNA em sua fita de RNA mensageiro complementar.
2.  **Tradução (RNA → Proteína):** Emprega um **Autômato de Pilha Determinístico** para validar a sintaxe de um gene na fita de RNA e traduzi-lo em uma cadeia de aminoácidos.

## ✨ Funcionalidades Principais
- **Geração de DNA:** Scripts para gerar cadeias de DNA aleatórias e pseudoaleatórias (com estrutura de gene).
- **Transcrição DNA → RNA:** Converte DNA em RNA mensageiro usando um Transdutor Finito.
- **Tradução RNA → Proteína:** Identifica genes (delimitados por códons de início e parada), valida sua estrutura e os traduz em proteínas usando um Autômato de Pilha.
- **Testes Modulares:** Um conjunto de testes de unidade e integração para validar cada componente do sistema de forma isolada e em conjunto.
- **Orquestrador de Tarefas:** Um script `run.py` centraliza a execução de todas as tarefas do projeto, desde os testes até a limpeza do ambiente.

## 📂 Estrutura do Projeto
```
tradutor-genetico/
├── data/                 # Diretório para arquivos de entrada e saída
│   ├── input/
│   └── output/
│
├── src/                  # Código-fonte principal da aplicação
│   ├── __init__.py       # Funções "fábrica" que montam os autômatos
│   ├── automata/         # Implementações das classes de autômatos
│   │   ├── transdutor_finito.py
│   │   └── automato_pilha.py
│   ├── tabela_codons.py  # Mapeamento de códons para aminoácidos
│   └── utils.py          # Funções utilitárias (geração de DNA, I/O)
│
├── tests/                # Scripts de teste
│   ├── _modelo_testes.py # Modelo genérico para testes de fluxo
│   ├── dna_aleatorio.py
│   ├── dna_pseudoaleatorio.py
│   └── ribossomo.py      # Teste de unidade para o autômato de pilha
│
├── main.py               # (Futuro) Ponto de entrada da aplicação principal
├── run.py                # Orquestrador de tarefas do projeto
└── README.md
```

## ⚙️ Arquitetura e Teoria Aplicada

### Módulo 1: Transcrição (Transdutor Finito / Máquina de Mealy)
- **Modelo:** `src/automata/transdutor_finito.py`
- **Propósito:** Converter uma fita de DNA em RNA.
- **Teoria:** Este processo é uma **tradução regular**, pois cada símbolo de entrada (`A`, `T`, `C`, `G`) mapeia diretamente para um único símbolo de saída (`U`, `A`, `G`, `C`) sem a necessidade de memória complexa. Uma Máquina de Mealy é o modelo perfeito para essa tarefa, pois ela produz uma saída para cada transição de estado.

### Módulo 2: Tradução (Autômato de Pilha Determinístico)
- **Modelo:** `src/automata/automato_pilha.py`
- **Propósito:** Validar e traduzir uma fita de RNA em proteínas.
- **Teoria:** A estrutura de um gene é mais complexa e não pode ser reconhecida por um autômato finito. Ela pertence a uma **Linguagem Livre de Contexto**.
    - **Linguagem Reconhecida (L):** A linguagem `L` reconhecida pelo autômato pode ser descrita como fitas de RNA que contêm uma ou mais sequências de genes válidas. Um gene válido é definido pela estrutura `INÍCIO - CORPO - FIM`.
    - **Gramática Livre de Contexto (Simplificada):** Uma gramática `G` que gera uma versão simplificada de um gene (um códon de início, um corpo e um códon de fim) seria:
      ```
      G = (V, Σ, R, S)
      V = {S, Gene, Corpo, Codon, Base}  (Variáveis)
      Σ = {A, U, C, G}                   (Terminais)
      S -> Gene | Gene S                 (Ponto de partida: um ou mais genes)
      Gene -> 'AUG' Corpo StopCodon      (Estrutura do gene)
      Corpo -> Codon Corpo | ε           (O corpo pode ter zero ou mais códons)
      Codon -> Base Base Base            (Um códon tem 3 bases)
      Base -> 'A' | 'U' | 'C' | 'G'
      StopCodon -> 'UAA' | 'UAG' | 'UGA'
      ```
- **Implementação:** O autômato de pilha (`Automato_Pilha_Deterministico_ε`) utiliza sua pilha para "construir" a cadeia de aminoácidos à medida que valida a estrutura do gene, empilhando o nome de cada aminoácido correspondente a um códon lido.

## 🚀 Como Executar o Projeto

O script `run.py` é a maneira recomendada para interagir com o projeto. Ele oferece uma interface de linha de comando simples para executar os testes e outras tarefas.

### Pré-requisitos
- Python 3.8 ou superior.

### Comandos Disponíveis
Abra o terminal na raiz do projeto e utilize os seguintes comandos:

---
#### 1. Teste de Geração de DNA Aleatório
Testa o fluxo de geração de DNA aleatório e sua transcrição para RNA.
```bash
python run.py test_dna_a [OPÇÕES]
```
- **Opções:**
  - `-b <NÚMERO>` ou `--bases <NÚMERO>`: Define o número de bases a serem geradas (padrão: 50).
  - `-k` ou `--keep-files`: Mantém os arquivos de saída gerados em `data/`.
- **Exemplo:**
  ```bash
  # Gera e testa uma cadeia com 200 bases
  python run.py test_dna_a -b 200
  ```

---
#### 2. Teste de Geração de DNA Pseudoaleatório
Testa o fluxo de geração de DNA com estrutura de gene (início-corpo-fim) e sua transcrição.
```bash
python run.py test_dna_p [OPÇÕES]
```
- **Opções:**
  - `-c <NÚMERO>` ou `--codons <NÚMERO>`: Define o número de códons no corpo do gene (padrão: 10).
  - `-k` ou `--keep-files`: Mantém os arquivos de saída.
- **Exemplo:**
  ```bash
  # Gera e testa um gene com 30 códons e mantém os arquivos
  python run.py test_dna_p -c 30 -k
  ```

---
#### 3. Teste do Ribossomo (Autômato de Pilha)
Executa um teste de unidade no autômato de pilha, validando a tradução de RNA para proteína com múltiplos casos de teste (sucesso e falha).
```bash
python run.py test_ribossomo
```
*(Este teste não possui opções de linha de comando)*

---
#### 4. Execução da Aplicação Principal
*(Nota: O `main.py` é um trabalho em andamento e será o ponto de entrada para processar arquivos de DNA customizados.)*
```bash
python run.py main
```

---
#### 5. Limpeza do Projeto
Remove todos os diretórios `__pycache__` e arquivos `.pyc` gerados pelo Python.
```bash
python run.py clean
```

### Tratamento de Erros
O script `run.py` possui tratamento de erros básico. Se uma tarefa inválida for fornecida, ele informará o erro e listará todas as tarefas disponíveis.

## 👥 Equipe e Divisão de Tarefas
O projeto foi desenvolvido pela seguinte equipe:

- **Desenvolvimento do Código:**
    - [Alessandro Reali Lopes Silva](https://github.com/reali-705)
    - [Gian Victor Gonçalves Figueiredo](https://github.com/Gian-Figueiredo)

- **Elaboração do Artigo Científico:**
    - [Jhonata Bezerra Figueiredo](https://github.com/Jhonatabz)
    - [Felipe Lisboa Brasil](https://github.com/FelipeBrasill)