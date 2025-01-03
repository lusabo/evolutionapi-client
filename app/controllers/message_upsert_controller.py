import os
import tempfile
import logging
import requests
from openai import OpenAI

logger = logging.getLogger(__name__)
llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcrever_audio(url):
    try:
        # Baixando o áudio da URL
        response = requests.get(url, stream=True)

        # Criando um arquivo temporário para salvar o áudio
        with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as temp_audio_file:
            temp_audio_file.write(response.content)
            temp_audio_path = temp_audio_file.name


        # Lê o arquivo WAV convertido e envia para o Whisper
        with open(temp_audio_path, "rb") as audio_file:
            transcription = llm_client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        
        # Retorna o texto transcrito
        return transcription.text
    except Exception as e:
        return f"Erro ao processar o áudio: {e}"
    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
    
def process_message_upsert(data):
    """
    Processa os dados recebidos e aplica lógica dependendo se é texto ou áudio.
    Se for áudio, o mesmo será transcrito pelo Whisper antes de ser processado.
    """
    try:
        # Identificar se é áudio ou texto com base no conteúdo
        message_type = data.get('data', {}).get('messageType')

        if message_type == 'audioMessage':
            # Processar áudio
            logger.info("Mensagem do tipo áudio recebida.")
            audio_url = data['data']['message']['audioMessage']['url']

            # Transcrição usando Whisper            
            transcription = transcrever_audio(audio_url)

            logger.info(f"Transcrição do áudio: {transcription}")

            # Passar a transcrição para o primeiro guardrail
            result = transcription
        
        elif message_type == 'conversation':
            # Processar texto
            logger.info("Mensagem do tipo texto recebida.")
            conversation_text = data['data']['message']['conversation']

            # Passar o texto para o primeiro guardrail
            result = conversation_text
        
        else:
            logger.warning(f"Tipo de mensagem não suportado: {message_type}")
            result = {"error": "Unsupported message type"}

        return {"result": f"{result}"}

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")
        return {"error": f"Internal server error: {str(e)}"}