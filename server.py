import feedparser
import sqlite3
import datetime

RSS_FEEDS = [
    "https://www.svd.se/?service=rss",
    "https://www.di.se/rss",
    "http://feeds.reuters.com/reuters/europeBanksNews",
    "https://www.ecb.europa.eu/press/rss/press.html"
]

DB_PATH = "news.db"


def create_db():
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        source = feed_url.split("/")[2]

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

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()
    fetch_and_store()
    print("News updated!")
