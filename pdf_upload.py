# parameters: none
# Return: list[Document] (of Langchain)


import streamlit as st
from io import StringIO
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


import tempfile
import os



import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader

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
            pages = pdf_loader.load()

            # Concatenate all page content
            self.documents = "".join([page.page_content for page in pages])

            # Clean up the temporary file
            os.remove(tmp_file_path)

            # Display the content if within the acceptable length
            st.write(self.documents)
            st.write("PDF content loaded successfully!")
            return self.documents
