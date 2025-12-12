from src.config.database import engine, Base
from src.models.vendas import Venda 

print("Iniciando a construção do Banco de Dados...")

try:
    Base.metadata.drop_all(bind=engine)
    print("   - Tabelas antigas removidas (Limpeza).")
    
    Base.metadata.create_all(bind=engine)
    print("SUCESSO! Tabela 'vendas' criada no PostgreSQL.")
    
except Exception as e:
    print(f"ERRO: {e}")