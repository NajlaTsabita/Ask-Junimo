import streamlit as st

class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.messages = assistant.messages
        self.player_information = assistant.player_information

    def get_response(self, user_input):
        return self.assistant.get_response(user_input)

    def render_messages(self):
        messages = self.messages

        for message in messages:
            if message["role"] == "user":
               st.chat_message("human").markdown(message["content"])
            if message["role"] == "ai":
                st.chat_message("ai").markdown(message["content"])

    def set_state(self, key, value):
        st.session_state[key] = value

    def render_user_input(self):
        user_input = st.chat_input("Ask Junimo anything...", key="input")
        if user_input and user_input != "":
            st.chat_message("human").markdown(user_input)

            response_generator = self.get_response(user_input)

            with st.chat_message("ai"):
                response = st.write_stream(response_generator)

            self.messages.append({"role": "user", "content": user_input})
            self.messages.append({"role": "ai", "content": response})

            self.set_state("messages", self.messages)

    def render(self):
        with st.sidebar:
            st.logo("./data/stardew_logo.png")

            st.title("Ask Junimo")
            st.subheader("Player Information")
            if isinstance(self.player_information, dict):
                for key, value in self.player_information.items():
                    clean_key = str(key).replace("_", " ").title()
                    st.markdown(f"**{clean_key}:** {value}")
            else:
                st.write(self.player_information)

        self.render_messages()

        self.render_user_input()

    