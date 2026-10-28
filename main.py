from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import News
import schemas
from parser import parse_feeds
import pandas as pd

Base.metadata.create_all(bind=engine)
app = FastAPI(title="News Sentiment Tracer")

@app.get("/")
def root():
    return {"message": "API Работает! Зайди на /docs"}

@app.post("/parse")
def run_parser(db: Session = Depends(get_db)):
    """Запускает парсинг RSS и сохраняет новые новости."""
    added = parse_feeds(db)
    return {"added": added}


@app.get("/news", response_model=list[schemas.NewsOut])
def get_news(limit: int = 20, db: Session = Depends(get_db)):
    """Возвращает последние новости."""
    news = (
        db.query(News)
        .order_by(News.published_at.desc())
        .limit(limit)
        .all()
    )
    return news


@app.get("/sentiment/top-negative")
def top_negative(limit: int = 5, db: Session = Depends(get_db)):
    """Топ самых негативных новостей (аналитика через pandas)."""
    news = db.query(News).all()
    if not news:
        raise HTTPException(status_code=404, detail="Новостей пока нет — сначала /parse")

    # Превращаем в DataFrame для удобной аналитики
    df = pd.DataFrame([
        {
            "id": n.id,
            "title": n.title,
            "source": n.source,
            "sentiment": n.sentiment,
            "score": n.sentiment_score,
        }
        for n in news
    ])

    # Фильтруем негативные, сортируем по score, берём топ
    top = (
        df[df["sentiment"] == "negative"]
        .sort_values("score")
        .head(limit)
        .to_dict(orient="records")
    )
    return {"count": len(top), "items": top}