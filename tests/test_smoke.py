"""
Smoke-тесты HTTP-маршрутов (глава 4 ВКР: автоматизированная проверка работоспособности).

Проверяют коды ответа и минимальную структуру JSON без запуска браузера.
"""
import json


def test_index_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"html" in r.data.lower() or len(r.data) > 100


def test_languages_page_ok(client):
    r = client.get("/languages")
    assert r.status_code == 200


def test_search_page_ok(client):
    r = client.get("/search")
    assert r.status_code == 200


def test_dashboard_page_ok(client):
    r = client.get("/dashboard")
    assert r.status_code == 200


def test_api_languages_json(client):
    r = client.get("/api/languages")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_api_language_python(client):
    r = client.get("/api/language/Python")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, dict)
    assert len(data) >= 1


def test_api_stats_json(client):
    r = client.get("/api/stats")
    assert r.status_code == 200
    data = r.get_json()
    assert "total_languages" in data


def test_api_me_folders_requires_auth(client):
    r = client.get("/api/me/folders")
    assert r.status_code == 401
    data = r.get_json()
    assert data.get("success") is False


def test_api_search_post_json(client):
    r = client.post(
        "/api/search",
        data=json.dumps({"keywords": "Python", "page": 1, "per_page": 10}),
        content_type="application/json",
    )
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, dict)
    assert data.get("success") is True
    assert "total_results" in data
