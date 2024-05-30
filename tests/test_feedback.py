import pytest
from app import create_app, db
from flask import json


@pytest.fixture
def app():
    # Cria uma instância do aplicativo configurada para testes
    app = create_app({
        'TESTING': True,  # Ativa o modo de teste
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Usa um banco de dados em memória para testes
        'SQLALCHEMY_TRACK_MODIFICATIONS': False  # Desativa a modificação de rastreamento do SQLAlchemy
    })

    # Dentro do contexto do aplicativo
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados
        yield app  # Fornece a instância do aplicativo para os testes
        db.drop_all()  # Remove todas as tabelas após os testes

@pytest.fixture
def client(app):
    # Cria um cliente de teste para fazer solicitações à aplicação
    return app.test_client()

@pytest.fixture
def runner(app):
    # Cria um runner de teste para executar comandos CLI
    return app.test_cli_runner()


def test_analyze_feedback_positive(client):
    # Testando um feedback positivo
    feedback_data = {
        "id": "4042f20a-45f4-4647-8050-139ac16f610b",
        "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta"
    }

    response = client.post('/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data['id'] == feedback_data['id']
    assert response_data['sentiment'] == 'POSITIVO'

def test_analyze_feedback_negative(client):
    # Testando um feedback negativo
    feedback_data = {
        "id": "4042f20a-45f4-4647-8050-139ac16f610c",
        "feedback": "Não gostei do Alumind. Encontrei muitos problemas e não consegui resolver nada com ele. A edição do perfil é muito complicada."
    }

    response = client.post('/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data['id'] == feedback_data['id']
    assert response_data['sentiment'] == 'NEGATIVO'

def test_analyze_feedback_inconclusive(client):
    # Testando um feedback inconclusivo
    feedback_data = {
        "id": "4042f20a-45f4-4647-8050-139ac16f610d",
        "feedback": "O Alumind é bom em alguns aspectos, mas ruim em outros. Não sei se continuarei a usar."
    }

    response = client.post('/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data['id'] == feedback_data['id']
    assert response_data['sentiment'] == 'INCONCLUSIVO'

def test_analyze_feedback_feature_identification(client):
    # Testando a identificação de características no feedback
    feedback_data = {
        "id": "4042f20a-45f4-4647-8050-139ac16f610e",
        "feedback": """
                    Gosto muito de usar o Alumind! Está me ajudand
                    o bastante em relação a alguns problemas que tenho. Só quer
                    ia que houvesse uma forma mais fácil de eu mesmo realizar a
                    edição do meu perfil dentro da minha conta"""
    }

    response = client.post('/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data['id'] == feedback_data['id']
    assert response_data['sentiment'] == 'POSITIVO'
    assert response_data['requested_features']['code'] == 'EDITAR_PERFIL'
    assert response_data['requested_features']['reason'] != ''

def test_analyze_feedback_feature_identification_negative(client):
    # Testando a identificação de características no feedback
    feedback_data = {
        "id": "4042f20a-45f4-4647-8050-139ac16f610f",
        "feedback": """
                    Não gostei do Alumind. Encontrei muitos problemas e não consegui resolver nada com ele. Assistir as aulas é muito complicado."""
    }

    response = client.post('/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data['id'] == feedback_data['id']
    assert response_data['sentiment'] == 'NEGATIVO'
    assert response_data['requested_features']['code'] != ''
    assert response_data['requested_features']['reason'] != ''