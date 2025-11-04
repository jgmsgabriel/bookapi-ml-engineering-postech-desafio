import os
import datetime
import logging
from functools import wraps

import jwt
import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import jsonify, request, current_app

logger = logging.getLogger("app")

# Configs JWT por env (mantém compatibilidade com Config)
JWT_SECRET = os.getenv("JWT_SECRET", "MEUSEGREDOAQUI")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_DELTA_SECONDS = int(os.getenv("JWT_EXP_DELTA_SECONDS", "3600"))

def create_token(username: str) -> str:
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Token ausente"}), 401
        token = auth.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRET", JWT_SECRET), algorithms=[JWT_ALGORITHM])
            request.user = payload.get("username")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        return f(*args, **kwargs)
    return decorated

def scrape_book_details(detail_url: str) -> dict:
    """
    Faz scraping da página de detalhes para:
      - product_description
      - number_of_reviews
    """
    result = {
        "product_description": "Unavailable",
        "number_of_reviews": "Unavailable",
    }
    try:
        resp = requests.get(detail_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Descrição do produto
        desc_tag = soup.find("div", id="product_description")
        if desc_tag:
            result["product_description"] = desc_tag.find_next("p").get_text(strip=True)
        else:
            result["product_description"] = "No description available"

        # Número de reviews
        tbl = soup.find("table", class_="table table-striped")
        if tbl:
            for row in tbl.find_all("tr"):
                header = row.find("th").get_text(strip=True)
                if header.lower() == "number of reviews":
                    result["number_of_reviews"] = row.find("td").get_text(strip=True)
                    break
    except Exception as e:
        logger.warning(f"Falha ao fazer scraping de {detail_url}: {e}")
    return result

def load_books_df() -> pd.DataFrame:
    """
    Lê o CSV do caminho configurado no app (current_app.config["BOOKS_CSV_PATH"]).
    """
    csv_path = current_app.config.get("BOOKS_CSV_PATH", "./data/dados-books.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado em: {csv_path}")
    return pd.read_csv(csv_path)

# Alias opcional para compatibilidade com chamadas antigas
def read_books_csv(*_args, **_kwargs):
    return load_books_df()