# Guia de Deploy no PythonAnywhere

## Passo 1: Criar conta no PythonAnywhere

1. Acesse [pythonanywhere.com](https://www.pythonanywhere.com)
2. Clique em "Sign up" e escolha um plano (o plano gratuito é suficiente para começar)
3. Complete o registro e faça login

## Passo 2: Clone ou upload do repositório

### Opção A: Usando Git (recomendado)

1. No Dashboard do PythonAnywhere, abra um console "Bash"
2. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/equipment_control.git
cd equipment_control
```

### Opção B: Upload manual
1. Faça upload dos arquivos via Web UI

## Passo 3: Criar e configurar ambiente virtual

1. No console Bash do PythonAnywhere:
```bash
cd ~/equipment_control
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Passo 4: Configurar o banco de dados

1. Execute as migrações:
```bash
python manage.py migrate
```

2. Se quiser carregar os status iniciais:
```bash
python manage.py loaddata inventory/fixtures/status_initial.json
```

3. Crie um superusuário:
```bash
python manage.py createsuperuser
```

## Passo 5: Coletar arquivos estáticos

```bash
python manage.py collectstatic --noinput
```

⚠️ **Importante**: Este comando requer que `STATIC_ROOT` esteja configurado em `settings.py`:

```python
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
```

## Passo 6: Configurar settings.py para produção

Edite `equipment_control_project/settings.py`:

```python
# Mude DEBUG para False em produção
DEBUG = False

# Adicione seu domínio PythonAnywhere
ALLOWED_HOSTS = ['seu-usuario.pythonanywhere.com']

# Configure o banco de dados (PythonAnywhere oferece SQLite, PostgreSQL, MySQL)
# Para SQLite (padrão):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Ou para PostgreSQL (mais recomendado em produção):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seu-usuario$equipment_control',
        'USER': 'seu-usuario',
        'PASSWORD': 'sua-senha-db',
        'HOST': 'seu-usuario.postgres.pythonanywhere-services.com',
        'PORT': '5432',
    }
}

# Configurar arquivos estáticos
STATIC_ROOT = '/home/seu-usuario/equipment_control/static'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

## Passo 7: Configurar Web App no PythonAnywhere

1. Vá para "Web" no menu lateral
2. Clique em "Add a new web app"
3. Escolha "Manual configuration"
4. Escolha Python 3.x (compatível com sua versão)
5. Após criar, clique no web app e vá para "WSGI configuration file"

### Editar arquivo WSGI

O arquivo deve estar em `/home/seu-usuario/equipment_control/equipment_control_project/wsgi.py`

Copie este conteúdo:

```python
import os
import sys

# Adicione o caminho do projeto ao path
path = '/home/seu-usuario/equipment_control'
if path not in sys.path:
    sys.path.insert(0, path)

# Ative o ambiente virtual
os.environ['VIRTUAL_ENV'] = '/home/seu-usuario/equipment_control/venv'
virtual_env = os.path.expanduser(os.environ.get('VIRTUAL_ENV', '/home/seu-usuario/equipment_control/venv'))
if virtual_env:
    activate_this = os.path.join(virtual_env, 'bin', 'activate_this.py')
    if os.path.exists(activate_this):
        with open(activate_this) as f:
            exec(f.read(), dict(__file__=activate_this))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_control_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Passo 8: Configurar arquivos estáticos e media

1. No Web App do PythonAnywhere, abaixo de "Code", configure:
   - **URL**: `/static/` → **Directory**: `/home/seu-usuario/equipment_control/static`

## Passo 9: Reiniciar Web App

1. Vá para a página Web App
2. Clique no botão verde "Reload [seu-usuario.pythonanywhere.com]"

## Passo 10: Acessar sua aplicação

Sua aplicação estará disponível em:
```
https://seu-usuario.pythonanywhere.com
```

## Solução de problemas

### Erro: "ImproperlyConfigured: STATIC_ROOT setting to a filesystem path"

Adicione ao `settings.py`:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
```

Depois execute:
```bash
python manage.py collectstatic --noinput
```

### Ver logs de erro
- Vá para "Web" → Seu app → Clique em "Error log" ou "Server log"

### Certificado SSL
- PythonAnywhere fornece SSL gratuito. Ative em "Web" → "Security"

### Variáveis de ambiente
- Se precisar de variáveis secretas, adicione em "Web" → "Environment variables"

## Melhorias futuras

Para produção em escala maior, considere:
- **PostgreSQL** em vez de SQLite
- **Azure App Service** com PostgreSQL gerenciado
- **DigitalOcean App Platform** com Docker
- **Heroku** (mais caro, mas fácil de usar)

## Referências
- [PythonAnywhere Django Guide](https://help.pythonanywhere.com/pages/Django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
