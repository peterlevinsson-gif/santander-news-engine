from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

# Use the prebuilt database shipped with the repo
DB_PATH = os.path.join(os.path.dirname(__file__), "news.db")


class NewsQuery(BaseModel):
    query: str = ""
    limit: int = 20


@app.get("/")
def home():
    return {"status": "Santander News Engine is running!", "db_exists": os.path.isfile(DB_PATH)}


@app.post("/fetch_news")
def fetch_news(query: NewsQuery):
    # Ensure DB file exists
    if not os.path.isfile(DB_PATH):
        return {"error": "news.db not found on server"}

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
