import os
import sys
import getpass
import streamlit as st
from io import StringIO
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
import tempfile

Wikisearch_root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(Wikisearch_root_path)
import pdf_upload

load_dotenv()

# Streamlit interface for data type selection
data_type = st.radio('Select data type:', ['pdf', 'text'])

if data_type == 'pdf':
    # PDF file uploader appears if 'pdf' is selected
    PdfUpload = pdf_upload.pdf_upload()   #Initialise pdf_upload() 
    documents = PdfUpload.upload()
#    st.write(documents[0].page_content)
 
else:
    # Text input appears if 'text' is selected
    user_input = st.text_input("Enter your text here")
    if user_input:
        st.write("Text input received!")



