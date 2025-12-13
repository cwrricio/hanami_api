from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.services.data_processor import process_dataset
from src.models.vendas import Venda
from src.config.logger import logger

router = APIRouter()

@router.post("/upload", tags=["Upload"])
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Recebe CSV/XLSX, processa e salva no banco, registrando logs de auditoria.
    """
    filename = file.filename
    logger.info(f"Recebendo arquivo para upload: {filename}")

    try:
        # Validação de Extensão
        if not filename.lower().endswith(('.csv', '.xlsx')):
            msg = f"Arquivo rejeitado (extensão inválida): {filename}"
            logger.error(msg)
            raise HTTPException(status_code=400, detail="Formato inválido. Use .csv ou .xlsx")

        # Leitura e ETL
        content = await file.read()
        try:
            df_limpo = process_dataset(content, filename)
        except Exception as e_etl:
            logger.error(f"❌ Erro durante o ETL do arquivo {filename}: {str(e_etl)}")
            raise HTTPException(status_code=422, detail=f"Erro na leitura dos dados: {str(e_etl)}")

        # Salvar no Banco
        records = df_limpo.to_dict(orient="records")
        try:
            db.bulk_insert_mappings(Venda, records)
            db.commit()
            logger.info(f"Sucesso: {len(records)} linhas inseridas no banco via arquivo {filename}.")
        except Exception as e_db:
            db.rollback()
            logger.error(f"🔥 Erro de Banco de Dados ao salvar {filename}: {str(e_db)}")
            raise HTTPException(status_code=500, detail="Erro ao salvar no banco de dados.")

        return {
            "status": "sucesso",
            "mensagem": "Upload processado e logado.",
            "linhas": len(records)
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.critical(f"☠️ Erro inesperado no sistema: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno.")