"""
Хранилище данных для личного кабинета (пользователи, папки, сохраненные ресурсы).

Используем SQLite, чтобы не добавлять внешние зависимости.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from config import BASE_DIR, ONTOLOGY_PATH


DB_PATH = BASE_DIR / "data" / "cabinet.sqlite3"


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def _normalize_username(username: str) -> str:
    username = username.strip()
    # Ограничиваем символы для стабильных ключей.
    username = re.sub(r"[^a-zA-Z0-9_\-\.]", "", username)
    return username[:40]


def _slug_bib_key(value: str, max_len: int = 60) -> str:
    value = value.strip()
    value = value.replace(" ", "_")
    value = re.sub(r"[^a-zA-Z0-9_:\-\.]", "", value)
    if len(value) > max_len:
        value = value[:max_len]
    return value or "key"


def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """Создает таблицы, если их нет."""
    with _get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS saved_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                folder_id INTEGER NOT NULL,
                resource_uri TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                publication_type TEXT,
                title_snapshot TEXT,
                author_snapshot TEXT,
                url_snapshot TEXT,
                keywords_snapshot TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE
            );
            """
        )
        # Индексы ускорят типовые выборки.
        conn.execute("CREATE INDEX IF NOT EXISTS idx_folders_user ON folders(user_id);")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_saved_user_folder ON saved_resources(user_id, folder_id);"
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_saved_resource_uri ON saved_resources(resource_uri);")


@dataclass
class Folder:
    id: int
    name: str
    created_at: str


def create_user(username: str, password_hash: str) -> Optional[int]:
    username = _normalize_username(username)
    if not username:
        return None

    with _get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO users(username, password_hash, created_at) VALUES (?, ?, ?);",
            (username, password_hash, _now_iso()),
        )
        return int(cur.lastrowid)


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    username = _normalize_username(username)
    if not username:
        return None

    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?;", (username,)).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?;", (user_id,)).fetchone()
        return dict(row) if row else None


def create_folder(user_id: int, name: str) -> Optional[int]:
    name = name.strip() if name else ""
    if not name:
        return None

    with _get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO folders(user_id, name, created_at) VALUES (?, ?, ?);",
            (user_id, name, _now_iso()),
        )
        return int(cur.lastrowid)


def list_folders(user_id: int) -> List[Dict[str, Any]]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT id, name, created_at FROM folders WHERE user_id = ? ORDER BY created_at DESC;",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def delete_folder(user_id: int, folder_id: int) -> bool:
    with _get_conn() as conn:
        cur = conn.execute(
            "DELETE FROM folders WHERE id = ? AND user_id = ?;",
            (folder_id, user_id),
        )
        return cur.rowcount > 0


def folder_belongs_to_user(user_id: int, folder_id: int) -> bool:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM folders WHERE id = ? AND user_id = ?;",
            (folder_id, user_id),
        ).fetchone()
        return row is not None


def save_resource(
    user_id: int,
    folder_id: int,
    *,
    resource_uri: str,
    resource_type: str,
    publication_type: Optional[str] = None,
    title_snapshot: Optional[str] = None,
    author_snapshot: Optional[str] = None,
    url_snapshot: Optional[str] = None,
    keywords_snapshot: Optional[str] = None,
) -> bool:
    """Сохраняет ресурс в папку."""
    if not resource_uri or not resource_type:
        return False

    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO saved_resources(
                user_id, folder_id, resource_uri, resource_type,
                publication_type, title_snapshot, author_snapshot,
                url_snapshot, keywords_snapshot, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                user_id,
                folder_id,
                resource_uri,
                resource_type,
                publication_type,
                title_snapshot,
                author_snapshot,
                url_snapshot,
                keywords_snapshot,
                _now_iso(),
            ),
        )
        return True


def list_saved_resources(user_id: int, folder_id: Optional[int] = None) -> List[Dict[str, Any]]:
    with _get_conn() as conn:
        if folder_id is None:
            rows = conn.execute(
                """
                SELECT
                    id, folder_id, resource_uri, resource_type, publication_type,
                    title_snapshot, author_snapshot, url_snapshot, keywords_snapshot,
                    created_at
                FROM saved_resources
                WHERE user_id = ?
                ORDER BY created_at DESC;
                """,
                (user_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT
                    id, folder_id, resource_uri, resource_type, publication_type,
                    title_snapshot, author_snapshot, url_snapshot, keywords_snapshot,
                    created_at
                FROM saved_resources
                WHERE user_id = ? AND folder_id = ?
                ORDER BY created_at DESC;
                """,
                (user_id, folder_id),
            ).fetchall()
        return [dict(r) for r in rows]


def list_saved_resources_by_ids(user_id: int, saved_ids: Sequence[int]) -> List[Dict[str, Any]]:
    """
    Возвращает сохраненные ресурсы по их id.
    Служебная функция для экспорта “выбранных” записей.
    """
    ids = sorted({int(x) for x in saved_ids if x is not None})
    if not ids:
        return []

    placeholders = ",".join(["?"] * len(ids))
    with _get_conn() as conn:
        rows = conn.execute(
            f"""
            SELECT
                id, folder_id, resource_uri, resource_type, publication_type,
                title_snapshot, author_snapshot, url_snapshot, keywords_snapshot,
                created_at
            FROM saved_resources
            WHERE user_id = ?
              AND id IN ({placeholders})
            ORDER BY created_at DESC;
            """,
            (user_id, *ids),
        ).fetchall()
        return [dict(r) for r in rows]


def move_saved_resource(user_id: int, saved_id: int, new_folder_id: int) -> bool:
    with _get_conn() as conn:
        cur = conn.execute(
            """
            UPDATE saved_resources
            SET folder_id = ?
            WHERE id = ? AND user_id = ?;
            """,
            (new_folder_id, saved_id, user_id),
        )
        return cur.rowcount > 0


def delete_saved_resource(user_id: int, saved_id: int) -> bool:
    with _get_conn() as conn:
        cur = conn.execute(
            "DELETE FROM saved_resources WHERE id = ? AND user_id = ?;",
            (saved_id, user_id),
        )
        return cur.rowcount > 0


def export_bibtex_for_resources(resources: Sequence[Dict[str, Any]]) -> str:
    """
    Генерирует BibTeX текст из snapshot-полей.
    """
    entries: List[str] = []

    for r in resources:
        pub_type = (r.get("publication_type") or "").strip()
        title = (r.get("title_snapshot") or "").strip()
        author = (r.get("author_snapshot") or "").strip()
        url = (r.get("url_snapshot") or "").strip()

        if pub_type:
            bib_type = {
                "Book": "book",
                "Article": "article",
                "Documentation": "misc",
                "Tutorial": "misc",
            }.get(pub_type, "misc")
        else:
            bib_type = "misc"

        year = ""
        # Опционально достаем год из онтологии по resource_uri.
        try:
            if r.get("resource_uri"):
                from rdflib import Graph, Namespace

                g = Graph()
                g.parse(str(ONTOLOGY_PATH), format="turtle")
                onto_ns = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")
                local_name = r.get("resource_uri").split("/")[-1]
                year_val = g.value(onto_ns[local_name], onto_ns.yearCreated)
                if year_val:
                    year = str(year_val)
        except Exception:
            year = ""

        bib_key = _slug_bib_key(f"{author}_{title}_{year}_{r.get('resource_uri','')}")

        def esc(s: str) -> str:
            s = s.replace("{", "\\{").replace("}", "\\}")
            s = s.replace("\n", " ").strip()
            return s

        base = f"@{bib_type}{{{bib_key},\n"
        fields = []
        if author:
            fields.append(f"  author = {{{esc(author)}}}")
        if title:
            fields.append(f"  title = {{{esc(title)}}}")
        if year:
            fields.append(f"  year = {{{esc(year)}}}")
        if url:
            fields.append(f"  howpublished = {{\\url{{{esc(url)}}}}}")

        entries.append(base + ",\n".join(fields) + "\n}}")

    return "\n\n".join(entries)


def ensure_default_folder_exists(user_id: int) -> int:
    """Создает папку 'Избранное' при первом использовании."""
    folders = list_folders(user_id)
    for f in folders:
        if f.get("name") == "Избранное":
            return int(f["id"])

    folder_id = create_folder(user_id, "Избранное")
    if folder_id is None:
        raise RuntimeError("Не удалось создать папку 'Избранное'")
    return folder_id


# Инициализируем схему при импорте.
init_db()

