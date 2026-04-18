import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. Configure sua API Key do Google Gemini
genai.configure(api_key="SUA_CHAVE_API_AQUI")
model = genai.GenerativeModel('gemini-pro')

@app.route('/alexa', methods=['POST'])
def alexa_skill():
    # Recebe a requisição da Alexa
    req_data = request.get_json()
    
    # Extrai a pergunta do usuário (vinda do Intent configurado na Skill)
    try:
        user_query = req_data['request']['intent']['slots']['pergunta']['value']
    except (KeyError, TypeError):
        user_query = "Olá, como posso ajudar?"

    # Envia para o Gemini
    response = model.generate_content(user_query)
    answer = response.text

    # Formata a resposta no padrão exigido pela Alexa
    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": answer
            },
            "shouldEndSession": True
        }
    })

if __name__ == '__main__':
    # Rodando na porta 5000
    app.run(port=5000)
