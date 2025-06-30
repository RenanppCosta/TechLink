import os
import subprocess
import sys
import platform

def run_command(command, shell=True):
    result = subprocess.run(command, shell=shell)
    if result.returncode != 0:
        print(f"Erro ao executar: {command}")
        sys.exit(result.returncode)

def main():
    venv_path = os.path.join(os.getcwd(), 'venv')
    if not os.path.isdir(venv_path):
        print("Criando ambiente virtual...")
        run_command(f"{sys.executable} -m venv venv")
    
    # Remover o banco de dados SQLite se existir
    db_path = os.path.join(os.getcwd(), 'db.sqlite3')
    if os.path.exists(db_path):
        print("Removendo banco de dados existente...")
        os.remove(db_path)



    is_windows = platform.system() == "Windows"
    activate = os.path.join("venv", "Scripts", "activate") if is_windows else "source venv/bin/activate"

    commands = [
        f"{activate} && pip install -r requirements.txt",
        f"{activate} && python manage.py migrate",
        f"{activate} && python manage.py fake_users",
        f"{activate} && python manage.py runserver"
    ]

    for cmd in commands:
        if is_windows:
            run_command(f"cmd /c \"{cmd}\"")
        else:
            run_command(f"/bin/bash -c '{cmd}'")

if __name__ == "__main__":
    main()
