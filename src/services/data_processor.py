import pandas as pd
from io import BytesIO
from fastapi import HTTPException
from src.utils.constants import (
    REQUIRED_COLUMNS, CRITICAL_COLUMNS, 
    UPPERCASE_COLUMNS, LOWERCASE_COLUMNS, TITLECASE_COLUMNS
)

def load_file(file_content: bytes, filename: str) -> pd.DataFrame:
    """Lê CSV ou Excel."""
    try:
        if filename.endswith(".csv"):
            return pd.read_csv(BytesIO(file_content))
        elif filename.endswith(".xlsx"):
            return pd.read_excel(BytesIO(file_content))
        else:
            raise HTTPException(status_code=400, detail="Formato inválido. Use CSV ou XLSX.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na leitura do arquivo: {str(e)}")

def validate_structure(df: pd.DataFrame):
    """Garante que todas as colunas do PDF existem."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise HTTPException(
            status_code=400, 
            detail=f"Arquivo inválido. Colunas faltando: {', '.join(missing)}"
        )

def _handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Estratégia de Blindagem contra Nulos."""
    
    # 1. Remove linhas onde dados críticos estão faltando
    df = df.dropna(subset=CRITICAL_COLUMNS)

    # 2. Numéricos restantes viram 0 
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # 3. Textos restantes viram "Não Informado"
    text_cols = df.select_dtypes(include=['object']).columns
    df[text_cols] = df[text_cols].fillna("Não Informado")
    
    return df

def _enforce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas para os tipos corretos (Data, Int, Float)."""
    
    if "data_venda" in df.columns:
        df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
        df = df.dropna(subset=["data_venda"])

    float_cols = ["valor_final", "subtotal", "desconto_percent", "renda_estimada", "preco_unitario", "margem_lucro"]
    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    int_cols = ["idade_cliente", "quantidade", "tempo_entrega_dias"]
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
            
    return df

def _standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica Casing (Maiúscula/minúscula)."""
    
    # Minúsculas (Categorias)
    for col in LOWERCASE_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

    # Maiúsculas (Siglas/Códigos)
    for col in UPPERCASE_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.upper().str.strip()

    # Title Case (Nomes)
    for col in TITLECASE_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title().str.strip()
            
    return df

def process_dataset(file_content: bytes, filename: str) -> pd.DataFrame:
    """Função Principal (Pipeline de ETL)."""
    # 1. Carregar
    df = load_file(file_content, filename)
    
    # 2. Validar
    validate_structure(df)
    
    # 3. Limpar (Nulos e Tipos)
    df = _handle_nulls(df)
    df = _enforce_types(df)
    
    # 4. Padronizar
    df = _standardize_text(df)
    
    return df