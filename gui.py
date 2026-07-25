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
            st.logo("./data/junimo.png")

            st.title("Ask Junimo")
            st.subheader("Player Information")

            player = self.player_information
            st.markdown(f"**👤 Name:** {player['player_name']}")
            st.markdown(f"**🏡 Farm:** {player['farm_name']} ({player['farm_type']})")
            st.markdown(f"**🗓️ Time:** {player['current_season']}, Year {player['current_year']}")
            st.markdown(f"**🐶 Pet:** {player['pet_type']}")
            st.markdown(f"**⭐ Favorite:** {player['favorite_thing']}")
            
  
            st.metric(label="💰 Current Gold", value=f"{player['current_gold']:,} G")

            with st.expander("💪 Player Skills (Level 1-10)"):
                st.caption(f"Farming (Lv {player['skills']['farming']})")
                st.progress(player['skills']['farming'] * 10) 
                
                st.caption(f"Mining (Lv {player['skills']['mining']})")
                st.progress(player['skills']['mining'] * 10)
                
                st.caption(f"Foraging (Lv {player['skills']['foraging']})")
                st.progress(player['skills']['foraging'] * 10)
                
                st.caption(f"Fishing (Lv {player['skills']['fishing']})")
                st.progress(player['skills']['fishing'] * 10)
                
                st.caption(f"Combat (Lv {player['skills']['combat']})")
                st.progress(player['skills']['combat'] * 10)

        self.render_messages()

        self.render_user_input()

    