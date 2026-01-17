import os
import psycopg2

con=psycopg2.connect(os.getenv("DATABASE_URL"))
def store_chunks(con,chunks,embeddings):
    with con.cursor() as cur:
        for chunk, emb in zip(chunks,embeddings):
            cur.execute(
                """
                INSERT INTO doc_chunks (authority, heading, content, embedding)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    chunk["authority"],
                    chunk["heading"],
                    chunk["content"],
                    emb
                )
            )
    con.commit()