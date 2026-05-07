#!/bin/bash
# Script de deployment para PythonAnywhere
# Uso: bash deploy.sh seu-usuario

if [ -z "$1" ]; then
    echo "Uso: bash deploy.sh seu-usuario"
    exit 1
fi

USERNAME=$1
PROJECT_DIR="/home/$USERNAME/equipment_control"
VENV_DIR="$PROJECT_DIR/venv"

echo "🚀 Iniciando deployment para PythonAnywhere..."

# 1. Ativar ambiente virtual
echo "📦 Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate"

# 2. Ir para diretório do projeto
echo "📂 Entrando no diretório do projeto..."
cd "$PROJECT_DIR"

# 3. Pull das atualizações (se usando git)
echo "🔄 Atualizando repositório..."
git pull origin main || git pull origin master || echo "⚠️ Git pull falhou, continuando..."

# 4. Instalar/atualizar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt --upgrade

# 5. Executar migrações
echo "🗄️ Executando migrações..."
python manage.py migrate

# 6. Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# 7. Limpar cache
echo "🧹 Limpando cache..."
rm -rf "$PROJECT_DIR/equipment_control_project/__pycache__"
rm -rf "$PROJECT_DIR/inventory/__pycache__"
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -delete

# 8. Recarregar o web app
echo "🔄 Recarregando web app no PythonAnywhere..."
curl -X POST https://www.pythonanywhere.com/api/v0/user/$USERNAME/webapps/$USERNAME.pythonanywhere.com/reload/ \
  -H "Authorization: Token $PYTHONANYWHERE_API_TOKEN"

echo "✅ Deployment concluído!"
