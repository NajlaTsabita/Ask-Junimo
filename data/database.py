import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "player.db")


def _get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=DB_PATH):
    conn = _get_connection(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                player_name TEXT NOT NULL,
                farm_name TEXT NOT NULL,
                farm_type TEXT NOT NULL,
                current_season TEXT NOT NULL,
                current_year INTEGER NOT NULL,
                current_gold INTEGER NOT NULL,
                favorite_thing TEXT,
                pet_type TEXT,
                farming INTEGER NOT NULL,
                mining INTEGER NOT NULL,
                foraging INTEGER NOT NULL,
                fishing INTEGER NOT NULL,
                combat INTEGER NOT NULL,
                house_upgrade_level INTEGER NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def get_player(db_path=DB_PATH):
    conn = _get_connection(db_path)
    try:
        row = conn.execute("SELECT * FROM player WHERE id = 1").fetchone()
    finally:
        conn.close()

    if row is None:
        return None

    return {
        "player_name": row["player_name"],
        "farm_name": row["farm_name"],
        "farm_type": row["farm_type"],
        "current_season": row["current_season"],
        "current_year": row["current_year"],
        "current_gold": row["current_gold"],
        "favorite_thing": row["favorite_thing"],
        "pet_type": row["pet_type"],
        "skills": {
            "farming": row["farming"],
            "mining": row["mining"],
            "foraging": row["foraging"],
            "fishing": row["fishing"],
            "combat": row["combat"],
        },
        "house_upgrade_level": row["house_upgrade_level"],
    }


def save_player(player, db_path=DB_PATH):
    conn = _get_connection(db_path)
    try:
        conn.execute(
            """
            INSERT INTO player (
                id, player_name, farm_name, farm_type, current_season,
                current_year, current_gold, favorite_thing, pet_type,
                farming, mining, foraging, fishing, combat, house_upgrade_level
            ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                player_name=excluded.player_name,
                farm_name=excluded.farm_name,
                farm_type=excluded.farm_type,
                current_season=excluded.current_season,
                current_year=excluded.current_year,
                current_gold=excluded.current_gold,
                favorite_thing=excluded.favorite_thing,
                pet_type=excluded.pet_type,
                farming=excluded.farming,
                mining=excluded.mining,
                foraging=excluded.foraging,
                fishing=excluded.fishing,
                combat=excluded.combat,
                house_upgrade_level=excluded.house_upgrade_level
            """,
            (
                player["player_name"],
                player["farm_name"],
                player["farm_type"],
                player["current_season"],
                player["current_year"],
                player["current_gold"],
                player.get("favorite_thing"),
                player.get("pet_type"),
                player["skills"]["farming"],
                player["skills"]["mining"],
                player["skills"]["foraging"],
                player["skills"]["fishing"],
                player["skills"]["combat"],
                player["house_upgrade_level"],
            ),
        )
        conn.commit()
    finally:
        conn.close()


def delete_player(db_path=DB_PATH):
    conn = _get_connection(db_path)
    try:
        conn.execute("DELETE FROM player WHERE id = 1")
        conn.commit()
    finally:
        conn.close()