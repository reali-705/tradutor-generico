# Tradutor Genético: DNA para Proteínas com Teoria dos Autômatos

## 📖 Sobre o Projeto
Este projeto foi desenvolvido para a disciplina de Linguagens Formais e Autômatos e tem como objetivo aplicar os conceitos da Teoria dos Autômatos para resolver um problema de bioinformática: a tradução de sequências de DNA em proteínas.

O sistema é implementado como um pipeline de dois estágios, utilizando um **Transdutor Finito** (Máquina de Mealy) para a transcrição de DNA em RNA e um **Autômato de Pilha** para a validação sintática e tradução do RNA em uma cadeia de aminoácidos.

## ✨ Funcionalidades
- **Geração de DNA:** Scripts de teste para gerar DNA pseudoaleatório com estrutura de gene válida.
- **Transcrição DNA → RNA:** Converte sequências de DNA para suas contrapartes em RNA mensageiro usando um Transdutor Finito.
- **Tradução RNA → Proteína:** Identifica regiões codificantes em uma fita de RNA (delimitadas por códons de início e parada) e as traduz para as cadeias de aminoácidos correspondentes usando um Autômato de Pilha.
- **Processamento em Lote:** Capaz de ler um arquivo `.txt` contendo múltiplos genes e processá-los sequencialmente.
- **Geração de Arquivos:** Salva os resultados intermediários (RNA) e finais (proteínas) em arquivos de saída para fácil verificação.

## 📂 Estrutura do Projeto
O projeto utiliza uma estrutura de pacotes Python para garantir modularidade e legibilidade.

```
tradutor-genetico/
├── data/
│   ├── input/
│   └── output/
│
├── src/
│   ├── __init__.py
│   ├── automata/
│   │   ├── __init__.py
│   │   ├── transdutor_finito.py
│   │   └── transdutor_pilha.py
│   │
│   ├── tabela_codons.py
│   └── utils.py
│
├── tests/
│   └── dna_pseudoaleatorio.py
│
├── main.py
├── run.py
└── README.md
```

## ⚙️ Arquitetura do Sistema
O fluxo de dados do sistema é modelado como um pipeline de dois autômatos que operam em sequência.

### Módulo 1: Transcrição (Transdutor Finito)
- **Modelo:** `src/automata/transdutor_finito.py`
- **Entrada:** Cadeia de DNA.
- **Processo:** Utiliza uma Máquina de Mealy para realizar a substituição 1-para-1 de cada base do DNA (`A`, `T`, `C`, `G`) para a base complementar em RNA (`U`, `A`, `G`, `C`).
- **Saída:** Cadeia de RNA mensageiro.

### Módulo 2: Tradução (Autômato de Pilha)
- **Modelo:** `src/automata/transdutor_pilha.py`
- **Entrada:** Cadeia de RNA.
- **Processo:** Simula um autômato de pilha para reconhecer a linguagem livre de contexto que define a estrutura de um gene (`INÍCIO-CORPO-FIM`). A pilha é utilizada para validar a estrutura e construir a cadeia de aminoácidos.
- **Saída:** Cadeia de aminoácidos (proteína) e a localização do gene no RNA.

## 🚀 Como Executar
### Pré-requisitos
- Python 3.8 ou superior.

### Passos
1. **Clone o repositório:**
   ```bash
   git clone [URL_DO_SEU_REPOSITORIO]
   cd tradutor-genetico
   ```

2. **Prepare o arquivo de entrada (Opcional):**
   - Adicione as sequências de DNA que você deseja traduzir no arquivo `data/input/dna_genes.txt` (crie-o se não existir).
   - **Importante:** Coloque apenas **uma sequência de DNA por linha.**

3. **Execute o script principal:**
   - O projeto utiliza um script `run.py` para facilitar a execução. Abra o terminal na raiz do projeto e use:
   ```bash
   # Para executar a aplicação principal
   python run.py main

   # Para executar o teste de geração de DNA com 50 códons
   python run.py test_dna -c 50

   # Para limpar os arquivos de cache (__pycache__)
   python run.py clean
   ```

4. **Verifique os resultados:**
   - Os arquivos de saída serão criados (ou sobrescritos) no diretório `data/output/`.

## 👥 Equipe e Divisão de Tarefas
O projeto foi desenvolvido pela seguinte equipe:

- **Desenvolvimento do Código:**
    - Alessandro
    - Gian

- **Elaboração do Artigo Científico:**
    - Jhonata