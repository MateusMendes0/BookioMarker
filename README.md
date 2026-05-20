# BookioMarker

O **BookioMarker** é um organizador e rastreador pessoal de leitura desenvolvido em Python com o framework Django. Ele foi projetado para ajudar os leitores a acompanharem suas leituras, registrarem o progresso de páginas lidas, avaliarem livros e gerenciarem suas metas literárias anuais.

O projeto utiliza o **Django Unfold** para fornecer uma interface de administração moderna, limpa e responsiva.

---

## 🚀 Funcionalidades Principais

O sistema é dividido em três aplicações principais Django localizadas no diretório `apps/`:

### 1. Usuários (`apps.usuarios`)
*   **Perfis Personalizados**: Extensão do modelo padrão do Django (`AbstractUser`) para incluir informações adicionais como `nickname`, gênero, país de origem, biografia e foto.
*   **Estatísticas de Leitura**: Acompanhamento automático de estatísticas de leitura do usuário, incluindo total de livros lidos, total de páginas lidas, streak atual de leitura diária e o maior streak alcançado.
*   **Meta Anual**: Possibilidade de o usuário definir uma meta quantitativa de livros a serem lidos em um determinado ano (por exemplo, ler 12 livros em 2026).

### 2. Catálogo (`apps.catalogo`)
*   **Autores e Categorias**: Cadastro completo de autores (com biografia e país) e categorias de livros.
*   **Livros**: Registro de livros contendo título, ISBN, total de páginas, idioma, data de publicação, imagem de capa e relacionamento com autores e categorias.
*   **Avaliações**: Sistema de resenhas e notas (de 1 a 5 estrelas) dadas pelos usuários aos livros lidos.

### 3. Leituras (`apps.leitura`)
*   **Status da Leitura**: Registro e controle do estado de cada leitura (`Quero Ler`, `Lendo`, `Lido` ou `Abandonado`).
*   **Sessões de Leitura**: Registro incremental de páginas lidas por meio de sessões de leitura (`SessaoLeitura`).
*   **Atualização Automatizada**: Sinais (signals) do Django atualizam automaticamente a quantidade total de páginas lidas, o status da leitura (mudando para `Lendo` ao iniciar ou `Lido` ao atingir o total de páginas) e as datas de início e fim da leitura.

---

## 🛠️ Tecnologias Utilizadas

*   **Python 3**
*   **Django 6**
*   **Django Unfold** (Tema administrativo moderno e responsivo)
*   **SQLite** (Banco de dados padrão para desenvolvimento)
*   **Django Countries** (Para seleção de países de autores e usuários)

---

## 🔧 Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto localmente:

### 1. Clonar o repositório e acessar a pasta do projeto
```bash
cd BookioMarker
```

### 2. Configurar o Ambiente Virtual (`venv`)
Crie e ative o ambiente virtual para isolar as dependências do projeto:

**No Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**No Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências
Com o ambiente virtual ativo, instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

### 4. Executar as Migrações do Banco de Dados
Crie a estrutura de tabelas no banco de dados SQLite:
```bash
python manage.py migrate
```

### 5. Carregar Dados Iniciais (Fixtures)
Popule o catálogo com alguns dados iniciais de autores, categorias e livros:
```bash
python manage.py loaddata catalogo_data.json
```

### 6. Criar um Superusuário (Acesso ao Admin)
Crie uma conta de administrador para gerenciar o sistema:
```bash
python manage.py createsuperuser
```
Siga as instruções no terminal para definir o nome de usuário, e-mail e senha.

### 7. Iniciar o Servidor de Desenvolvimento
Rode o servidor local:
```bash
python manage.py runserver
```

Agora você pode acessar:
*   **A aplicação**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
*   **O Painel Administrativo**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (Entre com as credenciais do superusuário criado).
