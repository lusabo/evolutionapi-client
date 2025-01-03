import os
import tempfile
import logging
import requests
from openai import OpenAI
from ..utils.whatsapp_decoder import download_using_enc_link

logger = logging.getLogger(__name__)
llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcrever_audio(decoded_audio_path):
    try:
        with open(decoded_audio_path, "rb") as audio_file:
            transcription = llm_client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        return transcription.text
    except Exception as e:
        return f"Erro ao processar o áudio: {e}"
    finally:
        if os.path.exists(decoded_audio_path):
            os.remove(decoded_audio_path)
    
def process_message_upsert(data):
    try:
        message_type = data.get('data', {}).get('messageType')

        if message_type == 'audioMessage':
            logger.info("Mensagem do tipo áudio recebida.")
            audio_payload = {
                'mediaKey': data['data']['message']['audioMessage']['mediaKey'],
                'url': data['data']['message']['audioMessage']['url'],
                'messageType': data['data']['messageType'],
                'whatsappTypeMessageToDecode': 'WhatsApp Audio Keys',
                'mimetype': data['data']['message']['audioMessage']['mimetype'],
            }

            decoded_audio_path = download_using_enc_link(audio_payload)
            logger.info(f"Áudio descriptografado salvo em: {decoded_audio_path}")

            transcription = transcrever_audio(decoded_audio_path)
            logger.info(f"Transcrição do áudio: {transcription}")

            result = transcription
        
        elif message_type == 'conversation':
            logger.info("Mensagem do tipo texto recebida.")
            conversation_text = data['data']['message']['conversation']
            result = conversation_text
        else:
            logger.warning(f"Tipo de mensagem não suportado: {message_type}")
            result = {"error": "Unsupported message type"}

        return {"result": f"{result}"}

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")
        return {"error": f"Internal server error: {str(e)}"}