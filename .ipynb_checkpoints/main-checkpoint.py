import os
import sys
import getpass
import streamlit as st
from io import StringIO



from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent, load_tools
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import json

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

language = st.radio('Select language:', ['English', '日本語', 'français'])

def find_fourth_occurrence(main_str, sub_str):  #a function to find the fourth occurrence of a substring in a string. 
    first_occurrence = main_str.find(sub_str)
    second_occurrence = main_str.find(sub_str, first_occurrence + 1)
    third_occurrence = main_str.find(sub_str, second_occurrence + 1)
    fourth_occurrence = main_str.find(sub_str, third_occurrence + 1)
    return fourth_occurrence

max_word_limit = 5000  # Adjust this based on the model's token context
if text != None and len(text) > max_word_limit:
    st.error("The data is too large to process. Please upload a shorter document.")
    

else:# Define your model and prompt
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 'Show the title and the first 100 words of 3 Wikipedia articles relevant to the user input. \
        Give the response in the JSON format. The keys of each article must be "article1", "article2" ,"article3", \
        and the names of the keys indicating the title and the content of each article must be "title" and "content". \
        Follow this format no matter what.\
        If no articles are found, put "No articles found" in the title key, and leave the content key empty.'),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
    )




# Set language for WikipediaQueryRun based on user selection
    if language == "English":
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="en"))
    elif language == "日本語":
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="ja"))
    elif language == "français":
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="fr"))

# Create agent and agent executor
    agent = create_tool_calling_agent(model, [wikipedia_tool], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[wikipedia_tool], verbose=True)
    
    if text:
        response = agent_executor.invoke({"input": text})["output"]
        #Make the response a neat json file
        response = response[response.index("{"):]
        if response.count("}") > 3:
            json_end = find_fourth_occurrence(response, "}")
            response = response[:json_end+1]
        try:
            if response != "No articles found":
                response_dict = json.loads(response)
      
                for i in range(len(response_dict)):
                    st.write("## title")
                    st.write(response_dict[f"article{1+i}"]["title"])
                    st.write("## content")
                    st.write(response_dict[f"article{1+i}"]["content"])
            else:
                st.write("No articles found")
            
        except json.JSONDecodeError:
            st.error("Failed to parse response as JSON. Please check the format of the response.")
        



