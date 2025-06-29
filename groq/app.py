import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import time

from dotenv import load_dotenv
load_dotenv()

# load the GROQ API Key

groq_api_key = os.environ['GROQ_API_KEY']

if 'vectors' not in st.session_state:
    st.session_state.embeddings= OllamaEmbeddings(model='llama3.2')
    st.session_state.loader = WebBaseLoader('https://docs.smith.langchain.com')
    st.session_state.docs = st.session_state.loader.load()
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size= 1000, chunk_overlap= 200)
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
    st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

st.title("ChatGROQ Demo")
llm = ChatGroq(api_key=groq_api_key, model='deepseek-r1-distill-llama-70b')
prompt = ChatPromptTemplate.from_template(
"""
Answer the question based on the provided context only.
Please provide the most accurate response based on the question.
<context>
{context}
</context>
Questions: {input}
"""
)
document_chain = create_stuff_documents_chain(llm, prompt)
retreiver = st.session_state.vectors.as_retriever()
retreival_chain = create_retrieval_chain(retreiver, document_chain)

prompt = st.text_input('Enter the prompt here')

if prompt:
    start_time = time.process_time()
    response = retreival_chain.invoke({'input': 'prompt'}) 
    end_time = time.process_time()
    print("Response Time",start_time-end_time)
    st.write(response['answer'])

    # With a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")

