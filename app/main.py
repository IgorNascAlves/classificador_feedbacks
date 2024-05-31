import os
import atexit
import logging
import json

from flask import Flask
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from app.utils.email_utils import format_email_content


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa as extensões Flask
db = SQLAlchemy()
mail = Mail()

# Imports realizados apos a inicialização das extensões Flask para evitar erros de importação circular
from app.main import mail
from app.models.models import Feedback
from app.routes import api_bp

# Função para carregar os destinatários do arquivo JSON
def load_recipients():
    with open('recipients.json', 'r') as file:
        recipients_data = json.load(file)
        return recipients_data['recipients']

# Função para enviar o relatório semanal de feedbacks por e-mai
def send_weekly_report():   
    # Consulta os feedbacks dos últimos 7 dias
    feedbacks = Feedback.query.filter(Feedback.created_at >= datetime.now() - timedelta(days=7)).all()

    # Calcula as estatísticas dos feedbacks
    total_feedbacks = len(feedbacks)
    positive_feedbacks = len([f for f in feedbacks if f.sentiment == 'POSITIVO'])
    negative_feedbacks = len([f for f in feedbacks if f.sentiment == 'NEGATIVO'])

    if total_feedbacks > 0:
        positive_percentage = round((positive_feedbacks / total_feedbacks) * 100)
        negative_percentage = round((negative_feedbacks / total_feedbacks) * 100)
    else:
        positive_percentage = 0
        negative_percentage = 0

    # Conta as solicitações de características
    feature_requests = {}
    for feedback in feedbacks:
        code = feedback.code
        if code in feature_requests:
            feature_requests[code] += 1
        else:
            feature_requests[code] = 1

    # Classifica as características por número de solicitações
    sorted_features = sorted(feature_requests.items(), key=lambda item: item[1], reverse=True)

    # Formata o conteúdo do e-mail
    email_content = format_email_content(total_feedbacks, positive_percentage, negative_percentage, sorted_features)

    # Carrega os destinatários do arquivo JSON
    recipients = load_recipients()

    # Envia o e-mail com o relatório para os destinatários
    msg = Message(subject="Resumo Semanal dos Feedbacks",
                  sender=os.getenv('MAIL_USERNAME'),
                  recipients=recipients)
    msg.body = email_content
    mail.send(msg)

# Cria e configura o aplicativo Flask
def create_app(test_config=None):
    app = Flask(__name__)

    # Configurações do banco de dados e e-mail
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

    # Inicializa as extensões Flask
    db.init_app(app)
    mail.init_app(app)

    # Adicione logs para verificar a criação da tabela feedback
    logging.debug("Creating database tables...")
    with app.app_context():
        db.create_all()
        logging.debug("Database tables created.")

    # Cria as tabelas do banco de dados
    app.register_blueprint(api_bp)

    # Configura o agendador de tarefas para enviar o relatório semanal de feedbacks
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_weekly_report, trigger="interval", minutes=5)
    scheduler.start()

    # Envia o relatório imediatamente após iniciar a aplicação
    with app.app_context():
        send_weekly_report()

    # Registra uma função para desligar o agendador quando a aplicação é encerrada
    atexit.register(lambda: scheduler.shutdown())

    return app
