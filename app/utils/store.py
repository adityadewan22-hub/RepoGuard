import os
import psycopg2
from app.models.chunk import Chunk

con=psycopg2.connect(os.getenv("DATABASE_URL"))
def store_chunks(con,repo_id:str,chunks:list[Chunk]):
    with con.cursor() as cur:
        for chunk in chunks:
            cur.execute(
                """
                INSERT INTO doc_chunks (repo_id,authority, heading, content, embedding)
                VALUES (%s,%s, %s, %s, %s)
                """,
                (
                    repo_id,
                    chunk.authority,
                    chunk.heading,
                    chunk.content,
                    chunk.embedding
                )
            )
    con.commit()