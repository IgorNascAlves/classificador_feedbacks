from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import atexit
import logging


from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail
from app.utils.email import format_email_content

load_dotenv()

db = SQLAlchemy()
mail = Mail()

import json

def load_recipients():
    with open('recipients.json', 'r') as file:
        recipients_data = json.load(file)
        return recipients_data['recipients']


from flask_mail import Message
from dotenv import load_dotenv
import os
from app import mail
from app.models.models import Feedback
from datetime import datetime, timedelta

def send_weekly_report():
    


    feedbacks = Feedback.query.filter(Feedback.created_at >= datetime.now() - timedelta(days=7)).all()

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

    email_content = format_email_content(total_feedbacks, positive_percentage, negative_percentage, sorted_features)

    recipients = load_recipients()

    msg = Message(subject="Resumo Semanal dos Feedbacks",
                  sender=os.getenv('MAIL_USERNAME'),
                  recipients=recipients)
    msg.body = email_content
    mail.send(msg)

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
        app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    db.init_app(app)
    mail.init_app(app)

    # Adicione logs para verificar a criação da tabela feedback
    logging.debug("Creating database tables...")
    with app.app_context():
        db.create_all()
        logging.debug("Database tables created.")

    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_weekly_report, trigger="interval", weeks=1)
    scheduler.start()

    # # Envia o relatório imediatamente após iniciar a aplicação
    with app.app_context():
        send_weekly_report()

    atexit.register(lambda: scheduler.shutdown())

    return app
