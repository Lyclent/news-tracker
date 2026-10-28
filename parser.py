import feedparser
from datetime import datetime
from sqlalchemy.orm import Session
from models import News
from sentiment import analyze

FEEDS = [
    ("https://lenta.ru/rss/news", "Lenta"),
]


def parse_feeds(db: Session) -> int:
    """Парсит все RSS-ленты и сохраняет новые новости. Возвращает количество добавленных."""
    added = 0
    for url, source in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            link = entry.get("link")
            if not link:
                continue

            exists = db.query(News).filter(News.link == link).first()
            if exists:
                continue

            title = entry.get("title", "").strip()
            if not title:
                continue

            label, score = analyze(title)

            news = News(
                title=title,
                link=link,
                source=source,
                sentiment=label,
                sentiment_score=score,
            )
            db.add(news)
            added += 1

        db.commit()

    return added