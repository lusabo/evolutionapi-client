from flask import Flask
import logging

def create_app():
    app = Flask(__name__)

    # Configuração de logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Registro de Blueprints
    from app.views.webhook_view import webhook_bp
    app.register_blueprint(webhook_bp)
    
    return app