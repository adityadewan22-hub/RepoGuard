import psycopg2
import os

connect=psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db():
    with connect.cursor() as cur:
     cur.execute("""
        CREATE TABLE IF NOT EXISTS doc_chunks(
                id SERIAL PRIMARY KEY,
                authority TEXT NOT NULL,
                heading TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding REAL[] NOT NULL
        );
    """)
    connect.commit()

