import requests
import streamlit as st


def getOpenAI_response(input_text):
    response = requests.post('https://localhost:8000/essay/invoke',
                             json={'input' : {'topic':input_text}})
    return response.json()['output']['content']


def getLLama_response(input_text):
    response = requests.post('https://localhost:8000/poem/invoke',
                             json={'input' : {'topic': input_text}})
    return response.json()['output']

## Streamlit framework

st.title("Langchain Demo with API")
st.text