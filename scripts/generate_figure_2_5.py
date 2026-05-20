# -*- coding: utf-8 -*-
"""Рисунок 2.5 — схема навигации и основных экранов (глава 2.5 ВКР)."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent.parent / "docs" / "figures" / "ris_2_5_navigaciya_ekrany.png"


def box(ax, xy, w, h, text, fc="#E8F4FC", ec="#1a5276", fontsize=9):
    x, y = xy
    p = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.2,
        edgecolor=ec,
        facecolor=fc,
        mutation_aspect=0.4,
    )
    ax.add_patch(p)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        wrap=True,
        color="#1a1a1a",
    )
    return (x, y, w, h)


def arrow(ax, a, b, rad=0.0):
    (x1, y1, w1, h1) = a
    (x2, y2, w2, h2) = b
    ax.add_patch(
        FancyArrowPatch(
            (x1 + w1 / 2, y1),
            (x2 + w2 / 2, y2 + h2),
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.0,
            color="#2c3e50",
            connectionstyle=f"arc3,rad={rad}",
            shrinkA=2,
            shrinkB=2,
        )
    )


def arrow_side(ax, a, b, side="right"):
    (x1, y1, w1, h1) = a
    (x2, y2, w2, h2) = b
    if side == "right":
        start = (x1 + w1, y1 + h1 / 2)
        end = (x2, y2 + h2 / 2)
    else:
        start = (x1, y1 + h1 / 2)
        end = (x2 + w2, y2 + h2 / 2)
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=1.0,
            color="#2c3e50",
            shrinkA=2,
            shrinkB=2,
        )
    )


def main():
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(1, 1, figsize=(11.69, 8.27))  # A4 landscape
    ax.set_xlim(0, 11.69)
    ax.set_ylim(0, 8.27)
    ax.axis("off")

    ax.text(
        5.85,
        7.85,
        "Рисунок 2.5 — Схема навигации и основных экранов веб-приложения",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color="#1a1a1a",
    )

    # Общая шапка
    header = box(ax, (0.6, 6.95), 10.5, 0.55, "Постоянная шапка: навигация по разделам\n(Bootstrap, единые компоненты меню)", fc="#D5E8D4", ec="#1e8449", fontsize=9)

    home = box(ax, (4.85, 6.15), 1.9, 0.5, "Стартовая\n/")

    # Второй ряд — ключевые разделы
    w, h = 1.75, 0.55
    y2 = 5.15
    x0 = 0.55
    gap = 0.22
    cat = box(ax, (x0 + 0 * (w + gap), y2), w, h, "Каталог языков\n/languages")
    search = box(ax, (x0 + 1 * (w + gap), y2), w, h, "Семантический\n/search\nпоиск")
    dash = box(ax, (x0 + 2 * (w + gap), y2), w, h, "Дашборд\n/dashboard")
    src = box(ax, (x0 + 3 * (w + gap), y2), w, h, "Источники\n/sources")
    cab = box(ax, (x0 + 4 * (w + gap), y2), w, h, "Личный кабинет\n/cabinet")
    auth = box(ax, (x0 + 5 * (w + gap), y2), w, h, "Вход / регистрация\n/login, /register")

    # Третий ряд — от каталога
    y3 = 3.85
    det = box(ax, (1.2, y3), 2.2, 0.55, "Детальная страница\nязыка\n/language/<name>")
    pub = box(ax, (4.2, y3), 2.0, 0.55, "Публикации\nпо языку\n/…/sources")
    ext = box(ax, (7.0, y3), 3.5, 0.55, "Внешний веб-поиск → сохранение\nPOST …/save_external, /save_fact")

    # Нижняя подпись про карточки
    y4 = 2.55
    card1 = box(ax, (0.8, y4), 2.4, 0.5, "Карточка публикации\n(из списка по языку)", fc="#FCE5CD", ec="#a04000")
    card2 = box(ax, (3.5, y4), 2.2, 0.5, "Карточка автора\n(по связи writtenBy)", fc="#FCE5CD", ec="#a04000")
    note = box(ax, (6.2, y4), 4.9, 0.5, "UX: статусы загрузки, сообщения об ошибках API,\nмодальные подтверждения (по сценарию)", fc="#EAEDED", ec="#566573", fontsize=8)

    # Стрелки: шапка -> разделы (упрощённо от центра стартовой)
    for n in (cat, search, dash, src, cab, auth):
        arrow(ax, header, n, rad=0.05)
    arrow(ax, header, home, rad=0.02)
    arrow(ax, home, cat, rad=0.0)

    arrow_side(ax, cat, det, "right")
    arrow_side(ax, det, pub, "right")
    arrow_side(ax, search, det, "right")
    arrow_side(ax, search, ext, "right")

    arrow(ax, pub, card1, rad=0.0)
    arrow(ax, card1, card2, rad=0.0)

    ax.text(
        5.85,
        0.45,
        "Сплошные стрелки — основные переходы пользователя; пунктир в тексте работы при необходимости\nдополняется сценариями AJAX (Fetch API) к REST-эндпоинтам.",
        ha="center",
        va="center",
        fontsize=8,
        style="italic",
        color="#555",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved:", OUT)


if __name__ == "__main__":
    main()
