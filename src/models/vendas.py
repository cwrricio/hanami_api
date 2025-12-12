from sqlalchemy import Column, String, Integer, Float, Date, DateTime
from src.config.database import Base
from sqlalchemy.sql import func

class Venda(Base):
    """
    Representa a tabela 'vendas' no Banco de Dados.
    Otimizada para consultas analíticas de Business Intelligence.
    """
    __tablename__ = "vendas"
    
    # Primary Key: Identificador único da linha
    id_transacao = Column(String(50), primary_key=True, index=True, nullable=False)
    
    # Foreign Keys 
    cliente_id = Column(String(50), index=True, nullable=False)
    produto_id = Column(String(50), index=True, nullable=False)
    vendedor_id = Column(String(50), index=True)

    # nullable=False garante que nunca teremos vendas sem valor no banco
    valor_final = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    desconto_percent = Column(Float, default=0.0)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Float)
    margem_lucro = Column(Float)

    data_venda = Column(Date, nullable=False, index=True)

    canal_venda = Column(String(50))     
    forma_pagamento = Column(String(50)) 
    status_entrega = Column(String(50))  
    
    nome_cliente = Column(String(150))
    idade_cliente = Column(Integer)
    genero_cliente = Column(String(1))
    cidade_cliente = Column(String(100))
    estado_cliente = Column(String(2))   
    renda_estimada = Column(Float)
    regiao = Column(String(20))
    
    nome_produto = Column(String(150))
    categoria = Column(String(50))
    marca = Column(String(50))
    
    tempo_entrega_dias = Column(Integer)

    # Data em que o registro entrou no sistema 
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Venda {self.id_transacao} - {self.valor_final}>"