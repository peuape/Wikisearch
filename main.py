# Import necessary modules
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import json
import pdf_upload


# API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    st.success("API key has been set successfully!")
else:
    st.warning("Please enter your OpenAI API key to proceed.")

# Streamlit Interface
data_type = st.radio('Select data type:', ['pdf', 'text'])
if data_type == 'pdf':
    PdfUpload = pdf_upload.pdf_upload()  # Initialize pdf_upload
    text = PdfUpload.upload()  # Upload and extract text from PDF
else:
    text = st.text_input("Enter your text here")  # Text input for users

language = st.radio('Select language:', ['English', '日本語', 'français'])

# Helper function to find the fourth occurrence of a substring
def find_fourth_occurrence(main_str, sub_str):
    first_occurrence = main_str.find(sub_str)
    second_occurrence = main_str.find(sub_str, first_occurrence + 1)
    third_occurrence = main_str.find(sub_str, second_occurrence + 1)
    fourth_occurrence = main_str.find(sub_str, third_occurrence + 1)
    return fourth_occurrence

# Define the ChatOpenAI model
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def translate_input(text, selected_language):
    # Define a prompt for translation
    translation_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant who translates queries into the user's selected language if they are different."
            ),
            ("human", f"User selected language: {selected_language}. Input text: {text}.")
        ]
    )

    # Convert the ChatPromptTemplate to a PromptValue
    prompt_value = translation_prompt.format_prompt()

    # Generate the response
    response = model.generate([prompt_value])
    # Access the first generation's text and strip whitespace
    translated_text = response.generations[0][0].text.strip()
    return translated_text


# Define the main Wikipedia search prompt
search_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Show the title and the first 100 words of 3 Wikipedia articles relevant to the user input. "
            "Provide the response in JSON format with keys 'article1', 'article2', and 'article3'. "
            "Each article should have 'title' and 'content'. If no articles are found, set 'title' to "
            "'No articles found' and leave 'content' empty."
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

# Language-based Wikipedia tool
if language == "English":
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="en"))
elif language == "日本語":
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="ja"))
elif language == "français":
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="fr"))

# Define the Wikipedia search agent
search_agent = create_tool_calling_agent(
    llm=model,
    tools=[wikipedia_tool],
    prompt=search_prompt
)

# Create the search executor
search_executor = AgentExecutor(agent=search_agent, tools=[wikipedia_tool], verbose=True)

# Handle user input and run the chain
if text:
    # Step 1: Translate the input if needed
    translated_input = translate_input(text, language)

    # Step 2: Search Wikipedia using the translated input
    response = search_executor.invoke({"input": translated_input})["output"]

    # Process and display the response
    response = response[response.index("{"):]  # Extract JSON portion
    if response.count("}") > 3:
        json_end = find_fourth_occurrence(response, "}")
        response = response[:json_end + 1]
    try:
        response_dict = json.loads(response)
        for i in range(1, 4):
            article_key = f"article{i}"
            if article_key in response_dict:
                st.write(f"## Title: {response_dict[article_key]['title']}")
                st.write(f"## Content: {response_dict[article_key]['content']}")
    except json.JSONDecodeError:
        st.error("Failed to parse response as JSON. Please check the format.")