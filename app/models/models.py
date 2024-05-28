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

llm = ChatGoogleGenerativeAI(model="gemini-pro")

parseador = JsonOutputParser(pydantic_object=SentimentResult)

modelo_sentimento = PromptTemplate(
    template="""Analisar o sentimento do seguinte feedback:
    {feedback}
    {formatacao_de_saida}
    """,
    input_variables=["feedback"],
    partial_variables={"formatacao_de_saida": parseador.get_format_instructions()},
)

# cadeia_sentimento = LLMChain(prompt=modelo_sentimento, llm=llm)
cadeia_sentimento = modelo_sentimento | llm | parseador

def analyze_sentiment(feedback_text):
    resultado = cadeia_sentimento.invoke(feedback_text)
    return resultado['sentiment']
