import requests
import streamlit as st


def getOpenAI_response(input_text):
    response = requests.post('http://localhost:8000/essay/invoke',
                             json={'input' : {'topic':input_text}})
    return response.json()['output']['content']


def getLLama_response(input_text1):
    response = requests.post('http://localhost:8000/poem/invoke',
                             json={'input' : {'topic': input_text1}})
    return response.json()['output']

## Streamlit framework

st.title("Langchain Demo with API")
input_text = st.text_input("Write an essay on")
input_text1 = st.text_input('Write poem on')

if input_text:
    st.write(getOpenAI_response(input_text))

if input_text1:
    st.write(getLLama_response(input_text1))

