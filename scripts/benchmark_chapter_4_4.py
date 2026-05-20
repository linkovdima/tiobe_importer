"""
Замеры для главы 4.4 (время отклика на локальном стенде).

Запуск: в одном терминале — py web_dashboard.py
        во втором — py scripts/benchmark_chapter_4_4.py

Переменная окружения BASE_URL (необязательно), по умолчанию http://127.0.0.1:5000
"""
import os
import statistics
import time

import requests

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:5000").rstrip("/")


def measure(name, func, n=10):
    times = []
    for i in range(n):
        t0 = time.perf_counter()
        r = func()
        dt = time.perf_counter() - t0
        times.append(dt * 1000)
        print(i, name, int(dt * 1000), "ms", r.status_code)
        time.sleep(0.05)
    cold, warm = times[0], times[1:]
    print(
        name,
        "cold_ms=",
        round(cold, 1),
        "warm_avg=",
        round(statistics.mean(warm), 1),
        "warm_min=",
        round(min(warm), 1),
        "warm_max=",
        round(max(warm), 1),
    )
    print()


def dashboard_html_only():
    """Только HTML-страница (без учёта отдельных XHR к графикам)."""
    r = requests.get(f"{BASE}/dashboard", timeout=180)
    r.raise_for_status()
    return r


def dashboard_with_charts():
    """
    Полная цепочка, как при открытии дашборда в браузере:
    HTML + два запроса к API графиков (Matplotlib на сервере).
    Одно число в таблице 4.4 — суммарное время всех трёх запросов подряд.
    """
    s = requests.Session()
    r1 = s.get(f"{BASE}/dashboard", timeout=180)
    r1.raise_for_status()
    r2 = s.get(f"{BASE}/api/chart/tiobe", timeout=180)
    r2.raise_for_status()
    r3 = s.get(f"{BASE}/api/chart/github", timeout=180)
    r3.raise_for_status()
    return r3


if __name__ == "__main__":
    print("BASE =", BASE, "\n")

    measure("GET /api/languages", lambda: requests.get(f"{BASE}/api/languages", timeout=60))

    measure(
        "POST /api/search",
        lambda: requests.post(
            f"{BASE}/api/search",
            json={"keywords": "Python", "page": 1, "per_page": 10},
            headers={"Content-Type": "application/json"},
            timeout=120,
        ),
    )

    measure("GET /dashboard (только HTML)", dashboard_html_only)

    measure(
        "GET /dashboard + /api/chart/tiobe + /api/chart/github (последовательно)",
        dashboard_with_charts,
    )
