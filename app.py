
from data.player import generate_player_data
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import logging
from assistant import Assistant
from gui import AssistantGUI
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE
from langchain_groq import ChatGroq


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    st.set_page_config(page_title="Aks Junimo", layout="wide")

    @st.cache_data(ttl=3600, show_spinner="Loading Player Data... ")
    def get_player_data():
        return generate_player_data(1)[0]

    @st.cache_resource(ttl=3600, show_spinner="Initializing Vector Store... ")
    def init_vectore_store(pdf_path):
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)

            embaddings_function = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
            persistent_path = "./data/vectorstore" 

            vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=embaddings_function,
                persist_directory=persistent_path
            )

            return vectorstore
        except Exception as e:
            logging.error(f"Error initializing vector store: {str(e)}")
            st.error(f"Failed to initialize vector store: {str(e)}")
            return None

    player_data = get_player_data()
    vector_store = init_vectore_store("data/Stardew_Valley_Wiki.pdf")

    if "player" not in st.session_state:
        st.session_state.player = player_data
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": WELCOME_MESSAGE}]

    llm = ChatGroq(model="openai/gpt-oss-120b")

    assistant = Assistant(
        system_prompt=SYSTEM_PROMPT,
        llm=llm,
        message_history=st.session_state.messages,
        player_information=st.session_state.player,
        vector_store=vector_store,
    )

    gui = AssistantGUI(assistant)
    gui.render()