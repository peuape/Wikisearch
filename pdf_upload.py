# parameters: none
# Return: list[Document] (of Langchain)


import streamlit as st
from io import StringIO
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os

class pdf_upload:
    def __init__(self):
        self.documents = None
    def upload(self):
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        if uploaded_file is not None:
        # Use a temporary file to save the uploaded file content
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
        
        # Load the PDF using PyPDFLoader with the temporary file path
            pdf_loader = PyPDFLoader(tmp_file_path)
            self.documents = pdf_loader.load()
        
            st.write("PDF content loaded successfully!")
        
        # Clean up the temporary file 
            os.remove(tmp_file_path)
            return self.documents