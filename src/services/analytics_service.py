import pandas as pd

def calcular_metricas_financeiras(df: pd.DataFrame) -> dict:
    # Se estiver vazio, retorna zerado
    if df.empty:
        return {
            "receita_liquida": 0.0,
            "lucro_bruto": 0.0,
            "custo_total": 0.0,
            "margem_liquida_percent": 0.0
        } 
    
    # Garante que são números
    valores = pd.to_numeric(df["valor_final"], errors='coerce').fillna(0.0)
    
    # Receita líquida
    receita = valores.sum()
    
    # Lucro Bruto
    if "margem_lucro" in df.columns:
        margens = pd.to_numeric(df["margem_lucro"], errors='coerce').fillna(0.0)
        # Cálculo: Valor * (Margem / 100)
        lucro = (valores * (margens / 100)).sum()
    else:
        lucro = 0.0
      
    custo = receita - lucro
    
    # Margem Líquida Global (%)
    margem_percent = (lucro / receita * 100) if receita > 0 else 0.0
    
    return {
        "receita_liquida": round(receita, 2),
        "lucro_bruto": round(lucro, 2),
        "custo_total": round(custo, 2),
        "margem_liquida_percent": round(margem_percent, 2)
    }

def calcular_metricas_vendas(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_vendas_valor": 0.0,
            "numero_transacoes": 0,
            "media_por_transacao": 0.0
        }
    
    valores = pd.to_numeric(df["valor_final"], errors='coerce').fillna(0.0)
    
    # Número de transações 
    qtd_transacoes = len(df)
    
    # Total de vendas
    total_vendas = valores.sum()
    
    # Ticket médio 
    media = valores.mean()
    
    return {
        "total_vendas_valor": round(total_vendas, 2),
        "numero_transacoes": int(qtd_transacoes),
        "media_por_transacao": round(media, 2)
    }