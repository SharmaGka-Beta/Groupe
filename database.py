import sqlite3

dbname = "SinCity.db"

def create_tables():

    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT exists user_info(
            user_id INTEGER PRIMARY KEY,
            money INTEGER DEFAULT 1000,
            wanted INTEGER DEFAULT 0 CHECK(wanted >= 0 AND wanted <= 100), 
            integrity INTEGER DEFAULT 0 CHECK(integrity >= 0 AND integrity <= 100),
            user_role TEXT DEFAULT "civilian"
        )  
    """)

    cursor.execute("""
        CREATE TABLE IF NOT exists ammunitions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            gun_name TEXT,
            qty INTEGER,
            FOREIGN_KEY (user_id) REFERENCES user_info(user_id)         
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT exists drugs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            drug_name TEXT,
            qty INTEGER,
            FOREIGN_KEY (user_id) REFERENCES user_info(user_id)         
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT exists others(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_name TEXT,
            qty INTEGER,
            FOREIGN_KEY (user_id) REFERENCES user_info(user_id)         
        )
    """)

    conn.commit()
    conn.close()

def add_user(user_id: int):
    conn = sqlite3.connect(dbname)
    cursor = conn.execute(
        "SELECT * FROM users WHERE user_id = ?", (user_id,)
    )
    row = cursor.fetchone()

    if row is None:
        conn.execute(
            "INSERT INTO users (user_id) VALUES (?)", (user_id,)
        )
        conn.commit()
        conn.close()
