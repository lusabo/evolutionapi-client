from flask import Flask

def create_app():
    
    app = Flask(__name__)
    
    # Registro de Blueprints
    from app.views.webhook_view import webhook_bp
    app.register_blueprint(webhook_bp)
    
    return app