import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
# from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings  # Use HuggingFaceEmbeddings instead
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, user_template, bot_template
from langchain.llms import HuggingFaceHub



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

# def get_vectorstore(text_chunks):
#     # embeddings = OpenAIEmbeddings()
#     # embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vectorstore = FAISS.from_texts(texts = text_chunks, embedding =  embeddings )
#     return vectorstore

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    # Check the number of embeddings created
    with st.expander("Show/Hide embeddings"):
        st.write(f"Number of embeddings created: {len(text_chunks)}")
        # Print a sample embedding for the first chunk
        st.write(f"Sample embedding for first chunk: {vectorstore.index.reconstruct(0)}")
    return vectorstore

def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key = 'chat_history', return_messages = True )
    Conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm, 
        retriever = vectorstore.as_retriever(), 
        memory = memory 
    )
    return Conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    # st.write(response)
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()

    st.set_page_config(page_title = "Chat with multiple PDFs", page_icon = ":books:")

    st.write(css, unsafe_allow_html= True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header('Chat with the pdfs')
    user_question = st.text_input("Ask any question about ur pdf  :books::")
    if user_question:
        handle_userinput(user_question)


    st.write(user_template.replace("{{MSG}}", "Hi, I am Raghav"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hi, I am a bot"), unsafe_allow_html=True)

    
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
                        st.write(f"Number of text_chunks created: {len(text_chunks)}")
                        st.write(f"**Chunk {i+1}:**")
                        st.write(chunk)

                #creating the vector store to store the chunks
                vectorstore = get_vectorstore(text_chunks)


                #create the conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore) 


if __name__ == '__main__':
    main()

