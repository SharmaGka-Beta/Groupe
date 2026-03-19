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
            FOREIGN KEY (user_id) REFERENCES user_info(user_id)         
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT exists drugs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            drug_name TEXT,
            qty INTEGER,
            FOREIGN KEY (user_id) REFERENCES user_info(user_id)         
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT exists others(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_name TEXT,
            qty INTEGER,
            FOREIGN KEY (user_id) REFERENCES user_info(user_id)         
        )
    """)

    conn.commit()
    conn.close()


def add_user(user_id: int):
    conn = sqlite3.connect(dbname)
    cursor = conn.execute(
        "SELECT * FROM user_info WHERE user_id = ?", (user_id,)
    )
    row = cursor.fetchone()

    if row is None:
        conn.execute(
            "INSERT INTO user_info (user_id) VALUES (?)", (user_id,)
        )
        conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = sqlite3.connect(dbname)
    cursor = conn.execute(
        "SELECT * FROM user_info WHERE user_id = ?", (user_id,)
    )
    row = cursor.fetchone()
    if row is None:
        add_user(user_id)
        return {"user_id": user_id, "money": 1000, "wanted": 0, "integrity": 0, "user_role": "civilian"}
    
    conn.close()
    return {"user_id": row[0], "money": row[1], "wanted": row[2], "integrity": row[3], "user_role": row[4]}

def get_inventory(uid):

    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    
    cursor.execute("""
        SELECT gun_name, qty
        FROM ammunitions
        WHERE user_id = ?
        """, (uid, )
    )

    guns = cursor.fetchall()

    cursor.execute("""
        SELECT drug_name, qty
        FROM drugs
        WHERE user_id = ?
        """, (uid, )
    )

    drugs = cursor.fetchall()

    cursor.execute("""
        SELECT item_name, qty
        FROM others
        WHERE user_id = ?
        """, (uid, )
    )

    items = cursor.fetchall()

    conn.close()
    return [guns, drugs, items]






