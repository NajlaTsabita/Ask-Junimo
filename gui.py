import streamlit as st

class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.messages = assistant.messages
        self.player_information = assistant.player_information

    def render(self):
        with st.sidebar:
            st.logo("./data/stardew_logo.png")

            st.title("Ask Junimo")

    