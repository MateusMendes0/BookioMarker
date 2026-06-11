import os
import subprocess
import django

print("=== Iniciando Setup do Container ===")

# Executa as migrações do banco de dados
print("Rodando migrações...")
subprocess.run(["python", "manage.py", "migrate", "--noinput"], check=True)

# Carrega os dados iniciais (fixtures)
print("Carregando fixtures...")
subprocess.run(["python", "manage.py", "loaddata", "catalogo_data.json"], check=True)

# Cria o superusuário se não existir
print("Configurando superusuário...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = "mateus"
password = "1234"
email = "mateus@gmail.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superusuário '{username}' criado com sucesso!")
else:
    print(f"Superusuário '{username}' já existe.")

print("=== Iniciando o servidor de desenvolvimento ===")
# Inicia o servidor do Django na porta 8000 exposta para todos os IPs da rede docker
subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])
