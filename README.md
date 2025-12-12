# 🌸 Projeto Hanami Backend

API de Análise de Dados desenvolvida com **FastAPI** e **PostgreSQL**.  
O objetivo deste projeto é processar arquivos de vendas (CSV/XLSX), realizar validações de dados e gerar relatórios analíticos financeiros e de performance.

## ✅ Status do Projeto
- [x] **Task 1:** Setup do Ambiente e Banco de Dados
- [x] **Task 2:** Motor de Leitura e Validação de Dados (ETL)

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

## 📁 Estrutura do Arquivo de Dados
Para realizar o upload, o arquivo (**CSV** ou **XLSX**) deve conter estritamente as colunas abaixo. A API realiza validação automática e rejeita arquivos fora do padrão.

| Categoria | Colunas |
| :--- | :--- |
| **Vendas** | `id_transacao`, `data_venda`, `valor_final`, `subtotal`, `desconto_percent`, `canal_venda`, `forma_pagamento` |
| **Clientes** | `cliente_id`, `nome_cliente`, `idade_cliente`, `genero_cliente`, `cidade_cliente`, `estado_cliente`, `renda_estimada` |
| **Produtos** | `produto_id`, `nome_produto`, `categoria`, `marca`, `preco_unitario`, `quantidade`, `margem_lucro` |
| **Logística** | `regiao`, `status_entrega`, `tempo_entrega_dias`, `vendedor_id` |

### Regras de Tratamento de Dados
O sistema aplica uma "blindagem" automática durante o processamento:
1. **Dados Críticos:** Linhas sem `id_transacao`, `valor_final` ou `data_venda` são **removidas**.
2. **Nulos:** Campos numéricos vazios viram `0`; textos vazios viram `"Não Informado"`.
3. **Padronização:**
   - **Minúsculas:** `canal_venda`, `categoria`, `status_entrega`.
   - **Maiúsculas:** Siglas (UF, Região) e IDs.
   - **Title Case:** Nomes de clientes e produtos.
  
  Pode realizar o teste do tratamento dos dados rodando:
  ```json
  python tests/test_etl.py
```