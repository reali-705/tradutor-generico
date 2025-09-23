import sys
import subprocess
import shutil
from pathlib import Path

def clean_project(*args):
    """
    Remove arquivos de cache do projeto.

    Se a flag '--all' ou '-a' for fornecida, também remove todos os
    arquivos .txt dos diretórios 'data/input' e 'data/output'.

    Args:
        *args: Argumentos adicionais passados pela linha de comando.
    """
    print("Limpando arquivos de cache...")
    # Itera por todos os subdiretórios a partir da raiz do projeto
    for path in Path('.').rglob('__pycache__'):
        if path.is_dir():
            print(f"Removendo diretório: {path}")
            shutil.rmtree(path)
    
    for path in Path('.').rglob('*.pyc'):
        if path.is_file():
            print(f"Removendo arquivo: {path}")
            path.unlink()
    print("Limpeza de cache concluída.")

    # Verifica se a flag para limpeza total foi passada
    if "--all" in args or "-a" in args:
        print("\nOpção '--all' detectada. Limpando arquivos de dados (.txt)...")
        data_path = Path('./data')
        if data_path.exists():
            files_removed = 0
            # Itera por todos os arquivos .txt dentro do diretório 'data'
            for txt_file in data_path.rglob('*.txt'):
                if txt_file.is_file():
                    print(f"Removendo arquivo de dados: {txt_file}")
                    txt_file.unlink()
                    files_removed += 1
            
            if files_removed > 0:
                print(f"Limpeza de dados concluída. {files_removed} arquivo(s) removido(s).")
            else:
                print("Nenhum arquivo .txt encontrado no diretório 'data'.")
        else:
            print("Diretório 'data' não encontrado. Pulando limpeza de dados.")

# Mapeia um nome amigável para o comando ou função
TASKS = {
    "main": ["python", "main.py"],
    # Adicionada a tarefa 'test' para rodar a suíte pytest
    "test": ["pytest", "-v"],
    # Mantidos os testes antigos como 'demo'
    "demo_dna_p": ["python", "-m", "tests.dna_pseudoaleatorio"],
    "demo_dna_a": ["python", "-m", "tests.dna_aleatorio"],
    "demo_ribossomo": ["python", "-m", "tests.ribossomo"],
    "clean": clean_project,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: Nenhuma tarefa especificada.")
        print("Tarefas disponíveis:", ", ".join(TASKS.keys()))
        print("\nExemplo de uso:")
        print("  python run.py main -a 100")
        print("  python run.py test")
        print("  python run.py clean --all")
        sys.exit(1)

    task_name = sys.argv[1]
    extra_args = sys.argv[2:]

    task = TASKS.get(task_name)

    if task:
        if callable(task):
            # Executa a função, passando os argumentos extras para ela
            task(*extra_args)
        else:
            # Anexa os argumentos extras ao comando a ser executado
            command = task + extra_args
            print(f"Executando tarefa '{task_name}': {' '.join(command)}")
            try:
                subprocess.run(command, check=True)
            except FileNotFoundError:
                print(f"\nErro: O comando '{command[0]}' não foi encontrado.")
                if command[0] == "pytest":
                    print("Parece que o pytest não está instalado. Tente 'pip install pytest'.")
                sys.exit(1)
            except subprocess.CalledProcessError:
                print(f"\nA tarefa '{task_name}' encontrou um erro.")
    else:
        print(f"Erro: Tarefa '{task_name}' não encontrada.")
        print("Tarefas disponíveis:", ", ".join(TASKS.keys()))
        sys.exit(1)