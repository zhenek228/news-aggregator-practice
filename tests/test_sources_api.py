from fastapi.testclient import TestClient
from backend.app import app
from config import STUDENT_ID
from backend import app as backend_app  # доступ до глобальної змінної SOURCES
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_sources():
    # Очистка SOURCES перед кожним тестом (якщо це дозволено логікою)
    backend_app.sources_store[STUDENT_ID] = []

def test_get_empty_sources():
    res = client.get(f"/sources/{STUDENT_ID}")
    assert res.status_code == 200
    assert res.json() == {"sources": []}

def test_add_and_get_source():
    url = "https://example.com/rss"  # правильний URL, без <>
    res1 = client.post(f"/sources/{STUDENT_ID}", json={"url": url})
    assert res1.status_code == 200
    assert url in res1.json()["sources"]
    
    res2 = client.get(f"/sources/{STUDENT_ID}")
    assert url in res2.json()["sources"]
