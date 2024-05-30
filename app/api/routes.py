from flask import Blueprint, request, jsonify, render_template
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

@api_bp.route('/report', methods=['GET'])
def feedback_report():
    feedbacks = Feedback.query.all()

    total_feedbacks = len(feedbacks)
    positive_feedbacks = len([f for f in feedbacks if f.sentiment == 'POSITIVO'])
    negative_feedbacks = len([f for f in feedbacks if f.sentiment == 'NEGATIVO'])

    if total_feedbacks > 0:
        positive_percentage = round((positive_feedbacks / total_feedbacks) * 100)
        negative_percentage = round((negative_feedbacks / total_feedbacks) * 100)
    else:
        positive_percentage = 0
        negative_percentage = 0

    feature_requests = {}
    for feedback in feedbacks:
        code = feedback.code
        if code in feature_requests:
            feature_requests[code] += 1
        else:
            feature_requests[code] = 1

    sorted_features = sorted(feature_requests.items(), key=lambda item: item[1], reverse=True)

    return render_template('report.html', 
                            total_feedbacks=total_feedbacks, 
                            positive_percentage=positive_percentage,
                            negative_percentage=negative_percentage, 
                            sorted_features=sorted_features, 
                            feedbacks=feedbacks)
