from fastapi import APIRouter, Depends, Query # <--- Query adicionado
from sqlalchemy.orm import Session
from sqlalchemy import func, desc # <--- desc adicionado
from src.config.database import get_db
from src.models.vendas import Venda
from typing import List, Dict, Any # <--- Tipagem adicionada

router = APIRouter()

# ... (Mantenha o get_sales_summary aqui igual estava) ...
@router.get("/reports/sales-summary", tags=["Relatórios"])
def get_sales_summary(db: Session = Depends(get_db)):
    # ... (código da Etapa 1) ...
    query = db.query(
        func.count(Venda.id_transacao).label("total_transacoes"),
        func.sum(Venda.valor_final).label("valor_total_vendas"),
        func.avg(Venda.valor_final).label("ticket_medio")
    ).first()

    total_vendas = query.valor_total_vendas or 0.0
    total_transacoes = query.total_transacoes or 0
    ticket_medio = query.ticket_medio or 0.0

    return {
        "status": "sucesso",
        "periodo": "global",
        "data": {
            "total_vendas_valor": round(total_vendas, 2),
            "numero_transacoes": total_transacoes,
            "media_por_transacao": round(ticket_medio, 2)
        }
    }

@router.get("/reports/product-analysis", tags=["Relatórios"])
def get_product_analysis(
    sort_by: str = Query("faturamento", enum=["faturamento", "quantidade"], description="Critério de ordenação"),
    limit: int = Query(10, ge=1, le=100, description="Top N produtos"),
    db: Session = Depends(get_db)
):
    """
    Retorna a performance de vendas agrupada por produto.
    Permite ordenar por faturamento ou volume de vendas.
    """
    # 1. Definição das Colunas de Agregação
    col_qtd = func.sum(Venda.quantidade).label("total_pecas")
    col_fat = func.sum(Venda.valor_final).label("total_arrecadado")

    # 2. Construção da Query Base (GROUP BY)
    query = db.query(
        Venda.nome_produto,
        col_qtd,
        col_fat
    ).group_by(Venda.nome_produto)

    # 3. Aplicação da Ordenação Dinâmica
    if sort_by == "quantidade":
        query = query.order_by(desc("total_pecas"))
    else:
        query = query.order_by(desc("total_arrecadado"))

    # 4. Limite (Top N)
    resultados = query.limit(limit).all()

    # 5. Formatação da Resposta
    ranking = []
    for linha in resultados:
        ranking.append({
            "nome_produto": linha.nome_produto,
            "quantidade_vendida": int(linha.total_pecas or 0),
            "total_arrecadado": round(linha.total_arrecadado or 0.0, 2)
        })

    return {
        "status": "sucesso",
        "ordenacao_aplicada": sort_by,
        "top_limit": limit,
        "ranking": ranking
    }