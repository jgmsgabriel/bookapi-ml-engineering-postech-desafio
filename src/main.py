import logging
from flask import jsonify, request
import pandas as pd

from .config import Config
from .utilidades import (
    create_token,
    token_required,
    scrape_book_details,
    load_books_df,
)

logger = logging.getLogger("app")

def register_routes(app):
    # ----- Auth -----
    @app.route("/api/v1/auth/login", methods=["POST"])
    def login():
        """
        Login - Autentica usuário e retorna token JWT
        ---
        tags:
          - Auth
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: body
            name: body
            description: Credenciais de autenticação
            required: true
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                  example: admin
                  description: Nome de usuário
                password:
                  type: string
                  example: secret
                  description: Senha do usuário
        responses:
          200:
            description: Login realizado com sucesso
            schema:
              type: object
              properties:
                token:
                  type: string
                  description: Token JWT para autenticação nas próximas requisições
          401:
            description: Credenciais inválidas
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Credenciais inválidas
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
        Renova o token JWT
        ---
        tags:
          - Auth
        security:
          - Bearer: []
        responses:
          200:
            description: Token renovado com sucesso
            schema:
              type: object
              properties:
                token:
                  type: string
          401:
            description: Token inválido ou expirado
            schema:
              type: object
              properties:
                error:
                  type: string
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

    @app.route("/api/v1/health:", methods=["GET"])
    def health():
        """
        Healthcheck - Verifica status da API e conexão com dados
        ---
        tags:
          - Health
        responses:
          200:
            description: API funcionando normalmente
            schema:
              type: object
              properties:
                api_status:
                  type: string
                  example: ok
                data_status:
                  type: string
                  example: connected
                records:
                  type: integer
                  example: 1000
          500:
            description: Problema com os dados
            schema:
              type: object
              properties:
                api_status:
                  type: string
                data_status:
                  type: string
                records:
                  type: integer
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
        Lista todos os livros
        ---
        tags:
          - Books
        security:
          - Bearer: []
        responses:
          200:
            description: Lista de livros retornada com sucesso
            schema:
              type: array
              items:
                type: object
                properties:
                  title:
                    type: string
                  category:
                    type: string
                  price:
                    type: number
                  rating:
                    type: integer
                  detail_url:
                    type: string
          401:
            description: Token ausente ou inválido
          500:
            description: Erro ao carregar dados
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
        Busca livros por título e/ou categoria
        ---
        tags:
          - Books
        security:
          - Bearer: []
        parameters:
          - name: title
            in: query
            type: string
            required: false
            description: Buscar por título (case insensitive)
            example: Python
          - name: category
            in: query
            type: string
            required: false
            description: Buscar por categoria (case insensitive)
            example: Fiction
        responses:
          200:
            description: Livros encontrados
            schema:
              type: array
              items:
                type: object
          400:
            description: Parâmetros inválidos
          401:
            description: Token ausente ou inválido
          500:
            description: Erro ao buscar dados
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
        Lista todas as categorias disponíveis
        ---
        tags:
          - Categories
        security:
          - Bearer: []
        responses:
          200:
            description: Lista de categorias
            schema:
              type: array
              items:
                type: string
          401:
            description: Token ausente ou inválido
          500:
            description: Erro ao carregar dados
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
        Obtém detalhes de um livro específico pelo ID
        ---
        tags:
          - Books
        security:
          - Bearer: []
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: ID do livro (índice no CSV)
            example: 0
        responses:
          200:
            description: Detalhes do livro
            schema:
              type: object
          404:
            description: Livro não encontrado
          401:
            description: Token ausente ou inválido
          500:
            description: Erro ao buscar livro
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
        Enriquece dados do livro com scraping (descrição e reviews)
        ---
        tags:
          - Books
        security:
          - Bearer: []
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: ID do livro para enriquecer dados
            example: 0
        responses:
          200:
            description: Livro com dados enriquecidos
            schema:
              type: object
          404:
            description: Livro não encontrado
          401:
            description: Token ausente ou inválido
          500:
            description: Erro ao fazer scraping
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
        Estatísticas gerais dos livros
        ---
        tags:
          - Stats
        security:
          - Bearer: []
        responses:
          200:
            description: Estatísticas gerais
            schema:
              type: object
              properties:
                total_books:
                  type: integer
                  example: 1000
                average_price:
                  type: number
                  example: 25.50
                rating_distribution:
                  type: object
                  example: {"1": 50, "2": 100, "3": 200, "4": 350, "5": 300}
          401:
            description: Token ausente ou inválido
          500:
            description: Erro ao calcular estatísticas
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
        Estatísticas agrupadas por categoria
        ---
        tags:
          - Stats
        security:
          - Bearer: []
        responses:
          200:
            description: Estatísticas por categoria
            schema:
              type: array
              items:
                type: object
                properties:
                  category:
                    type: string
                  total_books:
                    type: integer
                  avg_price:
                    type: number
                  min_price:
                    type: number
                  max_price:
                    type: number
          401:
            description: Token ausente ou inválido
          500:
            description: Erro ao calcular estatísticas
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
        Lista livros com melhor avaliação
        ---
        tags:
          - Books
        security:
          - Bearer: []
        responses:
          200:
            description: Livros com melhor rating
            schema:
              type: array
              items:
                type: object
          401:
            description: Token ausente ou inválido
          500:
            description: Erro ao buscar livros
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
        Filtra livros por faixa de preço
        ---
        tags:
          - Books
        security:
          - Bearer: []
        parameters:
          - name: min
            in: query
            type: number
            required: true
            description: Preço mínimo
            example: 10.00
          - name: max
            in: query
            type: number
            required: true
            description: Preço máximo
            example: 50.00
        responses:
          200:
            description: Livros na faixa de preço especificada
            schema:
              type: array
              items:
                type: object
          400:
            description: Parâmetros obrigatórios ausentes
          401:
            description: Token ausente ou inválido
          500:
            description: Erro ao filtrar livros
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