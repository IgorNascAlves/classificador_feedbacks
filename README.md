# Classificador de Feedbacks

Este projeto é um classificador de feedbacks que analisa o sentimento dos feedbacks dos usuários e identifica funcionalidades solicitadas. Utiliza Flask para criar uma API e LangChain para análise de sentimentos.

## Estrutura do Projeto

```
classificador_feedbacks/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── routes.py
│   ├── models/
│   │   └── models.py
│   └── config.py
├── tests/
│   └── test_feedbacks.py
├── run.py
├── .env
├── requirements.txt
└── README.md
```

## Endpoints da API

### Analisar Feedback

- **URL:** `/api/feedbacks`
- **Método:** `POST`
- **Content-Type:** `application/json`

#### Exemplo de Requisição

```json
{
    "id": "4042f20a-45f4-4647-8050-139ac16f610b",
    "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta."
}
```

#### Exemplo de Resposta

```json
{
    "id": "4042f20a-45f4-4647-8050-139ac16f610b",
    "sentiment": "POSITIVO"
}
```

## Estrutura dos Arquivos

### `app/__init__.py`

Define a criação do aplicativo Flask e a configuração básica.

### `app/api/routes.py`

Contém as rotas da API, incluindo a rota para analisar feedbacks.

### `app/models/models.py`

Implementa a lógica para analisar o sentimento dos feedbacks utilizando LangChain.

### `tests/test_feedbacks.py`

Contém testes para garantir que a análise de feedbacks está funcionando corretamente.

### `run.py`

Ponto de entrada do aplicativo Flask.