from fastapi.testclient import TestClient
from backend.app import app, news_store
from config import STUDENT_ID
import feedparser

client = TestClient(app)

# Тест для перевірки порожнього стану новин
def test_get_news_empty():
    # Порожній початковий стан
    news_store[STUDENT_ID] = []
    res = client.get(f"/news/{STUDENT_ID}")
    
    # Перевіряємо статус 200 і порожній список
    assert res.status_code == 200
    assert res.json() == {"articles": []}

# Клас для підміни даних
class DummyFeed:
    entries = [
        {"title": "T1", "link": "<http://a>", "published": "2025-01-01"},
        {"title": "T2", "link": "<http://b>", "published": ""}
    ]

# Тест для перевірки збору новин із RSS
def test_fetch_and_get(monkeypatch):
    # Змінюємо SOURCES у модулі config
    monkeypatch.setattr("config.SOURCES", ["<http://example.com/rss>"])
    
    # Підмінюємо функцію feedparser.parse, щоб не робити реальний HTTP-запит
    monkeypatch.setattr(feedparser, "parse", lambda url: DummyFeed)
    
    # Очищаємо список новин перед тестом
    news_store[STUDENT_ID] = []
    
    # Виконуємо запит для отримання новин
    res1 = client.post(f"/fetch/{STUDENT_ID}")
    assert res1.status_code == 200
    assert res1.json() == {"fetched": 2}  # Ожидається, що було отримано 2 новини
    
    # Перевіряємо, що новини з'явилися в списку
    res2 = client.get(f"/news/{STUDENT_ID}")
    assert res2.status_code == 200
    assert res2.json() == {
        "articles": [
            {"title": "T1", "link": "<http://a>", "published": "2025-01-01"},
            {"title": "T2", "link": "<http://b>", "published": ""}
        ]
    }
