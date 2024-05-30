import requests
import json

# URL of the API endpoint
url = 'http://localhost:5000/feedbacks'

# List of feedback examples
feedbacks = [
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f610a",
        "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta."
    },
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f610b",
        "feedback": "Não gostei do Alumind. Encontrei muitos problemas e não consegui resolver nada com ele. A edição do perfil é muito complicada."
    },
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f610c",
        "feedback": "O Alumind é bom em alguns aspectos, mas ruim em outros. Não sei se continuarei a usar."
    },
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f610d",
        "feedback": "O Alumind tem potencial, mas precisa de muitas melhorias. A interface é confusa e alguns recursos são difíceis de encontrar."
    },
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f610e",
        "feedback": "Excelente ferramenta! Ajudou-me a organizar melhor minhas tarefas diárias."
    },
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f610f",
        "feedback": "Péssima experiência. Muitos bugs e a performance é lenta."
    },
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f6110",
        "feedback": "É um aplicativo mediano. Tem boas ideias, mas a execução deixa a desejar."
    },
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f6111",
        "feedback": "Não é muito intuitivo, mas depois que você se acostuma, funciona bem."
    },
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f6112",
        "feedback": "Adoro usar o Alumind, mas gostaria de mais opções de personalização."
    },
    {
        "id": "4042f20a-45f4-4647-8050-139ac16f6113",
        "feedback": "Muito bom! A interface é amigável e os recursos são úteis."
    }
]

# Function to send a POST request with the given feedback
def send_feedback(feedback):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(feedback), headers=headers)
    return response

# Send all feedbacks to the API endpoint
for feedback in feedbacks:
    response = send_feedback(feedback)
    print(f'Status Code: {response.status_code}')
    print(f'Response Data: {response.json()}')
