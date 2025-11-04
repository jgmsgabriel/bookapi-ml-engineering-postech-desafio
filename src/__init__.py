from flasgger import Swagger
from .config import Config
from flask import Flask

def create_app():
    app = Flask(__name__)

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
        # uiversion 3 = Swagger UI v3 renderizando um spec Swagger 2.0 (ok)
        "uiversion": Config.SWAGGER["uiversion"],
    }

    swagger_template = {
        "swagger": "2.0",   # <-- use APENAS Swagger 2.0
        "info": {
            "title": Config.SWAGGER["title"],
            "version": "1.0.0",
            "description": "Catálogo API Scrape Books",
        },
        # Definição do Bearer para funcionar com `security: [Bearer: []]`
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT no formato: Bearer <token>",
            }
        },
        # Opcional: segurança global (pode manter por-endpoint nos docstrings se preferir)
        # "security": [{"Bearer": []}],
        "basePath": "/",  # ajuste se sua app estiver sob subcaminho
        "schemes": ["https", "http"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    from . import main
    main.register_routes(app)
    return app