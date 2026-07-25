import random
from faker import Faker
import streamlit as st

fake = Faker()

@st.cache_data(ttl=3600, show_spinner="Loading Player Data... ")
def generate_player_data(num_players=1):
    players = []
    for _ in range(num_players):

        player = {
            "player_id": fake.uuid4(),
            "player_name": fake.first_name(),
            "farm_name": f"{fake.word().capitalize()} Farm",
            "farm_type": random.choice([
                "Standard Farm", 
                "Riverland Farm", 
                "Forest Farm", 
                "Hill-top Farm", 
                "Wilderness Farm",
                "Four Corners Farm",
                "Beach Farm",
                "Meadowlands Farm"
            ]),
            "current_season": random.choice(["Spring", "Summer", "Fall", "Winter"]),
            "current_year": random.randint(1, 3),
            "current_gold": random.randint(1000, 50000),
            "favorite_thing": random.choice(["Stardew Valley", "Coffee", "Pizza", "Stardrop", 
                                             "Gaming", "Fishing", "Farming", "Mining", "Foraging", 
                                             "Combat", "Abigail", "Emily", "Leah", "Penny",
                                             "Maru", "Sam", "Sebastian", "Shane", "Harvey", 
                                             "Elliott", "Alex", "Haley", "Krobus"]),
            "pet_type": random.choice(["Dog", "Cat"]),
            "skills": {
                "farming": random.randint(1, 10),
                "mining": random.randint(1, 10),
                "foraging": random.randint(1, 10),
                "fishing": random.randint(1, 10),
                "combat": random.randint(1, 10)
            },
            "house_upgrade_level": random.randint(0, 3)
        }

        players.append(player)

    return players