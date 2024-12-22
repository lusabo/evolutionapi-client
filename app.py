from flask import Flask, request, jsonify
import logging
from datetime import datetime
import json
import os

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class EvolutionAPIClientWebhook:

    @staticmethod
    @app.route('/health', methods=['GET'])
    def health_check():
        response = {
            "status": "OK",
            "message": "Service is running",
        }
        return jsonify(response), 200

    @staticmethod
    @app.route('/evolutionapi-client/webhook/send-message', methods=['POST'])
    def webhook_send_message():
        try:
            if not request.is_json:
                logger.error("Payload não é JSON")
                return jsonify({'error': 'Content-Type deve ser application/json'}), 400

            data = request.get_json()
            
            # Log dos dados recebidos
            logger.info(f"Webhook SEND-MESSAGE recebido: {json.dumps(data, indent=2)}")
            
            return "Webhook SEND-MESSAGE", 200

        except Exception as e:
            logger.error(f"Erro ao processar webhook de envio: {str(e)}")
            return jsonify({'error': f'Erro interno: {str(e)}'}), 500
    
    @staticmethod
    @app.route('/evolutionapi-client/webhook/messages-upsert', methods=['POST'])
    def webhook_messages_upsert():
        try:
            if not request.is_json:
                logger.error("Payload não é JSON")
                return jsonify({'error': 'Content-Type deve ser application/json'}), 400

            data = request.get_json()
            
            # Log da mensagem recebida
            logger.info(f"Webhook MESSAGES-UPSERT recebido: {json.dumps(data, indent=2)}")
            
            return "Webhook MESSAGES-UPSERT", 200

        except Exception as e:
            logger.error(f"Erro ao processar webhook: {str(e)}")
            return jsonify({'error': f'Erro interno: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)