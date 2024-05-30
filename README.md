# AluMind Feedback Classifier

A AluMind Feedback Classifier é uma aplicação desenvolvida para analisar feedbacks dos usuários, classificá-los por sentimento e identificar possíveis melhorias sugeridas. Além disso, a aplicação gera um relatório simples e envia um resumo semanal por email.

## Funcionalidades

1. **Classificação de Feedbacks**: Classifica os feedbacks recebidos em "POSITIVO", "NEGATIVO" e "INCONCLUSIVO".
2. **Relatório**: Gera um relatório que mostra a porcentagem de feedbacks positivos e negativos, além das funcionalidades mais pedidas.
3. **Resumo Semanal**: Envia um email semanal para stakeholders com um resumo dos principais feedbacks da semana.

## Estrutura do Projeto

```
classificador_feedbacks/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── models/
│   │   ├── models.py
│   │   └── __init__.py
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── scripts.js
│   ├── templates/
│   │   └── report.html
│   └── utils/
│       ├── email.py
│       ├── FeedbackAnalysisPipeline.py
│       └── __init__.py
├── scripts_python/
│   └── carga_banco.py
├── script_sql/
│   └── criacao_banco.sql
├── tests/
│   └── test_feedback.py
├── .env
├── .gitignore
├── README.md
├── recipients.json
├── requirements.txt
└── run.py
```

## Requisitos

- Python 3.11+
- MySQL

## Configuração

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/IgorNascAlves/classificador_feedbacks.git
   cd classificador_feedbacks
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .\.venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**

   - Certifique-se de ter o MySQL instalado e em execução.
   - Crie o banco de dados e a tabela necessária:

     ```bash
     mysql -u root -p < script_sql/criacao_banco.sql
     ```

5. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

   ```env
   GOOGLE_API_KEY=sua_api_key
   DATABASE_URL=mysql+pymysql://root:password@localhost/feedbacks_db
   MAIL_SERVER=smtp.seuservidor.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=seu_email@dominio.com
   MAIL_PASSWORD=sua_senha
   ```

6. **Configure os destinatários do email:**

   Edite o arquivo `recipients.json` com os emails dos stakeholders:

   ```json
   {
       "recipients": [
           "stakeholder1@dominio.com",
           "stakeholder2@dominio.com"
       ]
   }
   ```

## Executando a Aplicação

1. **Inicie o servidor:**

   ```bash
   python run.py
   ```

   O servidor estará em execução em `http://localhost:5000`.

2. **Envie feedbacks para análise:**

   Faça uma requisição POST para `http://localhost:5000/feedbacks` com o seguinte formato:

   ```json
   {
       "id": "4042f20a-45f4-4647-8050-139ac16f610b",
       "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta"
   }
   ```

3. **Acesse o relatório:**

   Abra `http://localhost:5000/report` no seu navegador para visualizar o relatório de feedbacks.

## Testes

Para executar os testes, use o pytest:

```bash
pytest
```

## Agendamento de Relatórios Semanais

A aplicação está configurada para enviar um relatório semanal por email usando APScheduler. Você pode ajustar o intervalo de tempo no arquivo `app/main.py`.

---
