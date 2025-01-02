from flask import Blueprint, request, jsonify
import logging
import json

# Configuração do logging
logger = logging.getLogger(__name__)

# Definindo o Blueprint
webhook_bp = Blueprint("webhook", __name__, url_prefix="/evolutionapi-client/webhook")

def process_message(data):
    """
    Função fictícia para processar mensagens recebidas.
    """
    logger.info("Processando mensagem: %s", data)
    return {"status": "processed"}

@webhook_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar a saúde do serviço.
    """
    response = {
        "status": "OK",
        "message": "Service is running",
    }
    return jsonify(response), 200

@webhook_bp.route('/send-message', methods=['POST'])
def webhook_send_message():
    """
    Endpoint para o webhook de envio de mensagens.
    """
    try:
        if not request.is_json:
            logger.error("Payload não é JSON")
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400

        data = request.get_json()
        
        logger.info(f"Webhook SEND-MESSAGE recebido: {json.dumps(data, indent=2)}")
        
        return "Webhook SEND-MESSAGE", 200

    except Exception as e:
        logger.error(f"Erro ao processar webhook de envio: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@webhook_bp.route('/messages-upsert', methods=['POST'])
def webhook_messages_upsert():
    """
    Endpoint para o webhook de atualização de mensagens.
    """
    try:
        if not request.is_json:
            logger.error("Payload não é JSON")
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400

        data = request.get_json()
        
        logger.info(f"Webhook MESSAGES-UPSERT recebido: {json.dumps(data, indent=2)}")

        return "Webhook MESSAGES-UPSERT", 200

    except Exception as e:
        logger.error(f"Erro ao processar webhook: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500
