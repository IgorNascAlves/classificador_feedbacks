from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import Field, BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os
from langchain.globals import set_debug
set_debug(True)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

class SentimentResult(BaseModel):
    sentiment: str = Field(description="O sentimento detectado no feedback (POSITIVO, NEGATIVO e INCONCLUSIVO)")

class FeatureIdentificationResult(BaseModel):
    code: str = Field(description="Uma funcionalidade descrita em caixa alta (Exemplo: EDITAR_PERFIL)")
    reason: str = Field(description="A razão pela qual o usuário deseja essa funcionalidade")

llm = ChatGoogleGenerativeAI(model="gemini-pro")

parseador_sentiment = JsonOutputParser(pydantic_object=SentimentResult)
parseador_feature_identification = JsonOutputParser(pydantic_object=FeatureIdentificationResult)

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

# cadeia_sentimento = LLMChain(prompt=modelo_sentimento, llm=llm)
cadeia_sentimento = modelo_sentimento | llm | parseador_sentiment
cadeia_feature_identification = modelo_feature_identification | llm | parseador_feature_identification

def analyze_sentiment(feedback_text):
    resultado = cadeia_sentimento.invoke(feedback_text), cadeia_feature_identification.invoke(feedback_text)

    return resultado
