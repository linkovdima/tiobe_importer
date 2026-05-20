"""
Общие фикстуры pytest для веб-приложения.

Запуск из корня проекта:
    pytest tests/ -v

Тестовый клиент Flask не открывает TCP-порт: запросы идут «внутрь» приложения.
"""
import pytest


@pytest.fixture
def client():
    from web_dashboard import app

    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
