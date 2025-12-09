from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.config.database import get_db

app = FastAPI(
    title="Projeto Hanami Backend",
    version="0.1.0"
)

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Hanami API está online!"}

@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "Conectado"}
    except Exception as e:
        return {"status": "error", "database": f"Erro: {str(e)}"}