# WikiSearch 

This project is a Streamlit-based application that allows users to search for Wikipedia articles relevant to their text input. Users can upload a PDF, type text directly, and select the language for the Wikipedia search (English, Japanese, or French). The application then extracts the main content of the PDF or text input and uses LangChain with OpenAI’s API to fetch relevant Wikipedia articles

## Features

- Upload a PDF file or enter text as input.
- Automatically extract text from PDFs.
- Select the language for Wikipedia searches (English, Japanese, French).
- Fetches up to 3 relevant Wikipedia articles and displays the title and the first 100 words of each.
- Requires an OpenAI API Key for text processing.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/WikiSearch.git
    cd WikiSearch
    ```

2. **Install the required packages**:

    Make sure you have Python 3.7 or higher installed. Install the required dependencies using:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up Streamlit**:

    Run the Streamlit app:

    ```bash
    streamlit run main.py
    ```

## Usage

1. **API Key**: Enter your OpenAI API key when prompted. This key will be used to access OpenAI's language model for text processing.

2. **Select Input Type**:
    - **PDF**: Upload a PDF file, and the application will extract and display the main content. 
    - **Text**: Enter text directly into the input box.
    - Note that this programme cannot handle data of more than 5,000 words.
3. **Select Language**:
    - Choose the language for Wikipedia searches (English, Japanese, or French).

4. **View Results**:
    - The application will display up to 3 relevant Wikipedia articles with their titles and an excerpt of the first 100 words.

## Code Structure

- **main.py**: The main application file containing the Streamlit interface and LangChain configuration.
- **pdf_upload.py**: A helper class for handling PDF uploads and text extraction.
- **README.md**: Project documentation.


