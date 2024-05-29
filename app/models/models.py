from app import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.String(50), unique=True, nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(50), nullable=True)
    reason = db.Column(db.Text, nullable=True)
