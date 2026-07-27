import streamlit as st
from data.database import delete_player
from player_form import render_player_form
import base64

def get_image_base64(img_path):
    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        return ""

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

            icon_name = get_image_base64("./data/The_Player_Icon.png")
            icon_farm = get_image_base64("./data/Standard_Farm_Map_Icon.png")
            icon_time = get_image_base64("./data/All_Seasons_Icon.png")
            icon_pet = get_image_base64("./data/White_Chicken.png")
            icon_fav = get_image_base64("./data/Favorite_Icon.png")
            icon_gold = get_image_base64("./data/Gold.png")
            
            st.markdown(f'<img src="data:image/png;base64,{icon_name}" width="22" style="vertical-align: middle; margin-right: 5px;"> **Name:** {player["player_name"]}', unsafe_allow_html=True)
            st.markdown(f'<img src="data:image/png;base64,{icon_farm}" width="22" style="vertical-align: middle; margin-right: 5px;"> **Farm:** {player["farm_name"]} ({player["farm_type"]})', unsafe_allow_html=True)
            st.markdown(f'<img src="data:image/png;base64,{icon_time}" width="22" style="vertical-align: middle; margin-right: 5px;"> **Time:** {player["current_season"]}, Year {player["current_year"]}', unsafe_allow_html=True)
            st.markdown(f'<img src="data:image/png;base64,{icon_pet}" width="22" style="vertical-align: middle; margin-right: 5px;"> **Pet:** {player["pet_type"]}', unsafe_allow_html=True)
            st.markdown(f'<img src="data:image/png;base64,{icon_fav}" width="22" style="vertical-align: middle; margin-right: 5px;"> **Favorite:** {player["favorite_thing"]}', unsafe_allow_html=True)
            st.markdown(f'<img src="data:image/png;base64,{icon_gold}" width="22" style="vertical-align: middle; margin-right: 5px;"> **Current Gold:** {player["current_gold"]:,} G', unsafe_allow_html=True)

            with st.expander("Player Skills (Level 1-10)"):
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

            with st.expander("Edit Player Data"):
                updated_player = render_player_form(
                    existing_player=player,
                    form_key="player_edit_form",
                    submit_label="Save Changes",
                )
                if updated_player:
                    st.session_state.player = updated_player
                    self.player_information = updated_player
                    self.assistant.player_information = updated_player
                    st.success("Player data has been updated!")
                    st.rerun()

            if st.button("Reset Player Data"):
                delete_player()
                st.session_state.clear()
                st.rerun()

        self.render_messages()

        self.render_user_input()