from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

app = FastAPI(
    title='Langchain server',
    version='1.0',
    description='A simple API server'
)

add_routes(
    app,
    ChatOpenAI(),
    path='/openai'
)

# 1st model
model1 = ChatOpenAI()
# 2nd model
model2 = OllamaLLM(model='llama3.2')

prompt1 = ChatPromptTemplate.from_template(
    'Write and essay about {topic} with 150 words')
prompt2 = ChatPromptTemplate.from_template(
    'Write a poem about {topic} in 100 words')

# Create API's

add_routes(
    app,
    prompt1 | model1,
    path='/essay'
)
add_routes(
    app,
    prompt2 | model2,
    path='/poem'
)

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
