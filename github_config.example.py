"""
Скопируйте в github_config.py или задайте переменную окружения GITHUB_TOKEN.

GitHub → Settings → Developer settings → Personal access tokens
(права: public_repo или read-only для поиска репозиториев).
"""
import os

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
