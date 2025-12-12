from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/upload/", tags=["Upload"])
async def upload_file(file: UploadFile = File (...)):
  """
  Recebe um arquivo CSV ou XLSX para processamento.
  """
  # Validar se o arquivo existe
  if not file:
    raise HTTPException(status_code=400, detail="Nenhum arquivo foi enviado.")
  
  #validar formato 
  filename = file.filename.lower()
  if not filename.endswith(('.csv', '.xlsx')):
    raise HTTPException(status_code=400, detail="Formato de arquivo inválido. Apenas CSV e XLSX são permitidos.")
  
  return {
    "status": "recebido",
    "filename": file.filename,
    "content_type": file.content_type,
    "mensagem": "Arquivo recebido com sucesso para processamento."
  }