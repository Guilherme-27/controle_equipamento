# Controle de Equipamentos - Escola

Projeto Integrador do primeiro semestre de 2026 da UNIVESP — Eixo de Computação.

Sistema web para controle de equipamentos escolares, permitindo cadastrar ambientes (salas, laboratórios), registrar equipamentos e acompanhar o status de cada um.

---

## Funcionalidades

- Login obrigatório para acessar o sistema
- Cadastro, edição e exclusão de ambientes
- Cadastro, edição e exclusão de equipamentos
- Cadastro, edição e exclusão de status (ex: Operante, Atenção, Inoperante)
- Busca por nome e filtros por ambiente e status
- Ordenação por colunas na listagem
- Dashboard de ambientes com contagem de equipamentos por status
- Paginação
- Impede excluir ambiente ou status que tenha equipamento vinculado

---

## Tecnologias

- Python / Django 6.0
- Bootstrap 5
- SQLite (desenvolvimento) / PostgreSQL (produção)
- WhiteNoise / Gunicorn
- Deploy no PythonAnywhere

---

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/Guilherme-27/controle_equipamento.git
   cd controle_equipamento
   ```

2. Crie e ative o ambiente virtual:

   **Linux / macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Copie o arquivo de exemplo e configure:
   ```bash
   cp .env.example .env
   ```

5. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

6. Carregue os status iniciais:
   ```bash
   python manage.py loaddata inventory/fixtures/status_initial.json
   ```

7. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

8. Rode o servidor:
   ```bash
   python manage.py runserver
   ```

Acesse [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Estrutura do Projeto

```
controle_equipamento/
├── equipment_control_project/   # Configurações do Django
│   ├── settings.py
│   ├── settings_prod.py
│   ├── urls.py
│   └── wsgi.py
├── inventory/                   # App principal
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── fixtures/
├── templates/
│   ├── base.html
│   └── inventory/
├── .env.example
├── manage.py
├── requirements.txt
├── SECURITY_CHECKLIST.md
├── DEPLOY_QUICK.md
└── DEPLOYMENT_PYTHONANYWHERE.md
```

---

## Deploy

Para colocar em produção, veja os guias:

- [`DEPLOY_QUICK.md`](DEPLOY_QUICK.md) — Passos rápidos
- [`DEPLOYMENT_PYTHONANYWHERE.md`](DEPLOYMENT_PYTHONANYWHERE.md) — Deploy no PythonAnywhere
- [`SECURITY_CHECKLIST.md`](SECURITY_CHECKLIST.md) — Checklist de segurança
