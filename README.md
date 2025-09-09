# Tradutor Genético: DNA para Proteínas com Teoria dos Autômatos

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)

## 📖 Sobre o Projeto
Este projeto, desenvolvido para a disciplina de **Linguagens Formais e Autômatos**, demonstra a aplicação prática de conceitos teóricos da ciência da computação para resolver um problema fundamental da bioinformática: a tradução de sequências de DNA em proteínas.

O sistema implementa um pipeline de dois estágios principais:
1.  **Transcrição (DNA → RNA):** Utiliza um **Transdutor Finito (Máquina de Mealy)** para converter uma fita de DNA em sua fita de RNA mensageiro complementar.
2.  **Tradução (RNA → Proteína):** Emprega um **Autômato de Pilha Determinístico** para validar a sintaxe de um gene na fita de RNA e traduzi-lo em uma cadeia de aminoácidos.

## ✨ Funcionalidades Principais
- **Interface de Linha de Comando:** Uma aplicação `main.py` robusta que permite gerar e processar DNA de várias formas.
- **Processamento em Lote:** Capacidade de executar múltiplas tarefas (geração aleatória, pseudoaleatória e leitura de arquivo) em uma única chamada.
- **Geração de DNA:** Scripts para gerar cadeias de DNA aleatórias e pseudoaleatórias (com estrutura de gene).
- **Transcrição e Tradução:** Pipeline completo que converte DNA em RNA e, subsequentemente, em proteínas.
- **Orquestrador de Tarefas:** Um script `run.py` que centraliza a execução da aplicação principal, dos testes e de tarefas de manutenção.
- **Testes Modulares:** Um conjunto de testes de unidade e integração para validar cada componente do sistema.

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
├── main.py               # Ponto de entrada da aplicação principal
├── run.py                # Orquestrador de tarefas do projeto
└── README.md
```

## ⚙️ Arquitetura e Teoria Aplicada

### Módulo 1: Transcrição (Transdutor Finito / Máquina de Mealy)
- **Modelo:** `src/automata/transdutor_finito.py`
- **Propósito:** Converter uma fita de DNA em RNA.
- **Teoria:** Este processo é uma **tradução regular**, pois cada símbolo de entrada (`A`, `T`, `C`, `G`) mapeia diretamente para um único símbolo de saída (`U`, `A`, `G`, `C`) sem a necessidade de memória complexa.

### Módulo 2: Tradução (Autômato de Pilha Determinístico)
- **Modelo:** `src/automata/automato_pilha.py`
- **Propósito:** Validar e traduzir uma fita de RNA em proteínas.
- **Teoria:** A estrutura de um gene pertence a uma **Linguagem Livre de Contexto**.
    - **Linguagem Reconhecida (L):** Fitas de RNA que contêm uma ou mais sequências de genes válidas, definidas pela estrutura `INÍCIO - CORPO - FIM`.
    - **Gramática Livre de Contexto (Simplificada):**
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

O script `run.py` é o ponto de entrada unificado para todas as operações.

### Pré-requisitos
- Python 3.8 ou superior.

### Comandos Disponíveis
Abra o terminal na raiz do projeto e utilize os seguintes comandos:

---
### 1. Executando a Aplicação Principal (`main.py`)

Esta é a forma principal de usar o projeto. Você pode combinar as opções para executar várias tarefas em sequência.

**Comando base:**
```bash
python run.py main [OPÇÕES]
```

**Opções:**
- `-p [N_CODONS]`, `--pseudoaleatorio [N_CODONS]`
  - Gera DNA pseudoaleatório. Se `N_CODONS` não for especificado, usa o valor padrão (1000).
- `-a [N_BASES]`, `--aleatorio [N_BASES]`
  - Gera DNA aleatório. Se `N_BASES` não for especificado, usa o valor padrão (10000).
- `-l <ARQUIVO>`, `--ler-arquivo <ARQUIVO>`
  - Lê uma cadeia de DNA de um arquivo. O script é inteligente e consegue encontrar o arquivo mesmo que você omita a extensão `.txt` ou o caminho `data/input/`.

**Exemplos de Uso:**

- **Gerar DNA pseudoaleatório com o tamanho padrão:**
  ```bash
  python run.py main -p
  ```

- **Gerar DNA aleatório com 500 bases:**
  ```bash
  python run.py main -a 500
  ```

- **Ler um arquivo de DNA (várias formas):**
  ```bash
  # Forma simples
  python run.py main -l meu_dna
  # Com extensão
  python run.py main -l meu_dna.txt
  # Com caminho relativo
  python run.py main -l data/input/meu_dna.txt
  ```

- **Executar múltiplas tarefas em uma única chamada:**
  *(O programa executará na ordem: pseudoaleatório, aleatório, leitura de arquivo)*
  ```bash
  python run.py main -p 50 -a 200 -l meu_dna
  ```

---
### 2. Executando os Testes Individuais

Para validar componentes específicos do sistema.

- **Teste de Geração de DNA Aleatório:**
  ```bash
  python run.py test_dna_a --bases 100 --keep-files
  ```
- **Teste de Geração de DNA Pseudoaleatório:**
  ```bash
  python run.py test_dna_p --codons 50 --keep-files
  ```
- **Teste de Unidade do Ribossomo (Autômato de Pilha):**
  ```bash
  python run.py test_ribossomo
  ```

---
### 3. Limpeza do Projeto

Para remover arquivos gerados.

- **Limpeza Padrão (apenas cache do Python):**
  ```bash
  python run.py clean
  ```
- **Limpeza Completa (cache + todos os arquivos `.txt` em `data/`):**
  ```bash
  python run.py clean --all
  ```
  ou
  ```bash
  python run.py clean -a
  ```

## 👥 Equipe e Divisão de Tarefas
O projeto foi desenvolvido pela seguinte equipe:

- **Desenvolvimento do Código:**
    - [Alessandro Reali Lopes Silva](https://github.com/reali-705)
    - [Gian Victor Gonçalves Figueiredo](https://github.com/Gian-Figueiredo)

- **Elaboração do Artigo Científico:**
    - [Jhonata Bezerra Figueiredo](https://github.com/Jhonatabz)
    - [Felipe Lisboa Brasil](https://github.com/FelipeBrasill)