import os
import sys
import getpass
import streamlit as st
from io import StringIO



from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent, load_tools
from langchain_core.prompts import ChatPromptTemplate

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

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Find up to 3 articles relavant to the user input. Provide the title and \
#the first 100 tokens of each article. Give the response in the JSON Format."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
tools = load_tools(["wikipedia"])
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke(
        {
            "input":text
        }
    )
# Display results
st.write("Wikipedia Search Results:")
st.write(response)




