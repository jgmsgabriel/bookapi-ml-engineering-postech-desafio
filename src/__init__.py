from flasgger import Swagger
from .config import Config
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Carregar configurações no app.config para uso global
    app.config["BOOKS_CSV_PATH"] = Config.BOOKS_CSV_PATH
    app.config["JWT_SECRET"] = Config.JWT_SECRET
    app.config["JWT_ALGORITHM"] = Config.JWT_ALGORITHM
    app.config["JWT_EXP_DELTA_SECONDS"] = Config.JWT_EXP_DELTA_SECONDS

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
        "uiversion": 3,
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": Config.SWAGGER["title"],
            "version": "1.0.0",
            "description": "Catálogo API Scrape Books - Sistema de gerenciamento de livros com autenticação JWT",
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Token JWT de autenticação. Formato: Bearer {seu_token_jwt}",
            }
        },
        "basePath": "/",
        "schemes": ["https", "http"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    from . import main
    main.register_routes(app)
    return app