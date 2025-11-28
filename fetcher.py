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
    """Normalize the URL to avoid duplicates."""
    if not url:
        return None
    # remove utm parameters and tracking
    return re.sub(r"[?&]utm_[^&]+", "", url)


def create_db():
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
    print("Fet
