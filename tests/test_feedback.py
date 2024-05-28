import pytest
from app import create_app
from flask import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        yield client

def test_analyze_feedback_positive(client):
    # Testando um feedback positivo
    feedback_data = {
        "id": "4042f20a-45f4-4647-8050-139ac16f610b",
        "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta"
    }

    response = client.post('/api/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
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

    response = client.post('/api/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
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

    response = client.post('/api/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
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

    response = client.post('/api/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
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

    response = client.post('/api/feedbacks', data=json.dumps(feedback_data), content_type='application/json')
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data['id'] == feedback_data['id']
    assert response_data['sentiment'] == 'NEGATIVO'
    assert response_data['requested_features']['code'] != ''
    assert response_data['requested_features']['reason'] != ''