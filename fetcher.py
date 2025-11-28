import feedparser
import sqlite3
import datetime
import os

RSS_FEEDS = [
    "https://www.svd.se/?service=rss",
    "https://www.di.se/rss",
    "http://feeds.reuters.com/reuters/europeBanksNews",
    "https://www.ecb.europa.eu/press/rss/press.html"
]

DB_PATH = "news.db"

def create_db():
    print("Creating or opening database at:", os.path.abspath(DB_PATH))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT,
            link TEXT UNIQUE,
            published TEXT,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()


def fetch_and_store():
    print("Fetching feeds...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    total_inserted = 0

    for feed_url in RSS_FEEDS:
        print("Reading:", feed_url)
        feed = feedparser.parse(feed_url)
        source = feed_url.split("/")[2]
        print("Entries found:", len(feed.entries))

        for entry in feed.entries:
            cursor.execute("""
                INSERT OR IGNORE INTO news (title, link, published, source)
                VALUES (?, ?, ?, ?)
            """, (
                entry.get("title"),
                entry.get("link"),
                entry.get("published", str(datetime.datetime.utcnow())),
                source
            ))
            total_inserted += cursor.rowcount

    conn.commit()
    conn.close()
    print("Inserted rows:", total_inserted)


if __name__ == "__main__":
    create_db()
    fetch_and_store()
    print("Debug: Done")
