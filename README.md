# Tradutor Genético: DNA para Proteínas com Teoria dos Autômatos
## 📖 Sobre o Projeto
Este projeto foi desenvolvido para a disciplina de [Nome da Disciplina] e tem como objetivo aplicar os conceitos da Teoria dos Autômatos e Linguagens Formais para resolver um problema de bioinformática: a tradução de sequências de DNA em proteínas.

O sistema é implementado como um pipeline de dois estágios, utilizando um **Transdutor Finito** para a transcrição de DNA em RNA e um **Autômato de Pilha** (atuando como Transdutor) para a validação sintática e tradução do RNA em uma cadeia de aminoácidos.

## ✨ Funcionalidades
- **Transcrição de DNA para RNA:** Converte sequências de DNA (`A`, `T`, `C`, `G`) para suas contrapartes em RNA mensageiro (`U`, `A`, `G`, `C`).

- **Validação Sintática:** Verifica se a molécula de RNA possui a estrutura gramatical correta para uma proteína (códon de início `AUG`, corpo e códon de parada).

- **Tradução para Proteínas:** Traduz o RNA validado em sua correspondente cadeia de aminoácidos, baseando-se na tabela de códons universal.

- **Processamento em Lote:** Capaz de ler um arquivo `.txt` contendo múltiplos genes (um por linha) e processá-los sequencialmente.

- **Geração de Arquivos:** Salva os resultados das transcrições (RNA) e traduções (proteínas) em arquivos de saída para fácil verificação.

## 📂 Estrutura do Projeto
O projeto foi organizado utilizando uma estrutura de pacotes Python para garantir modularidade, legibilidade e escalabilidade.

```
sintese_proteica/
├── data/
│   ├── input/
│   │   └── dna_genes.txt
│   └── output/
│       ├── rna_gerado.txt
│       └── proteina_gerada.txt
│
├── src/
│   ├── __init__.py
│   ├── automata/
│   │   ├── __init__.py
│   │   ├── transdutor_finito.py
│   │   └── transdutor_pilha.py
│   │
│   ├── codon_table.py
│   └── utils.py
│
├── main.py
└── README.md
```

## ⚙️ Arquitetura do Sistema
O fluxo de dados do sistema é modelado como um pipeline de dois autômatos que operam em sequência.

### Módulo 1: Transcrição (Transdutor Finito)
- **Modelo:** `transdutor_finito.py`

- **Entrada:** Cadeia de DNA.

- **Processo:** Utiliza um modelo de autômato finito para validar cada base do DNA (`A`, `T`, `C`, `G`) e realizar a substituição direta para a base correspondente em RNA. A tarefa é de natureza regular, tornando o transdutor finito a ferramenta teórica ideal.

- **Saída:** Cadeia de RNA mensageiro.

### Módulo 2: Validação e Tradução (Transdutor de Pilha)
- **Modelo:** `transdutor_pilha.py`

- **Entrada:** Cadeia de RNA.

- **Processo:** Simula um autômato de pilha para reconhecer a linguagem livre de contexto que define a estrutura de um gene (`INÍCIO-CORPO-FIM`). A pilha é utilizada para controlar a validação e construir a cadeia de aminoácidos.

- **Saída:** Cadeia de aminoácidos (proteína).

## 🚀 Como Executar
### Pré-requisitos
- Python 3.8 ou superior.

### Passos
1. **Clone o repositório:**

```
git clone [URL_DO_SEU_REPOSITORIO]
cd sintese_proteica
```

2. **Prepare o arquivo de entrada:**

- Adicione as sequências de DNA que você deseja traduzir no arquivo `data/input/dna_genes.txt`.

- Importante: Coloque apenas **uma sequência de DNA por linha.**

_Exemplo de_ `dna_genes.txt`:

```
ATGCGCGCGTATATAGG
TACGGCGATTACCGACT
ATGAAATTTGGGTAA
```

3. **Execute o script principal:**

- Abra o terminal na raiz do projeto (`sintese_proteica/`) e execute o seguinte comando:

```
python main.py
```

4. **Verifique os resultados:**
- Os arquivos `rna_gerado.txt` e `proteina_gerada.txt` serão criados (ou sobrescritos) no diretório `data/output/` com os resultados do processamento.

## 👥 Equipe e Divisão de Tarefas
O projeto foi desenvolvido pela seguinte equipe:

- **Desenvolvimento do Código:**
    - Alessandro
    - Gian

- **Elaboração do Artigo Científico:**
    - Jhonata
    - Felipe