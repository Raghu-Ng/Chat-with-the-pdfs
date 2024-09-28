import streamlit as st

def main():
    st.set_page_config(page_title = "Chat with multiple PDFs", page_icon = ":books:")

    st.header('Chat with the pdfs')
    st.text_input("Ask any question about ur pdf  :books::")

    with st.sidebar:
        st.subheader("your Docs")
        st.file_uploader("upload the files here")
        st.button("process")
if __name__ == '__main__':
    main()