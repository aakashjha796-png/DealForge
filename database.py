import sqlite3


DATABASE_NAME = "dealforge.db"


def init_db():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_price REAL NOT NULL,
            discount_percent REAL NOT NULL,
            discount_amount REAL NOT NULL,
            final_price REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()