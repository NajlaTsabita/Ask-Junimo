import streamlit as st
from data.database import save_player

FARM_TYPES = [
    "Standard Farm",
    "Riverland Farm",
    "Forest Farm",
    "Hill-top Farm",
    "Wilderness Farm",
    "Four Corners Farm",
    "Beach Farm",
    "Meadowlands Farm",
]

SEASONS = ["Spring", "Summer", "Fall", "Winter"]
PET_TYPES = ["Dog", "Cat", "None"]


def _build_player_dict(values):
    return {
        "player_name": values["player_name"].strip(),
        "farm_name": values["farm_name"].strip(),
        "farm_type": values["farm_type"],
        "current_season": values["current_season"],
        "current_year": values["current_year"],
        "current_gold": values["current_gold"],
        "favorite_thing": values["favorite_thing"].strip(),
        "pet_type": values["pet_type"],
        "skills": {
            "farming": values["farming"],
            "mining": values["mining"],
            "foraging": values["foraging"],
            "fishing": values["fishing"],
            "combat": values["combat"],
        },
        "house_upgrade_level": values["house_upgrade_level"],
    }


def render_player_form(existing_player=None, form_key="player_setup_form", submit_label="Simpan & Mulai Main"):
    """
    Renders the input form. Returns the saved player dict once the user
    submits successfully, otherwise returns None (form is still showing).

    `existing_player` pre-fills the form — used for the "edit" flow so the
    user doesn't have to retype everything.
    """
    defaults = existing_player or {}
    default_skills = defaults.get("skills", {})

    with st.form(key=form_key, clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            player_name = st.text_input(
                "Nama Pemain",
                value=defaults.get("player_name", ""),
                placeholder="mis. Andi",
            )
            farm_name = st.text_input(
                "Nama Farm",
                value=defaults.get("farm_name", ""),
                placeholder="mis. Rejeki Farm",
            )
            farm_type = st.selectbox(
                "Tipe Farm",
                FARM_TYPES,
                index=FARM_TYPES.index(defaults["farm_type"]) if defaults.get("farm_type") in FARM_TYPES else 0,
            )
            current_season = st.selectbox(
                "Musim Saat Ini",
                SEASONS,
                index=SEASONS.index(defaults["current_season"]) if defaults.get("current_season") in SEASONS else 0,
            )
            current_year = st.number_input(
                "Tahun Saat Ini (in-game)",
                min_value=1, max_value=99,
                value=int(defaults.get("current_year", 1)),
            )

        with col2:
            current_gold = st.number_input(
                "Gold Saat Ini",
                min_value=0,
                value=int(defaults.get("current_gold", 500)),
                step=100,
            )
            favorite_thing = st.text_input(
                "Hal/Karakter Favorit (opsional)",
                value=defaults.get("favorite_thing", ""),
                placeholder="mis. Abigail, Fishing, Coffee",
            )
            pet_type = st.selectbox(
                "Hewan Peliharaan",
                PET_TYPES,
                index=PET_TYPES.index(defaults["pet_type"]) if defaults.get("pet_type") in PET_TYPES else 0,
            )
            house_upgrade_level = st.selectbox(
                "Level Upgrade Rumah",
                [0, 1, 2, 3],
                index=int(defaults.get("house_upgrade_level", 0)),
            )

        st.markdown("**💪 Skill (Level 1-10)**")
        s1, s2, s3, s4, s5 = st.columns(5)
        with s1:
            farming = st.slider("Farming", 1, 10, int(default_skills.get("farming", 1)))
        with s2:
            mining = st.slider("Mining", 1, 10, int(default_skills.get("mining", 1)))
        with s3:
            foraging = st.slider("Foraging", 1, 10, int(default_skills.get("foraging", 1)))
        with s4:
            fishing = st.slider("Fishing", 1, 10, int(default_skills.get("fishing", 1)))
        with s5:
            combat = st.slider("Combat", 1, 10, int(default_skills.get("combat", 1)))

        submitted = st.form_submit_button(submit_label)

        if submitted:
            if not player_name.strip() or not farm_name.strip():
                st.error("Nama Pemain dan Nama Farm wajib diisi ya!")
                return None

            player = _build_player_dict({
                "player_name": player_name,
                "farm_name": farm_name,
                "farm_type": farm_type,
                "current_season": current_season,
                "current_year": current_year,
                "current_gold": current_gold,
                "favorite_thing": favorite_thing,
                "pet_type": pet_type,
                "farming": farming,
                "mining": mining,
                "foraging": foraging,
                "fishing": fishing,
                "combat": combat,
                "house_upgrade_level": house_upgrade_level,
            })

            save_player(player)
            return player

    return None


def render_onboarding_screen():
    """Full-page setup screen shown the first time (no player saved yet)."""
    st.title("🌾 Selamat Datang di Ask Junimo!")
    st.markdown(
        "Sebelum mulai, ceritakan dulu soal farm kamu. "
        "Data ini akan disimpan secara lokal dan dipakai Junimo Bot "
        "untuk memberi saran yang sesuai kondisi farm-mu — jadi kamu **tidak perlu isi ulang** setiap kali membuka aplikasi."
    )

    player = render_player_form(form_key="player_setup_form")

    if player:
        st.session_state.player = player
        st.success("Data tersimpan! Memuat Ask Junimo...")
        st.rerun()
