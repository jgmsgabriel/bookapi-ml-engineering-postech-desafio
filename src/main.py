import logging
from flask import jsonify, request
import pandas as pd

from .config import Config
from .utilidades import (
    create_token,
    token_required,
    scrape_book_details,
    load_books_df,   # usamos sempre esta função
)

logger = logging.getLogger("app")

def register_routes(app):
    # ----- Auth -----
    @app.route("/api/v1/auth/login", methods=["POST"])
    def login():
        """
        Login
        ---
        tags: [Auth]
        """
        data = request.get_json(force=True)
        username = data.get("username")
        password = data.get("password")
        if username == Config.TEST_USERNAME and password == Config.TEST_PASSWORD:
            token = create_token(username)
            logger.info("Usuario logado e token enviado")
            return jsonify({"token": token})
        else:
            logger.error("Credenciais inválidas")
            return jsonify({"error": "Credenciais inválidas"}), 401

    @app.route("/api/v1/auth/refresh", methods=["POST"])
    @token_required
    def refresh_token():
        """
        Renova o token JWT.
        ---
        tags: [Auth]
        security: [Bearer: []]
        """
        try:
            username = getattr(request, "user", None)
            if not username:
                return jsonify({"error": "Usuário não identificado"}), 401
            new_token = create_token(username)
            logger.info(f"Token renovado para o usuário: {username}")
            return jsonify({"token": new_token}), 200
        except Exception:
            logger.exception("Erro ao renovar token")
            return jsonify({"error": "Falha ao renovar token"}), 500

    # ----- Root -----
    @app.route("/")
    def route_hello():
        logger.info("API testada")
        return jsonify({
            "message": "s2 Conexao estabelecida: True | Latência do amor: 0ms | Status: Eternamente apaixonado por você, te amo! Feliz 01 atrasado s2"
        })

    # Mantido literal como no original (com dois pontos)
    @app.route("/api/v1/health:", methods=["GET"])
    def health():
        """
        Healthcheck
        ---
        tags: [Health]
        """
        try:
            try:
                df = load_books_df()
                record_count = len(df)
                logger.info("API: OK, Data: Connected")
                return jsonify({
                    "api_status": "ok",
                    "data_status": "connected",
                    "records": record_count
                }), 200
            except FileNotFoundError:
                logger.info("API: OK, Data: Missing")
                return jsonify({
                    "api_status": "ok",
                    "data_status": "missing",
                    "records": 0
                }), 500
        except Exception:
            logger.exception("Erro no healthcheck")
            return jsonify({
                "api_status": "ok",
                "data_status": "error",
                "records": 0
            }), 500

    # ----- Books -----
    @app.route("/api/v1/books", methods=["GET"])
    @token_required
    def list_books():
        """
        Lista todos os livros (array)
        ---
        tags: [Books]
        security: [Bearer: []]
        """
        try:
            df = load_books_df()
            return jsonify(df.to_dict(orient="records")), 200
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 500
        except Exception:
            logger.exception("Falha ao carregar livros")
            return jsonify({"error": "Falha ao carregar a base"}), 500

    @app.route("/api/v1/books/search", methods=["GET"])
    @token_required
    def search_books():
        """
        Busca por título e/ou categoria
        ---
        tags: [Books]
        security: [Bearer: []]
        """
        try:
            df = load_books_df()
            title = request.args.get("title", "").strip()
            category = request.args.get("category", "").strip()

            if not title and not category:
                return jsonify({"error": "Informe ao menos um parâmetro: title ou category"}), 400

            if title and category:
                logger.info("Filtrando por title e category")
                df = df[
                    df["title"].str.contains(title, case=False, na=False) &
                    df["category"].str.contains(category, case=False, na=False)
                ]
            elif title:
                logger.info("Filtrando por title")
                df = df[df["title"].str.contains(title, case=False, na=False)]
            elif category:
                logger.info("Filtrando por category")
                df = df[df["category"].str.contains(category, case=False, na=False)]

            return jsonify(df.to_dict(orient="records")), 200
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 500
        except Exception:
            logger.exception("Erro na busca de livros")
            return jsonify({"error": "Falha ao buscar livros"}), 500

    @app.route("/api/v1/categories", methods=["GET"])
    @token_required
    def list_categories():
        """
        Lista categorias
        ---
        tags: [Categories]
        security: [Bearer: []]
        """
        try:
            df = load_books_df()
            categories = sorted(df["category"].dropna().unique().tolist())
            return jsonify(categories), 200
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 500
        except Exception:
            logger.exception("Erro ao listar categorias")
            return jsonify({"error": "Falha ao listar categorias"}), 500

    @app.route("/api/v1/books/<int:book_id>", methods=["GET"])
    @token_required
    def get_book(book_id: int):
        """
        Detalhe por ID (índice do CSV)
        ---
        tags: [Books]
        security: [Bearer: []]
        """
        try:
            df = load_books_df()
            if book_id < 0 or book_id >= len(df):
                logger.exception("Livro não encontrado")
                return jsonify({"error": "Livro não encontrado"}), 404
            return jsonify(df.iloc[book_id].to_dict()), 200
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 500
        except Exception:
            logger.exception("Erro ao buscar livro por ID")
            return jsonify({"error": "Falha ao buscar livro"}), 500

    @app.route("/api/v1/scrape-book/<int:book_id>", methods=["GET"])
    @token_required
    def get_book_sc(book_id: int):
        """
        Enriquecimento por scraping (description/reviews)
        ---
        tags: [Books]
        security: [Bearer: []]
        """
        try:
            df = load_books_df()
            if book_id < 0 or book_id >= len(df):
                return jsonify({"error": "Livro não encontrado"}), 404
            book = df.iloc[book_id].to_dict()
            detail_url = book.get("detail_url")
            if not detail_url:
                return jsonify({"error": "URL de detalhes ausente"}), 500
            scraped = scrape_book_details(detail_url)
            book.update(scraped)
            return jsonify(book), 200
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 500
        except Exception:
            logger.exception("Erro ao buscar livro por ID")
            return jsonify({"error": "Falha ao buscar livro"}), 500

    # ----- Stats -----
    @app.route("/api/v1/stats/overview", methods=["GET"])
    @token_required
    def stats_overview():
        """
        Estatísticas gerais
        ---
        tags: [Stats]
        security: [Bearer: []]
        """
        try:
            df = load_books_df()
            total_books = len(df)
            average_price = round(df["price"].mean(skipna=True), 2)
            rating_distribution = (
                df["rating"].value_counts(dropna=True).sort_index().astype(int).to_dict()
            )
            return jsonify({
                "total_books": total_books,
                "average_price": average_price,
                "rating_distribution": rating_distribution
            }), 200
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 500
        except Exception:
            logger.exception("Erro ao calcular estatísticas gerais")
            return jsonify({"error": "Falha ao calcular estatísticas"}), 500

    @app.route("/api/v1/stats/categories", methods=["GET"])
    @token_required
    def stats_by_category():
        """
        Estatísticas por categoria
        ---
        tags: [Stats]
        security: [Bearer: []]
        """
        try:
            df = load_books_df()
            stats = (
                df.groupby("category", dropna=True)["price"]
                  .agg(total_books="count", avg_price="mean", min_price="min", max_price="max")
                  .reset_index()
            )
            stats["avg_price"] = stats["avg_price"].round(2)
            stats["min_price"] = stats["min_price"].round(2)
            stats["max_price"] = stats["max_price"].round(2)
            return jsonify(stats.to_dict(orient="records")), 200
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 500
        except Exception:
            logger.exception("Erro ao calcular estatísticas por categoria")
            return jsonify({"error": "Falha ao calcular estatísticas"}), 500

    @app.route("/api/v1/books/top-rated", methods=["GET"])
    @token_required
    def top_rated_books():
        """
        Livros com melhor rating
        ---
        tags: [Books]
        security: [Bearer: []]
        """
        try:
            df = load_books_df()
            max_rating = df["rating"].max()
            top_books = df[df["rating"] == max_rating]
            return jsonify(top_books.to_dict(orient="records")), 200
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 500
        except Exception:
            logger.exception("Erro ao listar livros com melhor rating")
            return jsonify({"error": "Falha ao listar livros"}), 500

    @app.route("/api/v1/books/price-range", methods=["GET"])
    @token_required
    def books_by_price_range():
        """
        Filtra por faixa de preço
        ---
        tags: [Books]
        security: [Bearer: []]
        """
        try:
            df = load_books_df()
            min_price = request.args.get("min", type=float)
            max_price = request.args.get("max", type=float)
            if min_price is None or max_price is None:
                return jsonify({"error": "Parâmetros 'min' e 'max' são obrigatórios"}), 400
            filtered = df[(df["price"] >= min_price) & (df["price"] <= max_price)]
            return jsonify(filtered.to_dict(orient="records")), 200
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 500
        except Exception:
            logger.exception("Erro ao filtrar livros por faixa de preço")
            return jsonify({"error": "Falha ao filtrar livros"}), 500


# Executar como módulo: python -m src.main
if __name__ == "__main__":
    from . import create_app
    import os
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)