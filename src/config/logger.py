import logging 
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
  os.makedirs(LOG_DIR)
  
LOG_FILE_PATH = os.path.join(LOG_DIR, "hanami_app.log")

def setup_logger():
  """
  Configura o sistema de logs para salvar em arquivo e mostrar no terminal
  """
  
  #
  logger = logging.getLogger("hanami_backend")
  logger.setLevel(logging.INFO)
  
  formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s} - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
  )
  
  # Handler 1: Arquivo (Salva o histórico, máximo 5MB por arquivo)
  file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
  file_handler.setFormatter(formatter)

  # Handler 2: Console (Mostra no terminal colorido se o terminal suportar)
  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)

    # Adiciona os handlers apenas se ainda não existirem (evita logs duplicados)
  if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

  return logger

# Instância pronta para uso
logger = setup_logger()