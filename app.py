import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings  # Use HuggingFaceEmbeddings instead
from langchain.vectorstores import FAISS

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator= "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    # embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding =  embeddings )
    return vectorstore


def main():
    load_dotenv()

    st.set_page_config(page_title = "Chat with multiple PDFs", page_icon = ":books:")

    st.header('Chat with the pdfs')
    st.text_input("Ask any question about ur pdf  :books::")
    
    with st.sidebar:
        st.subheader("your Docs")
        pdf_docs = st.file_uploader("upload the files here", accept_multiple_files=True)
        if st.button("process"):
            with st.spinner("In progress...."):
                #getting the pdf 
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text)
                
                #making the chunks of the text
                text_chunks = get_text_chunks(raw_text)
                # Displaying chunks with an expander to show/hide
                with st.expander("Show/Hide Text Chunks"):
                    for i, chunk in enumerate(text_chunks):
                        st.write(f"**Chunk {i+1}:**")
                        st.write(chunk)

                #creating the vector store to store the chunks
                vectorstore = get_vectorstore(text_chunks)


if __name__ == '__main__':
    main()

