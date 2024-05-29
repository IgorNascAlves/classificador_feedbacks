from flask import Blueprint, request, jsonify
from app.utils.FeedbackAnalysisPipeline import analyze_sentiment
from app.models.models import Feedback, db

api_bp = Blueprint('api', __name__)

@api_bp.route('/feedbacks', methods=['POST'])
def analyze_feedback():
    data = request.json
    feedback_id = data.get('id')
    feedback_text = data.get('feedback')

    # Perform sentiment analysis
    sentiment, requested_features = analyze_sentiment(feedback_text)

    # Save feedback to database
    feedback = Feedback(
        feedback_id=feedback_id,
        feedback_text=feedback_text,
        sentiment=sentiment['sentiment'],
        code=requested_features.get('code'),
        reason=requested_features.get('reason')
    )
    db.session.add(feedback)
    db.session.commit()

    # Return the response in the desired format
    response_data = {
        "id": feedback_id,
        "sentiment": sentiment['sentiment'],
        "requested_features": requested_features
    }

    return jsonify(response_data)
