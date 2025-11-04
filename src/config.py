import os
from dotenv import load_dotenv

# Carrega variáveis do .env (se existir)
load_dotenv()

class Config:
    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "MEUSEGREDOAQUI")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXP_DELTA_SECONDS = int(os.getenv("JWT_EXP_DELTA_SECONDS", "3600"))

    # Caminho do CSV (padrão no projeto)
    BOOKS_CSV_PATH = os.getenv("BOOKS_CSV_PATH", "./data/dados-books.csv")

    # Swagger (apenas metadados; a config completa é passada no __init__.py)
    SWAGGER = {
        "title": os.getenv("SWAGGER_TITLE", "Catálogo API Scrape Books"),
        "uiversion": 3,
    }

    # Credenciais de teste
    TEST_USERNAME = os.getenv("TEST_USERNAME", "admin")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "secret")