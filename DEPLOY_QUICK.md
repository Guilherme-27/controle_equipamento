# 📋 Guia Rápido de Deploy

## ✅ Checklist antes do Deploy

- [ ] Git repository criado e commits feitos
- [ ] `.env` não está commitado (verificar `.gitignore`)
- [ ] `DEBUG = False` em produção
- [ ] `ALLOWED_HOSTS` configurado com seu domínio
- [ ] `SECRET_KEY` gerada e segura
- [ ] Migrações executadas
- [ ] `collectstatic` executado
- [ ] HTTPS/SSL ativado

## 🚀 Deploy no PythonAnywhere (Fácil)

### 1. Conta e Repositório
```bash
# Crie conta em pythonanywhere.com
# Clone seu repositório
git clone https://github.com/seu-usuario/equipment_control.git
cd equipment_control
```

### 2. Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Banco de Dados
```bash
python manage.py migrate
python manage.py loaddata inventory/fixtures/status_initial.json
python manage.py createsuperuser
```

### 4. Arquivos Estáticos
```bash
python manage.py collectstatic --noinput
```

### 5. Configurar PythonAnywhere
- Acesse **Web** → **Add a new web app**
- Escolha **Manual configuration** → **Python 3.x**
- Configure o arquivo WSGI (veja DEPLOYMENT_PYTHONANYWHERE.md)
- Configure **Static files**: `/static/` → `/home/seu-usuario/equipment_control/static`

### 6. Variáveis de Ambiente
No PythonAnywhere, vá para **Web** → **Environment variables** e adicione:
```
DEBUG=False
SECRET_KEY=sua-chave-super-secreta
ALLOWED_HOSTS=seu-usuario.pythonanywhere.com
```

### 7. Recarregar
Clique no botão verde **Reload** na página Web app.

Seu app estará em: `https://seu-usuario.pythonanywhere.com`

---

## 🔐 Gerador de SECRET_KEY

```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
# Copie e guarde em local seguro!
```

---

## 📁 Estrutura de Pasta no PythonAnywhere

```
/home/seu-usuario/
├── equipment_control/           # Seu projeto
│   ├── venv/                   # Ambiente virtual
│   ├── inventory/              # App Django
│   ├── equipment_control_project/
│   ├── static/                 # Arquivos coletados (gerado)
│   ├── manage.py
│   ├── db.sqlite3
│   ├── requirements.txt
│   └── .env                    # NÃO COMMITAR!
```

---

## 🐛 Troubleshooting

| Erro | Solução |
|------|---------|
| `ImproperlyConfigured: STATIC_ROOT` | Adicione `STATIC_ROOT = BASE_DIR / "static"` em settings.py |
| `Página em branco (500)` | Verifique error log em Web → Error log |
| `CSS/JS não carrega` | Execute `python manage.py collectstatic --noinput` |
| `Database locked` | Use PostgreSQL ao invés de SQLite em produção |

---

## 📊 Próximas Melhorias

- [ ] PostgreSQL em vez de SQLite
- [ ] Email automático para notificações
- [ ] Backup automático do banco
- [ ] Monitoramento de uptime
- [ ] CDN para arquivos estáticos

---

## 📚 Referências

- [PythonAnywhere Django Docs](https://help.pythonanywhere.com/pages/Django)
- [Django Deployment](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- [Django Security](https://docs.djangoproject.com/en/6.0/topics/security/)
