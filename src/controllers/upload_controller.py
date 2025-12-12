from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.data_processor import process_dataset

router = APIRouter()

@router.post("/upload", tags=["Upload"])
async def upload_file(file: UploadFile = File(...)):
    """
    Recebe arquivo, valida colunas, limpa dados e retorna estatísticas.
    """
    try:
        content = await file.read()

        # Processamento dos dados (task2)
        # Se tiver colunas erradas, o process_dataset vai dar um erro 400 aqui
        df_limpo = process_dataset(content, file.filename)

        return {
            "status": "sucesso",
            "mensagem": "Arquivo validado e processado com sucesso!",
            "total_linhas_validas": len(df_limpo),
            "preview_dados": df_limpo.head(3).to_dict(orient="records")
        }

    except HTTPException as he:
        # Se o data_processor lançou erro (ex: Coluna faltando), repassamos pro usuário
        raise he
    except Exception as e:
        # Erros inesperados
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")