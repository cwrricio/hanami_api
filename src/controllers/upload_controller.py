from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.services.data_processor import process_dataset
from src.models.vendas import Venda

router = APIRouter()

@router.post("/upload", tags=["Upload"])
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Recebe CSV/XLSX, limpa os dados e salva no Banco de Dados PostgreSQL.
    """
    try:
        #Leitura e Processamento (ETL)
        content = await file.read()
        df_limpo = process_dataset(content, file.filename)

        # Conversão: DataFrame -> Lista de Dicionários
        records = df_limpo.to_dict(orient="records")

        # Salvamento no Banco com bulk insert
        try:
            db.bulk_insert_mappings(Venda, records)
            db.commit() 
        except Exception as e:
            db.rollback() # Desfaz se der erro (ex: ID duplicado)
            # Verifica se é erro de duplicidade (IntegrityError)
            if "duplicate key" in str(e) or "unique constraint" in str(e):
                raise HTTPException(status_code=409, detail="Erro: Algumas transações já existem no banco de dados.")
            raise e

        return {
            "status": "sucesso",
            "mensagem": "Dados processados e salvos no banco com sucesso!",
            "linhas_importadas": len(records),
            "database": "PostgreSQL"
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")