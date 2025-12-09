# 🌸 Projeto Hanami Backend

API de Análise de Dados desenvolvida com **FastAPI** e **PostgreSQL**.  
O objetivo deste projeto é processar arquivos de vendas (CSV/XLSX), realizar validações de dados e gerar relatórios analíticos financeiros e de performance.

---

## Tecnologias
- **Python 3.10+**
- **FastAPI** (Framework Web)
- **PostgreSQL**
- **SQLAlchemy**
- **Pandas**

---

## Configuração e Instalação

### 1. Pré-requisitos
- Python 3.10+
- PostgreSQL instalado e rodando

---

### 2. Configurar o Ambiente Virtual
```powershell
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente (Windows)
.\venv\Scripts\activate
```

---

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

---

### 4. Configurar Banco de Dados

Crie um arquivo `.env` na raiz do projeto:
```ini
# --- Arquivo .env ---
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hanami_analytics

DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

---

### 5. Criar as Tabelas
```bash
python create_tables.py
```

Se aparecer "✅ SUCESSO", a tabela foi criada corretamente.

---

##  Rodar a API
```bash
uvicorn src.main:app --reload
```

---

## Testar via Swagger

Acesse:
```
http://127.0.0.1:8000/docs
```

Teste a rota `GET /health` → Try it out → Execute

Resposta esperada:
```json
{
  "status": "ok",
  "database": "Conectado"
}
```