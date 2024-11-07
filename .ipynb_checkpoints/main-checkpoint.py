import os
import sys
import getpass
import streamlit as st
from io import StringIO
from langchain_text_splitters import RecursiveCharacterTextSplitter 
import tempfile

from langchain.agents import initialize_agent, AgentType
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Set the API key as an environment variable if provided
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    st.success("API key has been set successfully!")
else:
    st.warning("Please enter your OpenAI API key to proceed.")

Wikisearch_root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(Wikisearch_root_path)

import pdf_upload




# Streamlit interface for data type selection
data_type = st.radio('Select data type:', ['pdf', 'text'])

if data_type == 'pdf':
    PdfUpload = pdf_upload.pdf_upload()   #Initialise pdf_upload() 
    text = PdfUpload.upload()
else:
    text = st.text_input("Enter your text here")
    st.write("Text input received!")
    

# Initialise the Wikipedia tool
wikipedia_tool = WikipediaAPIWrapper()

# Define a LangChain agent with the Wikipedia tool
tools = [Tool.from_function(func=wikipedia_tool.run, name="Wikipedia Search", description="Search Wikipedia articles")]

model = ChatOpenAI(model="gpt-3.5-turbo")
# Initialise the agent
agent = initialize_agent(tools, llm=model, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

response = agent({"input": text})


# Display results
st.write("Wikipedia Search Results:")
st.write(response)




