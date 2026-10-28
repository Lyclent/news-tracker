POSITIVE_WORDS = {
    "рост", "успех", "прибыль", "развитие", "позитив", "достижение",
    "улучшение", "подъём", "стабильность", "прорыв", "увеличение",
    "good", "growth", "success", "profit", "improve", "gain"
}

NEGATIVE_WORDS = {
    "падение", "кризис", "убыток", "проблема", "риск", "потеря",
    "снижение", "негатив", "конфликт", "угроза", "обвал", "санкции",
    "bad", "crisis", "loss", "risk", "decline", "threat", "drop"
}


def analyze(text: str) -> tuple[str, float]:
    words = text.lower().split()
    pos = sum(1 for w in words if w.strip(".,!?:;") in POSITIVE_WORDS)
    neg = sum(1 for w in words if w.strip(".,!?:;") in NEGATIVE_WORDS)

    total = pos + neg
    if total == 0:
        return "neutral", 0.0

    score = (pos - neg) / total
    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"
    return label, round(score, 3)