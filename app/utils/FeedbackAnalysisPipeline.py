from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.pydantic_v1 import Field, BaseModel
from dotenv import load_dotenv
import os
from langchain.globals import set_debug

# Configurações iniciais
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ativação do modo de depuração
set_debug(True)

# Configuração do modelo de linguagem
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# Definição dos modelos de dados para os resultados de análise de sentimento e identificação de características
class SentimentResult(BaseModel):
    sentiment: str = Field(description="O sentimento detectado no feedback (POSITIVO, NEGATIVO e INCONCLUSIVO)")

class FeatureIdentificationResult(BaseModel):
    code: str = Field(description="Uma funcionalidade descrita em caixa alta (Exemplo: EDITAR_PERFIL)")
    reason: str = Field(description="A razão pela qual o usuário deseja essa funcionalidade")

# Configuração dos parsers de saída para análise de sentimento e identificação de características
parseador_sentiment = JsonOutputParser(pydantic_object=SentimentResult)
parseador_feature_identification = JsonOutputParser(pydantic_object=FeatureIdentificationResult)

# Definição dos modelos de prompt para análise de sentimento e identificação de características
modelo_sentimento = PromptTemplate(
    template="""Analisar o sentimento do seguinte feedback:
    {feedback}
    {formatacao_de_saida}
    """,
    input_variables=["feedback"],
    partial_variables={"formatacao_de_saida": parseador_sentiment.get_format_instructions()},
)

modelo_feature_identification = PromptTemplate(
    template="""Identificar características no seguinte feedback:
    {feedback}
    {formatacao_de_saida}
    """,
    input_variables=["feedback"],
    partial_variables={"formatacao_de_saida": parseador_feature_identification.get_format_instructions()},
)

modelo_email = PromptTemplate(
    template="""Melhore o texto do seguinte email para os stakeholders
do AluMind
    {email_content}
    """,
    input_variables=["email_content"],
)

# Configuração da cadeia de processamento para análise de sentimento e identificação de características
cadeia_sentimento = modelo_sentimento | llm | parseador_sentiment
cadeia_feature_identification = modelo_feature_identification | llm | parseador_feature_identification
cadeia_email = modelo_email | llm | StrOutputParser()

# Função para realizar a análise de sentimento de um texto de feedback
def analyze_sentiment(feedback_text):
    resultado = cadeia_sentimento.invoke(feedback_text), cadeia_feature_identification.invoke(feedback_text)
    return resultado

def email_pipeline(email_content):
    return cadeia_email.invoke(email_content)