from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()
DB_PATH = "news.db"


class NewsQuery(BaseModel):
    query: str = ""
    limit: int = 20


@app.get("/")
def home():
    return {"status": "Santander News Engine is running!"}


@app.post("/fetch_news")
def fetch_news(query: NewsQuery):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    q = f"%{query.query.lower()}%"
    cursor.execute("""
        SELECT title, link, published, source
        FROM news
        WHERE LOWER(title) LIKE ?
        ORDER BY published DESC
        LIMIT ?
    """, (q, query.limit))

    rows = cursor.fetchall()
    conn.close()

    return [
        {"title": r[0], "link": r[1], "published": r[2], "source": r[3]}
        for r in rows
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
