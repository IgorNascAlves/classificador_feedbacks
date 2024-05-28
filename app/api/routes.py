from flask import Blueprint, request, jsonify
from app.models.models import analyze_sentiment

# Criar um blueprint para as rotas da API
api_bp = Blueprint('api', __name__)

@api_bp.route('/feedbacks', methods=['POST'])
def analyze_feedback():
    data = request.json
    feedback_id = data.get('id')
    feedback_text = data.get('feedback')

    # Realizar análise de sentimento
    sentiment = analyze_sentiment(feedback_text)

    # Retornar a resposta com o formato desejado
    response_data = {
        "id": feedback_id,
        "sentiment": sentiment
    }

    return jsonify(response_data)

if __name__ == "__main__":
    api_bp.run(debug=True)
