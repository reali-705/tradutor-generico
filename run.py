import sys
import subprocess
import shutil
from pathlib import Path

def clean_project():
    """
    Remove todos os diretórios __pycache__ e arquivos .pyc do projeto.
    """
    print("Limpando o projeto...")
    # Itera por todos os subdiretórios a partir da raiz do projeto
    for path in Path('.').rglob('__pycache__'):
        if path.is_dir():
            print(f"Removendo diretório: {path}")
            # shutil.rmtree remove um diretório e todo o seu conteúdo
            shutil.rmtree(path)
    
    for path in Path('.').rglob('*.pyc'):
        if path.is_file():
            print(f"Removendo arquivo: {path}")
            # path.unlink() remove um arquivo
            path.unlink()
    print("Limpeza concluída.")

# Mapeia um nome amigável para o comando ou função
TASKS = {
    "main": ["python", "-m", "main"],
    "test_dna_p": ["python", "-m", "tests.dna_pseudoaleatorio"],
    "test_dna_a": ["python", "-m", "tests.dna_aleatorio"],
    "test_ribossomo": ["python", "-m", "tests.ribossomo"],
    "clean": clean_project,  # A tarefa "clean" agora chama a função diretamente
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: Nenhuma tarefa especificada.")
        print("Tarefas disponíveis:", ", ".join(TASKS.keys()))
        sys.exit(1)

    task_name = sys.argv[1]
    # NOVIDADE: Pega todos os argumentos extras passados após o nome da tarefa
    extra_args = sys.argv[2:]

    task = TASKS.get(task_name)

    if task:
        if callable(task):
            # Executa a função, passando os argumentos extras para ela (se houver)
            task(*extra_args)
        else:
            # NOVIDADE: Anexa os argumentos extras ao comando a ser executado
            command = task + extra_args
            print(f"Executando tarefa '{task_name}': {' '.join(command)}")
            subprocess.run(command)
    else:
        print(f"Erro: Tarefa '{task_name}' não encontrada.")
        print("Tarefas disponíveis:", ", ".join(TASKS.keys()))
        sys.exit(1)