# 🔐 Checklist de Segurança para Produção

## ⚠️ CRÍTICO - Antes de fazer Deploy

- [ ] **DEBUG = False** - Mude em `settings.py` ou via variável de ambiente
- [ ] **SECRET_KEY única** - Gere uma nova chave segura, nunca use a padrão
- [ ] **ALLOWED_HOSTS configurado** - Especifique seu domínio, não `*`
- [ ] **.env não commitado** - Adicione `.env` ao `.gitignore`
- [ ] **Senhas não commitadas** - Nenhuma senha no código
- [ ] **HTTPS/SSL ativado** - Redirecione HTTP → HTTPS
- [ ] **Banco em local seguro** - Longe do diretório do projeto

## 🔒 Configurações de Segurança

```python
# settings.py em produção

DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']
SECRET_KEY = 'gere-uma-chave-segura-e-longa'

# SSL/HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Segurança adicional
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}
```

## 🗝️ Variáveis de Ambiente

Crie `.env` **localmente** (nunca no repositório):

```env
# Segurança
DEBUG=False
SECRET_KEY=sua-chave-super-longa-e-segura-123456789
ALLOWED_HOSTS=seu-usuario.pythonanywhere.com

# Banco de Dados (opcional)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=seu-usuario$equipment_control
DB_USER=seu-usuario
DB_PASSWORD=sua-senha-super-segura
DB_HOST=seu-usuario.postgres.pythonanywhere-services.com
```

Use a biblioteca `python-dotenv` para ler:

```python
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

## 🛡️ Headers de Segurança

```python
# Previne clickjacking
X_FRAME_OPTIONS = 'DENY'

# Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", 'cdnjs.cloudflare.com'),
    'style-src': ("'self'", 'cdnjs.cloudflare.com'),
}

# Previne MIME sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Previne XSS
SECURE_BROWSER_XSS_FILTER = True
```

## 🔐 Autenticação

- [ ] Usuários têm senhas fortes
- [ ] 2FA habilitado (se possível)
- [ ] Senhas nunca são log
- [ ] Session timeout configurado

```python
# settings.py
SESSION_COOKIE_AGE = 1209600  # 2 semanas
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

## 💾 Backup

- [ ] Backup automático do banco de dados
- [ ] Backup seguro em local protegido
- [ ] Restauração testada

Para SQLite:
```bash
# Cron job diário
0 2 * * * cp ~/equipment_control/db.sqlite3 ~/backups/db-$(date +\%Y\%m\%d).sqlite3
```

## 🚨 Monitoramento

- [ ] Ativar logging de erros
- [ ] Monitorar uso de recursos
- [ ] Alertas para erros 500
- [ ] Verificação de uptime

## 📝 Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
    },
}
```

## 🔄 Updates de Segurança

- [ ] Django e todas as dependências estão atualizadas
- [ ] Verificar regularmente por CVEs
- [ ] Patch security releases imediatamente

```bash
pip list --outdated
pip install --upgrade django
```

## ✅ Antes de Ir Live

1. Teste em staging environment
2. Verificar todos os links
3. Testar login e funcionalidades principais
4. Monitorar por 24 horas
5. Preparar plano de rollback

## 📞 Suporte

PythonAnywhere oferece suporte gratuito para contas pagas. Para problemas de segurança críticos:
- Contacte o suporte imediatamente
- Se necessário, retire do ar até solucionar
