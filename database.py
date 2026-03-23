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
            user_role TEXT DEFAULT "civilian",
            jail INTEGER DEFAULT 0
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
        conn.close()
        return {"user_id": user_id, "money": 1000, "wanted": 0, "integrity": 0, "user_role": "civilian"}
        
    
    conn.close()
    return {"user_id": row[0], "money": row[1], "wanted": row[2], "integrity": row[3], "user_role": row[4], "jail": row[5]}

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

def update_inventory(user_id:int, item_name, item_category,  qt:int):
    column_name = ""

    conn = sqlite3.connect(dbname)
    if(item_category == "ammunitions"):
        column_name = "gun_name"
    elif(item_category == "drugs"):
        column_name = "drug_name"
    else:
        column_name = "item_name"


    existing = conn.execute(
        f"SELECT id FROM {item_category} WHERE user_id = ? AND {column_name} = ?",(user_id, item_name)).fetchone()


    if(existing):
        conn.execute(f"UPDATE {item_category} SET qty = qty + ? WHERE user_id = ? AND {column_name} = ?", (qt, user_id, item_name)) 
        conn.execute(f"DELETE FROM {item_category} WHERE user_id = ? AND {column_name} = ? AND qty = 0", (user_id, item_name))
    else:
        conn.execute(f"INSERT INTO {item_category} (user_id, {column_name}, qty) VALUES (?, ?, ?)", (user_id, item_name, qt))
    
    conn.commit()
    conn.close()
    


def add_money(user_id:int,amount:int ):
    conn = sqlite3.connect(dbname)
    conn.execute(
        "UPDATE user_info SET money= money+ ? WHERE user_id = ? ", (amount,user_id)
    )
    conn.commit()
    conn.close()

def remove_money(user_id:int,amount:int):

    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    try:
        try:
            cursor.execute(
                "UPDATE user_info SET money = money - ? WHERE user_id = ? ", (amount,user_id)
            )
        except sqlite3.IntegrityError:
            cursor.execute(
                "UPDATE user_info SET money = 0 WHERE user_id = ? ", (user_id,)
            )
        conn.commit()
    finally:
        conn.close()

def add_wanted(user_id, amount):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    try:
        try:
            cursor.execute(
                "UPDATE user_info SET wanted = wanted + ? WHERE user_id = ? ", (amount,user_id)
            )
        except sqlite3.IntegrityError:
            cursor.execute(
                "UPDATE user_info SET wanted = 100 WHERE user_id = ? ", (user_id,)
            )
        conn.commit()
    finally:
        conn.close()

def remove_wanted(user_id, amount):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    try:
        try:
            cursor.execute(
                "UPDATE user_info SET wanted = wanted - ? WHERE user_id = ? ", (amount,user_id)
            )
        except sqlite3.IntegrityError:
            cursor.execute(
                "UPDATE user_info SET wanted = 0 WHERE user_id = ? ", (user_id,)
            )
        conn.commit()
    finally:
        conn.close()

def add_integrity(user_id, amount):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    try:
        try:
            cursor.execute(
                "UPDATE user_info SET integrity = integrity + ? WHERE user_id = ? ", (amount,user_id)
            )
        except sqlite3.IntegrityError:
            cursor.execute(
                "UPDATE user_info SET integrity = 100 WHERE user_id = ? ", (user_id,)
            )
        conn.commit()
    finally:
        conn.close()

def remove_integrity(user_id, amount):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    try:
        try:
            cursor.execute(
                "UPDATE user_info SET integrity = integrity - ? WHERE user_id = ? ", (amount,user_id)
            )
        except sqlite3.IntegrityError:
            cursor.execute(
                "UPDATE user_info SET integrity = 0 WHERE user_id = ? ", (user_id,)
            )
        conn.commit()
    finally:
        conn.close()

def update_jail(uid, val):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute("UPDATE user_info SET jail = ? WHERE user_id = ?", (val, uid))

    conn.close()

def update_role(uid, role):

    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute("UPDATE user_info SET user_role = ? WHERE user_id = ?", (role, uid))

    conn.commit()
    conn.close()


