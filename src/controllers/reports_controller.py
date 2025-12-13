from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.config.database import get_db
from src.models.vendas import Venda

router = APIRouter()

@router.get("/reports/sales-summary", tags=["Relatórios"])
def get_sales_summary(db: Session = Depends(get_db)):
    """
    Retorna o consolidado geral de vendas (KPIs).
    Realiza a agregação diretamente no Banco de Dados.
    """
    query = db.query(
        func.count(Venda.id_transacao).label("total_transacoes"),
        func.sum(Venda.valor_final).label("valor_total_vendas"),
        func.avg(Venda.valor_final).label("ticket_medio")
    ).first()

    # Tratamento de Nulos (Caso o banco esteja vazio, evita retornar None)
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