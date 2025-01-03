import logging
from flask import Flask

def create_app():
    
    app = Flask(__name__)

    # Configuração de logging
    logging.basicConfig(
        level=logging.INFO,  # Configure o nível de log aqui (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    app.logger.info("Aplicação Flask iniciada.")
    
    # Registro de Blueprints
    from app.views.webhook_view import webhook_bp
    app.register_blueprint(webhook_bp)
    
    return app