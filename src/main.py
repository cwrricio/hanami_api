from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.config.database import get_db
from src.controllers import upload_controller
from src.config.logger import logger 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🌸 Hanami API iniciando... Sistema de logs ativado.")
    yield
    # Shutdown
    logger.info("🛑 Hanami API desligando.")

app = FastAPI(
    title="Projeto Hanami Backend", 
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(upload_controller.router)

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Hanami API está online!"}

@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        logger.info("Health Check: Banco de dados conectado com sucesso.")
        return {"status": "ok", "database": "Conectado 🚀"}
    except Exception as e:
        logger.error(f"Health Check Falhou: {str(e)}")
        return {"status": "error", "database": f"Erro: {str(e)}"}