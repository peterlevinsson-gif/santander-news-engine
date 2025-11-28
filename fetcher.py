import feedparser
import sqlite3
import datetime
import re
import os

RSS_FEEDS = [
    "https://www.svd.se/?service=rss",
    "https://www.di.se/rss",
    "http://feeds.reuters.com/reuters/europeBanksNews",
    "https://www.ecb.europa.eu/press/rss/press.html"
]

DB_PATH = "news.db"


def clean_url(url: str) -> str:
    """Normalize the URL to avoid duplicates by removing tracking parameters."""
    if not url:
        return None
    return re.sub(r"[?&]utm_[^&]+", "", url)


def create_db():
    print("Creating or opening database:", os.path.abspath(DB_PATH))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            guid TEXT PRIMARY KEY,
            title TEXT,
            link TEXT,
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
        print("\nReading:", feed_url)
        feed = feedparser.parse(feed_url)
        source = feed_url.split("/")[2]
        print("Entries found:", len(feed.entries))

        for entry in feed.entries:
            guid = entry.get("guid") or entry.get("id") or entry.get("link")
            if not guid:
                continue

            link = clean_url(entry.get("link") or guid)
            title = entry.get("title", "").strip()
            published = entry.get("published", str(datetime.datetime.utcnow()))

            cursor.execute("""
                INSERT OR REPLACE INTO news (guid, title, link, published, source)
                VALUES (?, ?, ?, ?, ?)
            """, (guid, title, link, published, source))

            total_inserted += cursor.rowcount

    conn.commit()
    conn.close()
    print("\nInserted rows:", total_inserted)


if __name__ == "__main__":
    create_db()
    fetch_and_store()
    print("Done.")
