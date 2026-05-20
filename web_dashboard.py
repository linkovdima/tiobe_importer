# web_dashboard.py
from flask import Flask, render_template, jsonify, request, redirect, session
from rdflib import Graph, Namespace, RDF, Literal
import json
from datetime import datetime
from typing import Optional
import matplotlib
matplotlib.use('Agg')  # Используем backend без GUI для сервера
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from cabinet_storage import (
    create_user,
    get_user_by_username,
    get_user_by_id,
    create_folder,
    list_folders,
    delete_folder,
    folder_belongs_to_user,
    save_resource,
    list_saved_resources,
    list_saved_resources_by_ids,
    move_saved_resource,
    delete_saved_resource,
    ensure_default_folder_exists,
    export_bibtex_for_resources,
)
from ontology_search import OntologySearch
from pathlib import Path
from publication_manager import PublicationManager

app = Flask(__name__)

# Конфигурация: путь к TTL рядом с проектом (переопределение: переменная окружения ONTOLOGY_PATH)
_BASE_DIR = Path(__file__).resolve().parent
ONTOLOGY_PATH = os.environ.get(
    "ONTOLOGY_PATH", str(_BASE_DIR / "data" / "programming_languages.ttl")
)
NS = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")

# Secret key нужен для Flask-сессий (login/logout).
# В проде лучше задать через переменную окружения.
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(16)

def create_templates():
    """Создание HTML шаблонов"""
    
    # Создаем папку templates если её нет
    os.makedirs('templates', exist_ok=True)
    
    # Главная страница
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Programming Languages Ontology Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2563eb;
            --bg-light: #f8fafc;
            --text-dark: #1e293b;
            --border-color: #e2e8f0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-light);
        }
        
        .hero-section {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white;
            padding: 60px 0;
            margin-bottom: 40px;
        }
        
        .stat-card {
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s;
            background: white;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .language-card {
            border: 1px solid var(--border-color);
            border-radius: 12px;
            margin-bottom: 20px;
            transition: all 0.2s;
            background: white;
        }
        
        .language-card:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-color: var(--primary-color);
        }
        
        .nav-link {
            font-weight: 500;
            color: rgba(255,255,255,0.8);
        }
        
        .nav-link:hover {
            color: white;
        }
        
        .navbar {
            background-color: #1e293b !important;
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .btn-primary:hover {
            background-color: #1e40af;
            border-color: #1e40af;
        }
    </style>
</head>
<body>
    <!-- Навигация -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-code"></i> Языки Программирования
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/dashboard">Дашборд</a>
                <a class="nav-link" href="/languages">Языки</a>
                <a class="nav-link" href="/search">Поиск</a>
                <a class="nav-link" href="/cabinet" title="Личный кабинет">
                    <i class="fas fa-user"></i>
                </a>
            </div>
        </div>
    </nav>

    <!-- Герой секция -->
    <div class="hero-section">
        <div class="container text-center">
            <h1 class="display-4 fw-bold">База знаний языков программирования</h1>
            <p class="lead">Комплексная информация о языках программирования: рейтинги, книги, документация, туториалы и многое другое</p>
            
            <!-- Поисковая строка -->
            <div class="row mt-4">
                <div class="col-md-8 mx-auto">
                    <form action="/search" method="GET" id="mainSearchForm">
                        <div class="input-group input-group-lg shadow-lg">
                            <input type="text" class="form-control" name="q" id="mainSearchInput" 
                                   placeholder="Поиск по языкам, книгам, документации... (например: Python, Fluent Python, документация)"
                                   style="border-radius: 50px 0 0 50px; border: none; padding: 15px 25px;">
                            <button class="btn btn-light" type="submit" 
                                    style="border-radius: 0 50px 50px 0; border: none; padding: 15px 30px;">
                                <i class="fas fa-search"></i> Найти
                            </button>
                        </div>
                    </form>
                    <p class="mt-3 mb-0">
                        <small>Попробуйте: "Python", "книга", "документация", "русский"</small>
                    </p>
                </div>
            </div>
            
            <div class="mt-4">
                <a href="/dashboard" class="btn btn-light btn-lg me-2">
                    <i class="fas fa-chart-bar"></i> Аналитика
                </a>
                <a href="/languages" class="btn btn-outline-light btn-lg">
                    <i class="fas fa-list"></i> Все языки
                </a>
            </div>
        </div>
    </div>

    <!-- Статистика -->
    <div class="container">
        <div class="row" id="stats-container">
            <!-- Статистика загрузится через JavaScript -->
        </div>

    </div>

    <!-- Результаты поиска (если есть запрос) -->
    <div class="container mt-4" id="search-results-section" style="display: none;">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0"><i class="fas fa-search"></i> Результаты поиска</h5>
            </div>
            <div class="card-body" id="search-results">
                <!-- Результаты загрузятся через JavaScript -->
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Загрузка статистики
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                const statsContainer = document.getElementById('stats-container');
                statsContainer.innerHTML = `
                    <div class="col-md-3 mb-3">
                        <div class="card stat-card">
                            <div class="card-body text-center">
                                <h3 class="text-primary">${data.total_languages}</h3>
                                <p class="text-muted">Всего языков</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3 mb-3">
                        <div class="card stat-card">
                            <div class="card-body text-center">
                                <h3 class="text-success">${data.languages_with_tiobe}</h3>
                                <p class="text-muted">TIOBE данные</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3 mb-3">
                        <div class="card stat-card">
                            <div class="card-body text-center">
                                <h3 class="text-info">${data.languages_with_github}</h3>
                                <p class="text-muted">GitHub данные</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3 mb-3">
                        <div class="card stat-card">
                            <div class="card-body text-center">
                                <h3 class="text-warning">${data.languages_with_stackoverflow}</h3>
                                <p class="text-muted">Stack Overflow</p>
                            </div>
                        </div>
                    </div>
                `;
            });
        
        // Обработка поиска на главной странице
        document.getElementById('mainSearchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const query = document.getElementById('mainSearchInput').value.trim();
            if (query) {
                performSearchOnMainPage(query);
            }
        });
        
        // Проверка GET параметра q
        const urlParams = new URLSearchParams(window.location.search);
        const q = urlParams.get('q');
        if (q) {
            document.getElementById('mainSearchInput').value = q;
            performSearchOnMainPage(q);
        }
        
        function performSearchOnMainPage(keywords) {
            const resultsSection = document.getElementById('search-results-section');
            const resultsContainer = document.getElementById('search-results');
            
            resultsSection.style.display = 'block';
            resultsContainer.innerHTML = '<div class="text-center py-3"><div class="spinner-border spinner-border-sm" role="status"></div><p class="mt-2">Поиск...</p></div>';
            
            // Прокрутка к результатам
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    keywords: keywords,
                    languages: null
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success && data.total_results > 0) {
                    renderSearchResults(data, resultsContainer);
                } else {
                    resultsContainer.innerHTML = `
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> По запросу "${keywords}" ничего не найдено.
                            <a href="/search?q=${encodeURIComponent(keywords)}" class="alert-link">Попробовать расширенный поиск</a>
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error('Ошибка поиска:', error);
                resultsContainer.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i> Ошибка поиска: ${error.message}
                    </div>
                `;
            });
        }
        
        function renderSearchResults(data, container) {
            let html = `
                <div class="mb-3">
                    <h6>Найдено результатов: ${data.total_results}</h6>
                    <p class="text-muted small">Запрос: "${data.keywords}"</p>
                    <a href="/search?q=${encodeURIComponent(data.keywords)}" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-external-link-alt"></i> Расширенный поиск
                    </a>
                </div>
                <div class="row">
            `;
            
            // Показываем первые 6 результатов
            data.results.slice(0, 6).forEach(result => {
                html += renderResultCard(result);
            });
            
            html += '</div>';
            
            if (data.total_results > 6) {
                html += `
                    <div class="mt-3 text-center">
                        <a href="/search?q=${encodeURIComponent(data.keywords)}" class="btn btn-primary">
                            Показать все ${data.total_results} результатов
                        </a>
                    </div>
                `;
            }
            
            container.innerHTML = html;
        }
        
        function renderResultCard(result) {
            let cardClass = '';
            let icon = '';
            let title = '';
            let content = '';
            
            if (result.type === 'language') {
                cardClass = 'border-primary';
                icon = '<i class="fas fa-code text-primary"></i>';
                title = `<h6 class="card-title">${result.display_name || result.name}</h6>`;
                content = `
                    <p class="small mb-2"><strong>Тип:</strong> Язык программирования</p>
                    <a href="/language/${result.name}/sources" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-list"></i> Все источники
                    </a>
                `;
            } else if (result.type === 'publication') {
                cardClass = 'border-success';
                
                // Определяем тип публикации
                let pubType = 'Публикация';
                let typeIcon = '<i class="fas fa-file-alt text-success"></i>';
                if (result.publication_type === 'Book') {
                    pubType = 'Книга';
                    typeIcon = '<i class="fas fa-book text-success"></i>';
                } else if (result.publication_type === 'Documentation') {
                    pubType = 'Документация';
                    typeIcon = '<i class="fas fa-book-open text-info"></i>';
                } else if (result.publication_type === 'Tutorial') {
                    pubType = 'Туториал';
                    typeIcon = '<i class="fas fa-graduation-cap text-warning"></i>';
                } else if (result.publication_type === 'Article') {
                    pubType = 'Статья';
                    typeIcon = '<i class="fas fa-newspaper text-primary"></i>';
                }
                
                icon = typeIcon;
                title = `<h6 class="card-title">${result.title || result.name}</h6>`;
                
                content = `
                    <p class="small mb-2"><strong>Тип:</strong> ${pubType}</p>
                    ${result.author ? `<p class="small mb-2"><strong>Автор:</strong> ${result.author}</p>` : ''}
                    ${result.url ? `
                        <a href="${result.url}" target="_blank" class="btn btn-sm btn-primary">
                            <i class="fas fa-external-link-alt"></i> Открыть
                        </a>
                    ` : ''}
                    ${result.language ? `
                        <a href="/language/${result.language}/sources" class="btn btn-sm btn-outline-secondary">
                            <i class="fas fa-list"></i> Все источники
                        </a>
                    ` : ''}
                `;
            } else if (result.type === 'framework') {
                cardClass = 'border-warning';
                icon = '<i class="fas fa-cube text-warning"></i>';
                title = `<h6 class="card-title">${result.name}</h6>`;
                content = `<p class="small mb-2"><strong>Тип:</strong> Фреймворк</p>`;
            }
            
            return `
                <div class="col-md-6 mb-3">
                    <div class="card ${cardClass} h-100">
                        <div class="card-body">
                            ${icon}
                            ${title}
                            ${content}
                        </div>
                    </div>
                </div>
            `;
        }
    </script>
</body>
</html>''')

    # Дашборд
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Дашборд - Языки Программирования</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2563eb;
            --bg-light: #f8fafc;
            --text-dark: #1e293b;
            --border-color: #e2e8f0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-light);
        }
        
        .chart-container {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid var(--border-color);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .chart-title {
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 12px;
            margin-bottom: 20px;
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-dark);
        }
        
        .chart-image {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }
        
        .navbar {
            background-color: #1e293b !important;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-code"></i> Языки Программирования
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link active" href="/dashboard">Дашборд</a>
                <a class="nav-link" href="/languages">Языки</a>
                <a class="nav-link" href="/cabinet" title="Личный кабинет">
                    <i class="fas fa-user"></i>
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h1>Аналитический Дашборд</h1>
        <p class="lead">Визуализация данных о языках программирования</p>

        <!-- TIOBE Chart -->
        <div class="chart-container" id="tiobe">
            <h3 class="chart-title">
                <i class="fas fa-trophy text-warning"></i> TIOBE Рейтинги
            </h3>
            <div id="tiobe-chart">
                <div class="text-center">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Загрузка...</span>
                    </div>
                    <p>Загрузка графика...</p>
                </div>
            </div>
        </div>

        <!-- GitHub Chart -->
        <div class="chart-container" id="github">
            <h3 class="chart-title">
                <i class="fab fa-github text-dark"></i> GitHub Репозитории
            </h3>
            <div id="github-chart">
                <div class="text-center">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Загрузка...</span>
                    </div>
                    <p>Загрузка графика...</p>
                </div>
            </div>
        </div>

        <!-- Stack Overflow Chart -->
        <div class="chart-container">
            <h3 class="chart-title">
                <i class="fab fa-stack-overflow text-orange"></i> Stack Overflow Вопросы
            </h3>
            <div id="stackoverflow-chart">
                <div class="text-center">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Загрузка...</span>
                    </div>
                    <p>Загрузка данных...</p>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Загрузка TIOBE графика
        fetch('/api/chart/tiobe')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка загрузки TIOBE графика');
                }
                return response.json();
            })
            .then(data => {
                if (data.chart) {
                    document.getElementById('tiobe-chart').innerHTML = 
                        `<img src="${data.chart}" class="img-fluid chart-image" alt="TIOBE Chart">`;
                } else {
                    document.getElementById('tiobe-chart').innerHTML = 
                        '<div class="alert alert-warning"><i class="fas fa-exclamation-triangle"></i> Нет данных для отображения</div>';
                }
            })
            .catch(error => {
                console.error('Ошибка TIOBE:', error);
                document.getElementById('tiobe-chart').innerHTML = 
                    '<div class="alert alert-danger">Ошибка загрузки графика: ' + error.message + '</div>';
            });

        // Загрузка GitHub графика
        fetch('/api/chart/github')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка загрузки GitHub графика');
                }
                return response.json();
            })
            .then(data => {
                if (data.chart) {
                    document.getElementById('github-chart').innerHTML = 
                        `<img src="${data.chart}" class="img-fluid chart-image" alt="GitHub Chart">`;
                } else {
                    document.getElementById('github-chart').innerHTML = 
                        '<div class="alert alert-warning"><i class="fas fa-exclamation-triangle"></i> Нет данных для отображения</div>';
                }
            })
            .catch(error => {
                console.error('Ошибка GitHub:', error);
                document.getElementById('github-chart').innerHTML = 
                    '<div class="alert alert-danger">Ошибка загрузки графика: ' + error.message + '</div>';
            });

        // Загрузка Stack Overflow данных
        fetch('/api/languages')
            .then(response => response.json())
            .then(languages => {
                const stackoverflowData = languages
                    .filter(lang => lang.stackoverflow_questions)
                    .sort((a, b) => b.stackoverflow_questions - a.stackoverflow_questions)
                    .slice(0, 6);

                let html = '<div class="table-responsive"><table class="table table-striped"><thead><tr>';
                html += '<th>Язык</th><th>Вопросов</th><th>Процент</th></tr></thead><tbody>';
                
                const totalQuestions = stackoverflowData.reduce((sum, lang) => sum + lang.stackoverflow_questions, 0);
                
                stackoverflowData.forEach(lang => {
                    const percentage = ((lang.stackoverflow_questions / totalQuestions) * 100).toFixed(1);
                    html += `<tr>
                        <td><strong>${lang.display_name}</strong></td>
                        <td>${lang.stackoverflow_questions.toLocaleString()}</td>
                        <td><span class="badge bg-info">${percentage}%</span></td>
                    </tr>`;
                });
                
                html += '</tbody></table></div>';
                document.getElementById('stackoverflow-chart').innerHTML = html;
            });
    </script>
</body>
</html>''')

    # Список языков
    with open('templates/languages.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Языки Программирования</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-code"></i> Языки Программирования
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/dashboard">Дашборд</a>
                <a class="nav-link active" href="/languages">Языки</a>
                <a class="nav-link" href="/cabinet" title="Личный кабинет">
                    <i class="fas fa-user"></i>
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h1>Языки Программирования</h1>
        <p class="lead">Детальная информация по всем языкам</p>
        
        <div class="row" id="languages-container">
            <!-- Языки загрузятся через JavaScript -->
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        fetch('/api/languages')
            .then(response => response.json())
            .then(languages => {
                const container = document.getElementById('languages-container');
                
                languages.forEach(lang => {
                    const card = document.createElement('div');
                    card.className = 'col-md-6 col-lg-4 mb-4';
                    
                    card.innerHTML = `
                        <div class="card language-card h-100">
                            <div class="card-body">
                                <h5 class="card-title">${lang.display_name}</h5>
                                
                                ${lang.tiobe_rank ? `
                                <div class="mb-2">
                                    <small class="text-muted">TIOBE Рейтинг</small>
                                    <div>
                                        <span class="badge bg-warning">#${lang.tiobe_rank}</span>
                                        <span class="text-muted">${lang.tiobe_rating}</span>
                                    </div>
                                </div>
                                ` : ''}
                                
                                ${lang.github_repos ? `
                                <div class="mb-2">
                                    <small class="text-muted">GitHub</small>
                                    <div>
                                        <i class="fab fa-github"></i>
                                        ${(lang.github_repos / 1000000).toFixed(1)}M репозиториев
                                    </div>
                                </div>
                                ` : ''}
                                
                                ${lang.stackoverflow_questions ? `
                                <div class="mb-3">
                                    <small class="text-muted">Stack Overflow</small>
                                    <div>
                                        <i class="fab fa-stack-overflow"></i>
                                        ${(lang.stackoverflow_questions / 1000).toFixed(0)}k вопросов
                                    </div>
                                </div>
                                ` : ''}
                                
                                <div class="d-grid gap-2">
                                    <a href="/language/${lang.name}/sources" class="btn btn-primary btn-sm">
                                        <i class="fas fa-book"></i> Все источники
                                    </a>
                                    <a href="/language/${lang.name}" class="btn btn-outline-secondary btn-sm">
                                        Детальная информация
                                    </a>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    container.appendChild(card);
                });
            });
    </script>
</body>
</html>''')

    # Страница поиска
    with open('templates/search.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Поиск по онтологии - Языки Программирования</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .search-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
            margin-bottom: 40px;
        }
        .result-card {
            border: none;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .result-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .relevance-badge {
            position: absolute;
            top: 10px;
            right: 10px;
        }
        .language-badge {
            display: inline-block;
            padding: 5px 10px;
            margin: 3px;
            background: #007bff;
            color: white;
            border-radius: 15px;
            font-size: 0.85em;
        }
        .filter-tags {
            margin-top: 10px;
        }
        .filter-tag {
            display: inline-block;
            padding: 5px 12px;
            margin: 5px 5px 5px 0;
            background: #e9ecef;
            border-radius: 20px;
            font-size: 0.9em;
        }
        .filter-tag.active {
            background: #007bff;
            color: white;
        }
    </style>
</head>
<body>
    <!-- Навигация -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-code"></i> Языки Программирования
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/dashboard">Дашборд</a>
                <a class="nav-link" href="/languages">Языки</a>
                <a class="nav-link active" href="/search">Поиск</a>
                <a class="nav-link" href="/cabinet" title="Личный кабинет">
                    <i class="fas fa-user"></i>
                </a>
            </div>
        </div>
    </nav>

    <!-- Поисковая секция -->
    <div class="search-container">
        <div class="container">
            <h1 class="display-4 mb-4">
                <i class="fas fa-search"></i> Поиск по онтологии
            </h1>
            <p class="lead">Ищите информацию о языках программирования, публикациях, фреймворках и многом другом</p>
            
            <div class="row mt-4">
                <div class="col-md-8 mx-auto">
                    <form id="searchForm">
                        <div class="input-group input-group-lg">
                            <input type="text" class="form-control" id="keywordsInput" 
                                   placeholder="Введите ключевые слова (например: web development, object oriented, beginner)">
                            <button class="btn btn-light" type="submit">
                                <i class="fas fa-search"></i> Найти
                            </button>
                        </div>
                    </form>
                    <script>
                        // Поддержка GET параметра q
                        const urlParams = new URLSearchParams(window.location.search);
                        const q = urlParams.get('q');
                        if (q) {
                            document.getElementById('keywordsInput').value = q;
                            setTimeout(() => {
                                performSearch(q, 1);
                            }, 500);
                        }
                    </script>
                </div>
            </div>
            
            <!-- Фильтр по языкам -->
            <div class="row mt-4">
                <div class="col-md-8 mx-auto">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Фильтр по языкам:</h6>
                            <div class="filter-tags" id="languageFilters">
                                <span class="filter-tag active" data-lang="">Все языки</span>
                                <!-- Языки загрузятся через JavaScript -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Дополнительные фильтры -->
            <div class="row mt-4">
                <div class="col-md-8 mx-auto">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Расширенный поиск</h6>
                            <div class="row g-2 align-items-end">
                                <div class="col-md-4">
                                    <label class="form-label small text-muted">Тип источника</label>
                                    <select class="form-select form-select-sm" id="sourceTypeSelect">
                                        <option value="">Любой</option>
                                        <option value="Book">Книга</option>
                                        <option value="Article">Статья</option>
                                        <option value="Documentation">Документация</option>
                                        <option value="Tutorial">Туториал</option>
                                    </select>
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small text-muted">Язык материала</label>
                                    <select class="form-select form-select-sm" id="sourceLanguageSelect">
                                        <option value="">Любой</option>
                                        <option value="русский">Русский</option>
                                        <option value="английский">Английский</option>
                                    </select>
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small text-muted">Сложность</label>
                                    <select class="form-select form-select-sm" id="difficultySelect">
                                        <option value="">Любая</option>
                                        <option value="начальный">Начальный</option>
                                        <option value="средний">Средний</option>
                                        <option value="продвинутый">Продвинутый</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label small text-muted">Год</label>
                                    <input class="form-control form-control-sm" id="yearInput" type="number" placeholder="Напр. 2015">
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label small text-muted">Сортировка</label>
                                    <select class="form-select form-select-sm" id="sortBySelect">
                                        <option value="relevance">По релевантности</option>
                                        <option value="date">По дате</option>
                                        <option value="popularity">По популярности</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label small text-muted">Результатов на страницу</label>
                                    <select class="form-select form-select-sm" id="perPageSelect">
                                        <option value="10">10</option>
                                        <option value="20" selected>20</option>
                                        <option value="50">50</option>
                                    </select>
                                </div>
                                <div class="col-md-3 d-grid">
                                    <button class="btn btn-outline-primary btn-sm mt-4" type="button" id="applyFiltersBtn">
                                        Применить
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Сохранение в кабинет -->
    <div class="row mt-4">
        <div class="col-md-8 mx-auto">
            <div class="card">
                <div class="card-body">
                    <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                        <div>
                            <h6 class="card-title mb-0">Сохранение в кабинет</h6>
                            <div class="text-muted small">Выберите папку для кнопок «Сохранить»</div>
                        </div>
                        <select class="form-select form-select-sm" id="saveFolderSelect" style="max-width: 320px;">
                            <option value="">Загрузить папки...</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Результаты поиска -->
    <div class="container">
        <div id="searchResults">
            <div class="text-center text-muted py-5">
                <i class="fas fa-search fa-3x mb-3"></i>
                <p>Введите ключевые слова для поиска</p>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let selectedLanguages = [];
        let allLanguages = [];
        let currentKeywords = '';

        async function loadSaveFolderSelect() {
            const select = document.getElementById('saveFolderSelect');
            if (!select) return;

            select.disabled = true;
            select.innerHTML = '<option value="">Войдите, чтобы сохранять</option>';

            try {
                const sessionRes = await fetch('/api/me/session');
                const sessionData = await sessionRes.json();
                if (!sessionData.logged_in) return;

                const foldersRes = await fetch('/api/me/folders');
                const foldersData = await foldersRes.json();
                if (!foldersData.success) return;

                const folders = foldersData.folders || [];
                if (folders.length === 0) return;

                select.innerHTML = '';
                folders.forEach(f => {
                    const opt = document.createElement('option');
                    opt.value = f.id;
                    opt.textContent = f.name;
                    select.appendChild(opt);
                });

                const favorite = folders.find(f => f.name === 'Избранное') || folders[0];
                select.value = favorite.id;
                select.disabled = false;
            } catch (e) {
                // ignore
            }
        }

        loadSaveFolderSelect();

        // Загрузка списка языков
        fetch('/api/search/languages')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success && data.languages) {
                    allLanguages = data.languages;
                    renderLanguageFilters();
                } else {
                    console.error('Ошибка загрузки языков:', data);
                    // Fallback на статический список
                    loadFallbackLanguages();
                }
            })
            .catch(error => {
                console.error('Ошибка при загрузке языков:', error);
                // Fallback на статический список
                loadFallbackLanguages();
            });
        
        function loadFallbackLanguages() {
            // Статический список языков как fallback
            allLanguages = ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp'];
            renderLanguageFilters();
            console.log('Использован fallback список языков');
        }

        function renderLanguageFilters() {
            const container = document.getElementById('languageFilters');
            container.innerHTML = '<span class="filter-tag active" data-lang="">Все языки</span>';
            
            allLanguages.forEach(lang => {
                const tag = document.createElement('span');
                tag.className = 'filter-tag';
                tag.textContent = lang;
                tag.dataset.lang = lang;
                tag.onclick = () => toggleLanguageFilter(lang);
                container.appendChild(tag);
            });
        }

        function toggleLanguageFilter(lang) {
            const tag = document.querySelector(`[data-lang="${lang}"]`);
            
            if (lang === '') {
                // "Все языки" выбрано
                selectedLanguages = [];
                document.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
                tag.classList.add('active');
            } else {
                // Переключаем конкретный язык
                if (selectedLanguages.includes(lang)) {
                    selectedLanguages = selectedLanguages.filter(l => l !== lang);
                    tag.classList.remove('active');
                    
                    // Если ничего не выбрано, выбираем "Все языки"
                    if (selectedLanguages.length === 0) {
                        document.querySelector('[data-lang=""]').classList.add('active');
                    }
                } else {
                    selectedLanguages.push(lang);
                    tag.classList.add('active');
                    document.querySelector('[data-lang=""]').classList.remove('active');
                }
            }
            
            // Если форма уже заполнена, выполняем поиск
            const keywords = document.getElementById('keywordsInput').value.trim();
            if (keywords) {
                performSearch(keywords, 1);
            }
        }

        // Обработка формы поиска
        document.getElementById('searchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const keywords = document.getElementById('keywordsInput').value.trim();
            if (keywords) {
                performSearch(keywords, 1);
            }
        });

        document.getElementById('applyFiltersBtn').addEventListener('click', () => {
            const keywords = document.getElementById('keywordsInput').value.trim();
            if (keywords) {
                performSearch(keywords, 1);
            }
        });

        function performSearch(keywords, page = 1) {
            const resultsContainer = document.getElementById('searchResults');
            currentKeywords = keywords;
            const source_type = document.getElementById('sourceTypeSelect').value || null;
            const source_language = document.getElementById('sourceLanguageSelect').value || null;
            const difficulty = document.getElementById('difficultySelect').value || null;
            const year = document.getElementById('yearInput').value || null;
            const sort_by = document.getElementById('sortBySelect').value || 'relevance';
            const per_page = parseInt(document.getElementById('perPageSelect').value || '20', 10);
            resultsContainer.innerHTML = '<div class="text-center py-5"><div class="spinner-border" role="status"></div><p class="mt-3">Поиск...</p></div>';
            
            const languages = selectedLanguages.length > 0 ? selectedLanguages : null;
            
            fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    keywords: keywords,
                    languages: languages,
                    source_type: source_type,
                    source_language: source_language,
                    difficulty: difficulty,
                    year: year,
                    sort_by: sort_by,
                    page: page,
                    per_page: per_page
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    renderResults(data);
                } else {
                    const errorMsg = data.error || 'Неизвестная ошибка';
                    resultsContainer.innerHTML = `<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> Ошибка: ${errorMsg}</div>`;
                }
            })
            .catch(error => {
                console.error('Ошибка поиска:', error);
                resultsContainer.innerHTML = `<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> Ошибка подключения: ${error.message}. Проверьте, что сервер запущен.</div>`;
            });
        }

        function renderResults(data) {
            const container = document.getElementById('searchResults');
            
            if (data.total_results === 0) {
                container.innerHTML = `
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle"></i> По запросу "${data.keywords}" ничего не найдено
                    </div>
                `;
                return;
            }
            
            let html = `
                <div class="mb-4">
                    <h4>Найдено результатов: ${data.total_results}</h4>
                    <p class="text-muted">Запрос: "${data.keywords}"</p>
                    ${data.languages_filter ? `<p class="text-muted">Фильтр: ${data.languages_filter.join(', ')}</p>` : ''}
                </div>
            `;
            
            data.results.forEach(result => {
                html += renderResultCard(result);
            });

            html += renderPagination(data.page, data.total_pages);
            
            container.innerHTML = html;
        }

        function renderPagination(page, totalPages) {
            page = parseInt(page || 1, 10);
            totalPages = parseInt(totalPages || 1, 10);
            if (totalPages <= 1) return '';

            const prevDisabled = page <= 1 ? 'disabled' : '';
            const nextDisabled = page >= totalPages ? 'disabled' : '';

            return `
                <div class="mt-4">
                    <div class="d-flex justify-content-center">
                        <nav aria-label="Пагинация">
                            <ul class="pagination">
                                <li class="page-item ${prevDisabled}">
                                    <a class="page-link" href="#" onclick="window.__goToPage(${page - 1}); return false;">Предыдущая</a>
                                </li>
                                <li class="page-item disabled">
                                    <span class="page-link">Страница ${page} из ${totalPages}</span>
                                </li>
                                <li class="page-item ${nextDisabled}">
                                    <a class="page-link" href="#" onclick="window.__goToPage(${page + 1}); return false;">Следующая</a>
                                </li>
                            </ul>
                        </nav>
                    </div>
                </div>
            `;
        }

        window.__goToPage = function(targetPage) {
            targetPage = parseInt(targetPage || 1, 10);
            if (!currentKeywords) return;
            if (targetPage < 1) return;
            performSearch(currentKeywords, targetPage);
        }

        function escapeAttr(text) {
            return String(text ?? '')
                .replace(/&/g, '&amp;')
                .replace(/"/g, '&quot;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;');
        }

        document.getElementById('searchResults').addEventListener('click', async (e) => {
            const btn = e.target.closest('.save-btn');
            if (!btn) return;

            const sessionRes = await fetch('/api/me/session');
            const sessionData = await sessionRes.json();
            if (!sessionData.logged_in) {
                window.location.href = '/login';
                return;
            }

            const foldersRes = await fetch('/api/me/folders');
            const foldersData = await foldersRes.json();
            if (!foldersData.success) {
                alert(foldersData.error || 'Не удалось загрузить папки');
                return;
            }

            const folders = foldersData.folders || [];
            const select = document.getElementById('saveFolderSelect');
            let chosenFolderId = null;
            if (select && select.value) {
                chosenFolderId = parseInt(select.value, 10);
            }

            const favorite = folders.find(f => f.name === 'Избранное');
            const chosenFolder = chosenFolderId ? folders.find(f => f.id === chosenFolderId) : (favorite || folders[0]);
            if (!chosenFolder) {
                alert('Нет доступных папок в кабинете');
                return;
            }

            const payload = {
                folder_id: chosenFolder.id,
                resource_uri: btn.dataset.resourceUri,
                resource_type: 'publication',
                publication_type: btn.dataset.publicationType,
                title: btn.dataset.title,
                author: btn.dataset.author,
                url: btn.dataset.url,
                keywords: btn.dataset.keywords
            };

            const saveRes = await fetch('/api/me/saved', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            const saveData = await saveRes.json();
            if (saveData.success) {
                alert('Ресурс сохранен в кабинет');
            } else {
                alert(saveData.error || 'Не удалось сохранить ресурс');
            }
        });

        function renderResultCard(result) {
            let cardClass = '';
            let icon = '';
            let title = '';
            let content = '';
            
            if (result.type === 'language') {
                cardClass = 'border-primary';
                icon = '<i class="fas fa-code text-primary"></i>';
                title = `<h5 class="card-title">${result.display_name || result.name}</h5>`;
                
                const props = result.properties || {};
                const data = result.data || {};
                
                content = `
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Создатель:</strong> ${props.creator || 'N/A'}</p>
                            <p><strong>Кривая обучения:</strong> ${props.learningCurve || 'N/A'}</p>
                            ${data.tiobeRank ? `<p><strong>TIOBE Рейтинг:</strong> #${data.tiobeRank} (${data.tiobeRating || 'N/A'})</p>` : ''}
                            ${data.githubRepositories ? `<p><strong>GitHub:</strong> ${(data.githubRepositories / 1000000).toFixed(1)}M репозиториев</p>` : ''}
                            ${data.stackOverflowQuestions ? `<p><strong>Stack Overflow:</strong> ${(data.stackOverflowQuestions / 1000).toFixed(0)}k вопросов</p>` : ''}
                        </div>
                        <div class="col-md-6">
                            ${props.paradigm ? `<p><strong>Парадигмы:</strong> ${Array.isArray(props.paradigm) ? props.paradigm.join(', ') : props.paradigm}</p>` : ''}
                            ${props.domain ? `<p><strong>Домены:</strong> ${Array.isArray(props.domain) ? props.domain.join(', ') : props.domain}</p>` : ''}
                            ${props.framework ? `<p><strong>Фреймворки:</strong> ${Array.isArray(props.framework) ? props.framework.join(', ') : props.framework}</p>` : ''}
                            ${props.typeSystem ? `<p><strong>Система типов:</strong> ${Array.isArray(props.typeSystem) ? props.typeSystem.join(', ') : props.typeSystem}</p>` : ''}
                        </div>
                    </div>
                    ${result.frameworks && result.frameworks.length > 0 ? `
                        <div class="mt-3">
                            <strong>Фреймворки:</strong>
                            ${result.frameworks.map(f => `<span class="language-badge">${f}</span>`).join('')}
                        </div>
                    ` : ''}
                `;
            } else if (result.type === 'publication') {
                cardClass = 'border-success';
                
                // Определяем тип публикации и иконку
                let pubType = 'Публикация';
                let typeIcon = '<i class="fas fa-file-alt text-success"></i>';
                if (result.publication_type === 'Book') {
                    pubType = 'Книга';
                    typeIcon = '<i class="fas fa-book text-success"></i>';
                } else if (result.publication_type === 'Documentation') {
                    pubType = 'Документация';
                    typeIcon = '<i class="fas fa-book-open text-info"></i>';
                } else if (result.publication_type === 'Tutorial') {
                    pubType = 'Туториал';
                    typeIcon = '<i class="fas fa-graduation-cap text-warning"></i>';
                } else if (result.publication_type === 'Article') {
                    pubType = 'Статья';
                    typeIcon = '<i class="fas fa-newspaper text-primary"></i>';
                }
                
                icon = typeIcon;
                title = `<h5 class="card-title">${result.title || result.name}</h5>`;
                
                const hasUrl = result.url && result.url.trim() !== '';
                
                content = `
                    <p><strong>Тип:</strong> ${pubType}</p>
                    ${result.keywords ? `<p><strong>Ключевые слова:</strong> ${result.keywords}</p>` : ''}
                    ${result.language ? `<p><strong>О языке:</strong> ${result.language}</p>` : ''}
                    ${result.author ? `<p><strong>Автор:</strong> ${result.author}</p>` : ''}
                    ${hasUrl ? `
                    <div class="mt-3">
                        <a href="${result.url}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary">
                            <i class="fas fa-external-link-alt"></i> Открыть источник
                        </a>
                        ${result.language ? `
                        <a href="/language/${result.language}/sources" class="btn btn-sm btn-outline-secondary ms-2">
                            <i class="fas fa-list"></i> Все источники ${result.language}
                        </a>
                        ` : ''}
                        <button class="btn btn-sm btn-outline-success ms-2 save-btn" type="button"
                                data-resource-uri="${escapeAttr(result.uri || '')}"
                                data-publication-type="${escapeAttr(result.publication_type || '')}"
                                data-title="${escapeAttr(result.title || '')}"
                                data-author="${escapeAttr(result.author || '')}"
                                data-url="${escapeAttr(result.url || '')}"
                                data-keywords="${escapeAttr(result.keywords || '')}">
                            <i class="fas fa-bookmark"></i> Сохранить
                        </button>
                    </div>
                    ` : result.language ? `
                    <div class="mt-3">
                        <a href="/language/${result.language}/sources" class="btn btn-sm btn-outline-secondary">
                            <i class="fas fa-list"></i> Все источники ${result.language}
                        </a>
                        <button class="btn btn-sm btn-outline-success ms-2 save-btn" type="button"
                                data-resource-uri="${escapeAttr(result.uri || '')}"
                                data-publication-type="${escapeAttr(result.publication_type || '')}"
                                data-title="${escapeAttr(result.title || '')}"
                                data-author="${escapeAttr(result.author || '')}"
                                data-url="${escapeAttr(result.url || '')}"
                                data-keywords="${escapeAttr(result.keywords || '')}">
                            <i class="fas fa-bookmark"></i> Сохранить
                        </button>
                    </div>
                    ` : ''}
                `;
            } else if (result.type === 'framework') {
                cardClass = 'border-warning';
                icon = '<i class="fas fa-cube text-warning"></i>';
                title = `<h5 class="card-title">${result.name}</h5>`;
                
                content = `
                    <p><strong>Тип:</strong> Фреймворк</p>
                    ${result.language ? `<p><strong>Язык:</strong> ${result.language}</p>` : ''}
                `;
            }
            
            return `
                <div class="card result-card ${cardClass} position-relative">
                    <div class="card-body">
                        <span class="badge bg-secondary relevance-badge">Релевантность: ${result.relevance?.toFixed(1) || 0}%</span>
                        ${icon}
                        ${title}
                        ${content}
                    </div>
                </div>
            `;
        }
    </script>
</body>
</html>''')

    # Детали языка
    with open('templates/language_detail.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Детали языка</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-code"></i> Языки Программирования
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/dashboard">Дашборд</a>
                <a class="nav-link" href="/languages">Языки</a>
                <a class="nav-link" href="/search">Поиск</a>
                <a class="nav-link" href="/cabinet" title="Личный кабинет">
                    <i class="fas fa-user"></i>
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <a href="/languages" class="btn btn-secondary mb-3">
            ← Назад к списку
        </a>
        
        <div id="language-details">
            <div class="text-center">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <p>Загрузка данных...</p>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const languageName = '{{ language_name }}';
        
        fetch(`/api/language/${languageName}`)
            .then(response => response.json())
            .then(details => {
                const container = document.getElementById('language-details');
                
                let html = `<h2>${languageName}</h2>`;
                html += '<div class="row mt-4"><div class="col-md-8"><table class="table table-striped"><tbody>';
                
                for (const [key, value] of Object.entries(details)) {
                    html += `<tr><td><strong>${key}</strong></td><td>${value}</td></tr>`;
                }
                
                html += '</tbody></table></div></div>';
                container.innerHTML = html;
            });
    </script>
</body>
</html>''')

    # Страница всех источников для языка
    with open('templates/language_sources.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Источники - {{ language_name }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .source-card {
            border: none;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .source-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .type-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .type-book { background: #e3f2fd; color: #1976d2; }
        .type-article { background: #f3e5f5; color: #7b1fa2; }
        .type-documentation { background: #e8f5e9; color: #388e3c; }
        .type-tutorial { background: #fff3e0; color: #f57c00; }
        .section-header {
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
            margin-bottom: 20px;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-code"></i> Языки Программирования
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/dashboard">Дашборд</a>
                <a class="nav-link" href="/languages">Языки</a>
                <a class="nav-link" href="/search">Поиск</a>
                <a class="nav-link" href="/cabinet" title="Личный кабинет">
                    <i class="fas fa-user"></i>
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <a href="/languages" class="btn btn-secondary mb-3">
            <i class="fas fa-arrow-left"></i> Назад к списку языков
        </a>
        
        <h1 class="mb-4">
            <i class="fas fa-book"></i> Все источники для <span id="language-name">{{ language_name }}</span>
        </h1>
        
        <div id="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
            <p class="mt-3">Загрузка источников...</p>
        </div>
        
        <div id="sources-container" style="display: none;">
            <div id="summary" class="alert alert-info mb-4">
                <strong>Всего источников: <span id="total-count">0</span></strong>
            </div>
            
            <div id="books-section"></div>
            <div id="articles-section"></div>
            <div id="documentation-section"></div>
            <div id="tutorials-section"></div>
        </div>
        
        <div id="error-message" class="alert alert-danger" style="display: none;"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const languageName = '{{ language_name }}';
        
        // Отображение имени языка в читаемом формате
        const languageDisplayNames = {
            'Python': 'Python',
            'Java': 'Java',
            'JavaScript': 'JavaScript',
            'C': 'C',
            'CPlusPlus': 'C++',
            'CSharp': 'C#'
        };
        
        document.getElementById('language-name').textContent = languageDisplayNames[languageName] || languageName;
        
        // Загрузка источников
        fetch(`/api/sources/language/${languageName}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    displaySources(data.publications);
                } else {
                    showError(data.error || 'Не удалось загрузить источники');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                showError('Ошибка подключения: ' + error.message);
            });
        
        function displaySources(publications) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('sources-container').style.display = 'block';
            
            // Подсчитываем по типам
            const books = publications.filter(p => p.type === 'Book');
            const articles = publications.filter(p => p.type === 'Article');
            const docs = publications.filter(p => p.type === 'Documentation');
            const tutorials = publications.filter(p => p.type === 'Tutorial');
            
            document.getElementById('total-count').textContent = publications.length;
            
            // Отображаем книги
            if (books.length > 0) {
                displaySection('books-section', '📚 Книги', books, 'type-book', 'book');
            }
            
            // Отображаем статьи
            if (articles.length > 0) {
                displaySection('articles-section', '📄 Статьи', articles, 'type-article', 'article');
            }
            
            // Отображаем документацию
            if (docs.length > 0) {
                displaySection('documentation-section', '📖 Документация', docs, 'type-documentation', 'documentation');
            }
            
            // Отображаем туториалы
            if (tutorials.length > 0) {
                displaySection('tutorials-section', '🎓 Туториалы', tutorials, 'type-tutorial', 'tutorial');
            }
            
            // Если нет источников
            if (publications.length === 0) {
                document.getElementById('sources-container').innerHTML = 
                    '<div class="alert alert-warning"><i class="fas fa-info-circle"></i> Для этого языка пока нет источников.</div>';
            }
        }
        
        function displaySection(sectionId, title, items, badgeClass, type) {
            const section = document.getElementById(sectionId);
            let html = `<h3 class="section-header">${title} <span class="badge bg-secondary">${items.length}</span></h3>`;
            html += '<div class="row">';
            
            items.forEach(item => {
                html += `
                    <div class="col-md-6 col-lg-4 mb-3">
                        <div class="card source-card h-100">
                            <div class="card-body">
                                <span class="type-badge ${badgeClass}">${getTypeLabel(item.type)}</span>
                                <h5 class="card-title mt-2">${escapeHtml(item.title || 'Без названия')}</h5>
                                ${item.author ? `<p class="text-muted mb-2"><i class="fas fa-user"></i> ${escapeHtml(item.author)}</p>` : ''}
                                ${item.keywords ? `<p class="small text-muted mb-2"><i class="fas fa-tags"></i> ${escapeHtml(item.keywords)}</p>` : ''}
                                ${item.url ? `<a href="${escapeHtml(item.url)}" target="_blank" class="btn btn-sm btn-outline-primary mt-2"><i class="fas fa-external-link-alt"></i> Открыть</a>` : ''}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
            section.innerHTML = html;
        }
        
        function getTypeLabel(type) {
            const labels = {
                'Book': 'Книга',
                'Article': 'Статья',
                'Documentation': 'Документация',
                'Tutorial': 'Туториал'
            };
            return labels[type] || type;
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        function showError(message) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('error-message').style.display = 'block';
            document.getElementById('error-message').innerHTML = 
                `<i class="fas fa-exclamation-triangle"></i> ${escapeHtml(message)}`;
        }
    </script>
</body>
</html>''')

    print("✅ HTML шаблоны созданы!")

class OntologyWebManager:
    def __init__(self):
        self.g = Graph()
        self.load_ontology()
    
    def load_ontology(self):
        """Загрузка онтологии"""
        try:
            if os.path.exists(ONTOLOGY_PATH):
                self.g.parse(ONTOLOGY_PATH, format="turtle")
                print(f"✅ Онтология загружена: {len(self.g)} триплов")
                return True
            else:
                print(f"❌ Файл онтологии не найден: {ONTOLOGY_PATH}")
                return False
        except Exception as e:
            print(f"❌ Ошибка загрузки онтологии: {e}")
            return False
    
    def get_all_languages(self):
        """Получение всех языков с данными"""
        query = """
        SELECT ?lang ?tiobeRank ?tiobeRating ?githubRepos ?githubStars ?stackOverflowQuestions 
        WHERE {
          ?lang a onto:ProgrammingLanguage .
          OPTIONAL { ?lang onto:tiobeRank ?tiobeRank . }
          OPTIONAL { ?lang onto:tiobeRating ?tiobeRating . }
          OPTIONAL { ?lang onto:githubRepositories ?githubRepos . }
          OPTIONAL { ?lang onto:githubStars ?githubStars . }
          OPTIONAL { ?lang onto:stackOverflowQuestions ?stackOverflowQuestions . }
        }
        ORDER BY ?tiobeRank
        """
        
        results = self.g.query(query, initNs={"onto": NS})
        languages = []
        
        for row in results:
            lang_name = str(row[0]).split("/")[-1]
            language_data = {
                'name': lang_name,
                'display_name': self._get_display_name(lang_name),
                'tiobe_rank': int(row[1]) if row[1] else None,
                'tiobe_rating': str(row[2]) if row[2] else None,
                'github_repos': int(row[3]) if row[3] else None,
                'github_stars': int(row[4]) if row[4] else None,
                'stackoverflow_questions': int(row[5]) if row[5] else None
            }
            languages.append(language_data)
        
        return languages
    
    def get_language_details(self, language_name):
        """Получение детальной информации о языке"""
        lang_uri = NS[language_name]
        
        query = """
        SELECT ?property ?value WHERE {
          ?lang ?property ?value .
          FILTER(?lang = onto:%s)
        }
        """ % language_name
        
        results = self.g.query(query, initNs={"onto": NS})
        details = {}
        
        for row in results:
            prop_name = str(row[0]).split("/")[-1]
            value = row[1]
            details[prop_name] = str(value)
        
        return details
    
    def _get_display_name(self, internal_name):
        """Преобразование внутреннего имени в отображаемое"""
        name_mapping = {
            'Python': 'Python',
            'Java': 'Java',
            'JavaScript': 'JavaScript',
            'C': 'C',
            'CPlusPlus': 'C++',
            'CSharp': 'C#'
        }
        return name_mapping.get(internal_name, internal_name)

# Инициализация менеджера онтологии
ontology_manager = OntologyWebManager()

# Инициализация поискового модуля
try:
    search_engine = OntologySearch()
    print("✅ Поисковый модуль инициализирован")
except Exception as e:
    print(f"⚠️ Ошибка инициализации поискового модуля: {e}")
    # Создаем заглушку для работы без поиска
    class DummySearchEngine:
        def get_all_languages(self):
            return ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp']
        def search_by_keywords(self, keywords, languages=None):
            return []
        def search_by_language(self, name):
            return None
    search_engine = DummySearchEngine()

# Инициализация менеджера публикаций
try:
    publication_manager = PublicationManager()
    print("✅ Менеджер публикаций инициализирован")
except Exception as e:
    print(f"⚠️ Ошибка инициализации менеджера публикаций: {e}")
    publication_manager = None

# =========================
# Личный кабинет (auth)
# =========================

def _get_logged_in_user_id() -> Optional[int]:
    user_id = session.get("user_id")
    try:
        if user_id is None:
            return None
        return int(user_id)
    except Exception:
        return None


@app.route("/api/me/session", methods=["GET"])
def api_me_session():
    user_id = _get_logged_in_user_id()
    if not user_id:
        return jsonify({"logged_in": False})
    user = get_user_by_id(user_id)
    if not user:
        session.pop("user_id", None)
        return jsonify({"logged_in": False})
    return jsonify({"logged_in": True, "user": {"id": int(user["id"]), "username": user["username"]}})


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if _get_logged_in_user_id():
            return redirect("/cabinet")
        return render_template("register.html")

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    password2 = request.form.get("password2") or ""

    if not username or len(password) < 4:
        return render_template("register.html", error="Имя пользователя или пароль слишком короткие"), 400
    if password != password2:
        return render_template("register.html", error="Пароли не совпадают"), 400

    existing = get_user_by_username(username)
    if existing:
        return render_template("register.html", error="Пользователь с таким именем уже существует"), 400

    password_hash = generate_password_hash(password)
    user_id = None
    try:
        user_id = create_user(username, password_hash)
    except Exception:
        user_id = None

    if not user_id:
        return render_template("register.html", error="Не удалось создать пользователя"), 500

    session["user_id"] = int(user_id)
    # На старте создаем папку "Избранное", чтобы кабинет был сразу готов.
    try:
        ensure_default_folder_exists(int(user_id))
    except Exception:
        pass
    return redirect("/cabinet")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if _get_logged_in_user_id():
            return redirect("/cabinet")
        return render_template("login.html")

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    user = get_user_by_username(username)
    if not user:
        return render_template("login.html", error="Неверное имя пользователя или пароль"), 400

    if not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Неверное имя пользователя или пароль"), 400

    session["user_id"] = int(user["id"])
    return redirect("/cabinet")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("user_id", None)
    return redirect("/")


@app.route("/cabinet", methods=["GET"])
def cabinet():
    user_id = _get_logged_in_user_id()
    if not user_id:
        return redirect("/login")
    return render_template("cabinet.html", user_id=user_id)

# =========================
# API кабинета (папки/сохранения)
# =========================


@app.route("/api/me/folders", methods=["GET"])
def api_me_folders_get():
    user_id = _get_logged_in_user_id()
    if not user_id:
        return jsonify({"success": False, "error": "Требуется авторизация"}), 401
    return jsonify({"success": True, "folders": list_folders(int(user_id))})


@app.route("/api/me/folders", methods=["POST"])
def api_me_folders_post():
    user_id = _get_logged_in_user_id()
    if not user_id:
        return jsonify({"success": False, "error": "Требуется авторизация"}), 401

    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"success": False, "error": "Не указано имя папки"}), 400

    folder_id = create_folder(int(user_id), name)
    if not folder_id:
        return jsonify({"success": False, "error": "Не удалось создать папку"}), 400
    return jsonify({"success": True, "folder_id": int(folder_id)})


@app.route("/api/me/folders/<int:folder_id>", methods=["DELETE"])
def api_me_folders_delete(folder_id: int):
    user_id = _get_logged_in_user_id()
    if not user_id:
        return jsonify({"success": False, "error": "Требуется авторизация"}), 401
    ok = delete_folder(int(user_id), int(folder_id))
    return jsonify({"success": ok})


@app.route("/api/me/saved", methods=["GET"])
def api_me_saved_get():
    user_id = _get_logged_in_user_id()
    if not user_id:
        return jsonify({"success": False, "error": "Требуется авторизация"}), 401

    folder_id = request.args.get("folder_id", None)
    parsed_folder_id = None
    if folder_id not in (None, "", "null"):
        try:
            parsed_folder_id = int(folder_id)
        except Exception:
            parsed_folder_id = None

    # Если задан folder_id — проверяем принадлежность.
    if parsed_folder_id is not None and not folder_belongs_to_user(int(user_id), parsed_folder_id):
        return jsonify({"success": False, "error": "Папка не принадлежит пользователю"}), 403

    resources = list_saved_resources(int(user_id), parsed_folder_id)
    return jsonify({"success": True, "resources": resources})


@app.route("/api/me/saved", methods=["POST"])
def api_me_saved_post():
    user_id = _get_logged_in_user_id()
    if not user_id:
        return jsonify({"success": False, "error": "Требуется авторизация"}), 401

    data = request.get_json() or {}
    folder_id = data.get("folder_id", None)
    try:
        folder_id = int(folder_id)
    except Exception:
        return jsonify({"success": False, "error": "Не указан или неверный folder_id"}), 400

    if not folder_belongs_to_user(int(user_id), folder_id):
        return jsonify({"success": False, "error": "Папка не принадлежит пользователю"}), 403

    resource_uri = (data.get("resource_uri") or "").strip()
    resource_type = (data.get("resource_type") or "publication").strip()
    publication_type = (data.get("publication_type") or "").strip() or None
    title_snapshot = data.get("title") or data.get("title_snapshot")
    author_snapshot = data.get("author") or data.get("author_snapshot")
    url_snapshot = data.get("url") or data.get("url_snapshot")
    keywords_snapshot = data.get("keywords") or data.get("keywords_snapshot")

    if not resource_uri:
        return jsonify({"success": False, "error": "Не указано resource_uri"}), 400

    ok = save_resource(
        int(user_id),
        int(folder_id),
        resource_uri=resource_uri,
        resource_type=resource_type,
        publication_type=publication_type,
        title_snapshot=title_snapshot,
        author_snapshot=author_snapshot,
        url_snapshot=url_snapshot,
        keywords_snapshot=keywords_snapshot,
    )
    if not ok:
        return jsonify({"success": False, "error": "Не удалось сохранить ресурс"}), 400
    return jsonify({"success": True})


@app.route("/api/me/saved/<int:saved_id>/move", methods=["POST"])
def api_me_saved_move(saved_id: int):
    user_id = _get_logged_in_user_id()
    if not user_id:
        return jsonify({"success": False, "error": "Требуется авторизация"}), 401

    data = request.get_json() or {}
    new_folder_id = data.get("new_folder_id", None)
    try:
        new_folder_id = int(new_folder_id)
    except Exception:
        return jsonify({"success": False, "error": "Не указан или неверный new_folder_id"}), 400

    if not folder_belongs_to_user(int(user_id), new_folder_id):
        return jsonify({"success": False, "error": "Папка не принадлежит пользователю"}), 403

    ok = move_saved_resource(int(user_id), int(saved_id), int(new_folder_id))
    return jsonify({"success": ok})


@app.route("/api/me/saved/<int:saved_id>", methods=["DELETE"])
def api_me_saved_delete(saved_id: int):
    user_id = _get_logged_in_user_id()
    if not user_id:
        return jsonify({"success": False, "error": "Требуется авторизация"}), 401
    ok = delete_saved_resource(int(user_id), int(saved_id))
    return jsonify({"success": ok})


@app.route("/api/me/export", methods=["GET"])
def api_me_export():
    user_id = _get_logged_in_user_id()
    if not user_id:
        return jsonify({"success": False, "error": "Требуется авторизация"}), 401

    fmt = (request.args.get("format") or "bibtex").lower()
    folder_id = request.args.get("folder_id", None)
    parsed_folder_id = None
    if folder_id not in (None, "", "null"):
        try:
            parsed_folder_id = int(folder_id)
        except Exception:
            parsed_folder_id = None

    if parsed_folder_id is not None and not folder_belongs_to_user(int(user_id), parsed_folder_id):
        return jsonify({"success": False, "error": "Папка не принадлежит пользователю"}), 403

    saved_ids_arg = request.args.get("saved_ids", None)
    resources = None
    if saved_ids_arg not in (None, "", "null"):
        # Ожидаем формат: "1,2,3"
        try:
            saved_ids = [int(x.strip()) for x in str(saved_ids_arg).split(",") if str(x).strip()]
        except Exception:
            saved_ids = []

        if saved_ids:
            resources = list_saved_resources_by_ids(int(user_id), saved_ids)

    if resources is None:
        # Фоллбек: экспорт всей папки (или всех ресурсов пользователя, если folder_id не указан)
        resources = list_saved_resources(int(user_id), parsed_folder_id)
    if fmt != "bibtex":
        return jsonify({"success": False, "error": f"Неподдерживаемый формат: {fmt}"}), 400

    bibtex = export_bibtex_for_resources(resources)
    return jsonify({"success": True, "bibtex": bibtex})

# Маршруты Flask
@app.route('/')
def index():
    """Главная страница дашборда"""
    return render_template('index.html')

@app.route('/api/languages')
def get_languages():
    """API для получения всех языков"""
    languages = ontology_manager.get_all_languages()
    return jsonify(languages)

@app.route('/api/language/<name>')
def get_language(name):
    """API для получения конкретного языка"""
    details = ontology_manager.get_language_details(name)
    return jsonify(details)

@app.route('/api/stats')
def get_stats():
    """API для общей статистики"""
    languages = ontology_manager.get_all_languages()
    
    stats = {
        'total_languages': len(languages),
        'languages_with_tiobe': len([l for l in languages if l['tiobe_rank']]),
        'languages_with_github': len([l for l in languages if l['github_repos']]),
        'languages_with_stackoverflow': len([l for l in languages if l['stackoverflow_questions']]),
        'last_updated': datetime.now().isoformat()
    }
    
    return jsonify(stats)

@app.route('/api/chart/tiobe')
def chart_tiobe():
    """Генерация графика TIOBE рейтингов"""
    try:
        languages = ontology_manager.get_all_languages()
        
        # Фильтруем языки с TIOBE рейтингом
        languages_with_rating = [l for l in languages if l.get('tiobe_rating')]
        
        if not languages_with_rating:
            return jsonify({'error': 'Нет данных TIOBE'}), 404
        
        languages_with_rating.sort(key=lambda x: x.get('tiobe_rank') or 999)
        
        # Берем топ-6
        top_languages = languages_with_rating[:6]
        
        if not top_languages:
            return jsonify({'error': 'Нет данных для графика'}), 404
        
        names = [lang['display_name'] for lang in top_languages]
        ratings = []
        for lang in top_languages:
            rating_str = str(lang.get('tiobe_rating', '0%'))
            try:
                rating_val = float(rating_str.replace('%', '').strip())
                ratings.append(rating_val)
            except:
                ratings.append(0.0)
        
        # Создаем график - уменьшенный размер
        plt.figure(figsize=(10, 5))
        plt.rcParams['font.size'] = 9
        bars = plt.bar(names, ratings, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
        plt.title('TIOBE Рейтинги - Топ 6 Языков', fontsize=14, fontweight='bold', pad=15)
        plt.ylabel('Рейтинг (%)', fontsize=11)
        plt.xlabel('Языки программирования', fontsize=11)
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(fontsize=9)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Добавляем значения на столбцы
        for bar, rating in zip(bars, ratings):
            if rating > 0:
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(ratings)*0.02, 
                        f'{rating:.2f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        
        # Сохраняем в base64 для HTML
        img = io.BytesIO()
        try:
            # Убеждаемся, что фигура создана
            if not plt.get_fignums():
                raise ValueError("График не был создан")
            
            plt.savefig(img, format='png', dpi=100, bbox_inches='tight', facecolor='white', edgecolor='none', pad_inches=0.2)
            img.seek(0)
            
            # Проверяем, что изображение не пустое
            img_data = img.getvalue()
            if len(img_data) < 1000:  # Минимальный размер для PNG
                raise ValueError("Изображение слишком маленькое")
            
            chart_url = base64.b64encode(img_data).decode()
            plt.close('all')  # Закрываем все фигуры
            
            return jsonify({'chart': f'data:image/png;base64,{chart_url}'})
        except Exception as e:
            plt.close('all')
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Ошибка создания графика: {str(e)}'}), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart/github')
def chart_github():
    """Генерация графика GitHub репозиториев"""
    try:
        languages = ontology_manager.get_all_languages()
        
        # Фильтруем языки с GitHub данными
        languages_with_github = [l for l in languages if l.get('github_repos')]
        
        if not languages_with_github:
            return jsonify({'error': 'Нет данных GitHub'}), 404
        
        languages_with_github.sort(key=lambda x: x.get('github_repos') or 0, reverse=True)
        
        # Берем топ-6
        top_languages = languages_with_github[:6]
        
        if not top_languages:
            return jsonify({'error': 'Нет данных для графика'}), 404
        
        names = [lang['display_name'] for lang in top_languages]
        repos = [lang.get('github_repos', 0) / 1000000 for lang in top_languages]  # в миллионах
        
        # Создаем график - уменьшенный размер
        plt.figure(figsize=(10, 5))
        plt.rcParams['font.size'] = 9
        bars = plt.bar(names, repos, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
        plt.title('GitHub Репозитории - Топ 6 Языков (в миллионах)', fontsize=14, fontweight='bold', pad=15)
        plt.ylabel('Количество репозиториев (млн)', fontsize=11)
        plt.xlabel('Языки программирования', fontsize=11)
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(fontsize=9)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Добавляем значения на столбцы
        for bar, repo in zip(bars, repos):
            if repo > 0:
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(repos)*0.02, 
                        f'{repo:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        
        # Сохраняем в base64 для HTML
        img = io.BytesIO()
        try:
            plt.savefig(img, format='png', dpi=100, bbox_inches='tight', facecolor='white', edgecolor='none')
            img.seek(0)
            chart_url = base64.b64encode(img.getvalue()).decode()
            plt.close('all')
            return jsonify({'chart': f'data:image/png;base64,{chart_url}'})
        except Exception as e:
            plt.close('all')
            raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Страница дашборда с графиками"""
    return render_template('dashboard.html')

@app.route('/languages')
def languages_page():
    """Страница списка языков"""
    return render_template('languages.html')

@app.route('/language/<name>')
def language_detail(name):
    """Страница деталей языка"""
    return render_template('language_detail.html', language_name=name)

@app.route('/language/<name>/sources')
def language_sources(name):
    """Страница всех источников для языка"""
    return render_template('language_sources.html', language_name=name)

# ========== ПОИСКОВЫЕ API ENDPOINTS ==========

@app.route('/search')
def search_page():
    """Страница поиска"""
    # Поддержка GET параметра q для поиска с главной страницы
    query = request.args.get('q', '')
    return render_template('search.html', initial_query=query)

@app.route('/api/search', methods=['GET', 'POST'])
def api_search():
    """API для поиска по ключевым словам с расширенными фильтрами"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'Нет данных в запросе'}), 400
            keywords = data.get('keywords', '')
            languages = data.get('languages', None)
            # Новые фильтры
            source_type = data.get('source_type', None)  # Book, Article, Documentation, Tutorial
            source_language = data.get('source_language', None)  # русский, английский
            difficulty = data.get('difficulty', None)  # начальный, средний, продвинутый
            include_external_always = bool(data.get('include_external_always', False))
            year = data.get('year', None)  # Год публикации
            if year is not None and str(year).strip() == '':
                year = None
            if year is not None:
                try:
                    year = int(year)
                except Exception:
                    year = None
            sort_by = data.get('sort_by', 'relevance')  # relevance, date, popularity
            page = data.get('page', 1)
            per_page = data.get('per_page', 20)
        else:
            keywords = request.args.get('keywords', '')
            languages_str = request.args.get('languages', '')
            languages = languages_str.split(',') if languages_str else None
            source_type = request.args.get('source_type', None)
            source_language = request.args.get('source_language', None)
            difficulty = request.args.get('difficulty', None)
            include_external_always = str(request.args.get('include_external_always', 'false')).lower() in ('1', 'true', 'yes', 'on')
            year = request.args.get('year', None)
            if year is not None and str(year).strip() == '':
                year = None
            if year is not None:
                try:
                    year = int(year)
                except Exception:
                    year = None
            sort_by = request.args.get('sort_by', 'relevance')
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 20))
        
        if not keywords:
            return jsonify({'success': False, 'error': 'Ключевые слова не указаны'}), 400
        
        results = search_engine.search_by_keywords(
            keywords,
            languages,
            include_external_always=include_external_always
        )
        
        # Применяем дополнительные фильтры
        filtered_results = results
        
        if source_type:
            filtered_results = [r for r in filtered_results if r.get('type') == 'publication' and r.get('publication_type') == source_type]
        
        if source_language:
            filtered_results = [r for r in filtered_results if source_language.lower() in (r.get('keywords', '') + ' ' + r.get('title', '')).lower()]
        
        if difficulty:
            difficulty_keywords = {
                'начальный': ['начальный', 'beginner', 'для начинающих', 'обучение', 'basics'],
                'средний': ['средний', 'intermediate', 'средний уровень'],
                'продвинутый': ['продвинутый', 'advanced', 'expert', 'глубокий']
            }
            keywords_list = difficulty_keywords.get(difficulty.lower(), [])
            filtered_results = [r for r in filtered_results if any(kw in (r.get('keywords', '') + ' ' + r.get('title', '')).lower() for kw in keywords_list)]
        
        if year is not None:
            # Фильтруем по году публикации (если есть в данных)
            filtered_results = [r for r in filtered_results if r.get('year') == year]
        
        # Сортировка
        if sort_by == 'relevance':
            filtered_results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        elif sort_by == 'date':
            # Сортируем по году, если есть
            filtered_results.sort(key=lambda x: int(x.get('year') or 0), reverse=True)
        elif sort_by == 'popularity':
            # Сортируем по релевантности как заменитель популярности
            filtered_results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        
        # Пагинация
        total = len(filtered_results)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_results = filtered_results[start:end]
        
        fallback_used = any(r.get('is_fallback') for r in paginated_results)
        avg_quality_score = 0.0
        quality_values = [r.get('quality', {}).get('total_score') for r in paginated_results if r.get('quality')]
        if quality_values:
            avg_quality_score = round(sum(quality_values) / len(quality_values), 1)

        return jsonify({
            'success': True,
            'keywords': keywords,
            'languages_filter': languages,
            'source_type_filter': source_type,
            'source_language_filter': source_language,
            'difficulty_filter': difficulty,
            'include_external_always': include_external_always,
            'year_filter': year,
            'sort_by': sort_by,
            'total_results': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'fallback_used': fallback_used,
            'avg_quality_score': avg_quality_score,
            'results': paginated_results
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search/language/<name>')
def api_search_language(name):
    """API для получения информации о конкретном языке"""
    try:
        result = search_engine.search_by_language(name)
        
        if result:
            return jsonify({
                'success': True,
                'language': result
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Язык {name} не найден'
            }), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/languages')
def api_get_all_languages():
    """API для получения списка всех доступных языков"""
    try:
        languages = search_engine.get_all_languages()
        
        if not languages:
            # Fallback на статический список
            languages = ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp']
        
        return jsonify({
            'success': True,
            'total': len(languages),
            'languages': languages
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Возвращаем fallback список даже при ошибке
        return jsonify({
            'success': True,
            'total': 6,
            'languages': ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp']
        })

@app.route('/api/search/save_external', methods=['POST'])
def api_save_external_result():
    """Сохранение выбранного внешнего результата в онтологию."""
    try:
        data = request.get_json() or {}
        title = (data.get('title') or '').strip()
        url = (data.get('url') or '').strip()
        source_name = (data.get('source_name') or 'Browser Search').strip()
        query_text = (data.get('query_text') or '').strip()
        language = (data.get('language') or '').strip() or None
        confidence_score = data.get('confidence_score', None)
        
        if not title or not url:
            return jsonify({'success': False, 'error': 'Не указаны title/url'}), 400
        
        ok = search_engine.save_external_result(
            title=title,
            url=url,
            source_name=source_name,
            query_text=query_text,
            language=language,
            confidence_score=confidence_score
        )
        if not ok:
            return jsonify({'success': False, 'error': 'Не удалось сохранить источник'}), 500
        
        return jsonify({'success': True, 'message': 'Источник сохранен в онтологию'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search/save_fact', methods=['POST'])
def api_save_fact_result():
    """Сохранение извлеченного факта из внешнего источника в онтологию."""
    try:
        data = request.get_json() or {}
        query_text = (data.get('query_text') or '').strip()
        language = (data.get('language') or '').strip()
        material_type = (data.get('material_type') or 'Article').strip()
        fact_text = (data.get('fact_text') or '').strip()
        source_url = (data.get('source_url') or '').strip()
        source_name = (data.get('source_name') or 'Browser Source').strip()
        title = (data.get('title') or 'Сохраненный факт').strip()

        if not fact_text or not source_url:
            return jsonify({'success': False, 'error': 'Не указаны fact_text/source_url'}), 400

        ok = search_engine.save_knowledge_fact(
            query_text=query_text,
            language=language,
            material_type=material_type,
            fact_text=fact_text,
            source_url=source_url,
            source_name=source_name,
            title=title
        )
        if not ok:
            return jsonify({'success': False, 'error': 'Не удалось сохранить факт'}), 500
        return jsonify({'success': True, 'message': 'Факт сохранен в онтологию'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/languages/popular')
def api_get_popular_languages():
    """API для получения популярных языков с количеством источников"""
    try:
        if not publication_manager:
            return jsonify({'success': False, 'error': 'Менеджер публикаций не инициализирован'}), 500
        
        all_languages = search_engine.get_all_languages()
        if not all_languages:
            all_languages = ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp']
        
        languages_with_sources = []
        for lang in all_languages:
            try:
                publications = publication_manager.get_publications_for_language(lang)
                source_count = len(publications)
                # Получаем display_name из search_engine
                display_name = search_engine._get_display_name(lang) if hasattr(search_engine, '_get_display_name') else lang
                languages_with_sources.append({
                    'name': lang,
                    'display_name': display_name,
                    'source_count': source_count
                })
            except Exception as e:
                # Если не удалось получить источники, добавляем с 0
                display_name = search_engine._get_display_name(lang) if hasattr(search_engine, '_get_display_name') else lang
                languages_with_sources.append({
                    'name': lang,
                    'display_name': display_name,
                    'source_count': 0
                })
        
        # Сортируем по количеству источников (по убыванию)
        languages_with_sources.sort(key=lambda x: x['source_count'], reverse=True)
        
        return jsonify({
            'success': True,
            'languages': languages_with_sources
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========== API ДЛЯ УПРАВЛЕНИЯ ИСТОЧНИКАМИ ==========

@app.route('/sources')
def sources_page():
    """Страница управления источниками"""
    return render_template('sources.html')

@app.route('/api/sources/language/<name>')
def api_get_sources_for_language(name):
    """API для получения источников для языка"""
    try:
        if not publication_manager:
            return jsonify({'success': False, 'error': 'Менеджер публикаций не инициализирован'}), 500
        
        publications = publication_manager.get_publications_for_language(name)
        
        return jsonify({
            'success': True,
            'language': name,
            'publications': publications,
            'total': len(publications)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sources/add', methods=['POST'])
def api_add_source():
    """API для добавления источника"""
    try:
        if not publication_manager:
            return jsonify({'success': False, 'error': 'Менеджер публикаций не инициализирован'}), 500
        
        data = request.get_json()
        source_type = data.get('type')  # book, article, documentation, tutorial
        language = data.get('language')
        title = data.get('title')
        
        if not source_type or not language or not title:
            return jsonify({'success': False, 'error': 'Не указаны обязательные поля'}), 400
        
        success = False
        
        if source_type == 'book':
            success = publication_manager.add_book(
                title=title,
                language=language,
                author=data.get('author'),
                isbn=data.get('isbn'),
                keywords=data.get('keywords'),
                description=data.get('description'),
                url=data.get('url'),
                year=data.get('year'),
                difficulty=data.get('difficulty')
            )
        elif source_type == 'article':
            if not data.get('url'):
                return jsonify({'success': False, 'error': 'URL обязателен для статьи'}), 400
            success = publication_manager.add_article(
                title=title,
                language=language,
                url=data.get('url'),
                author=data.get('author'),
                keywords=data.get('keywords'),
                description=data.get('description'),
                doi=data.get('doi'),
                publication_date=data.get('publication_date')
            )
        elif source_type == 'documentation':
            if not data.get('url'):
                return jsonify({'success': False, 'error': 'URL обязателен для документации'}), 400
            success = publication_manager.add_documentation(
                title=title,
                language=language,
                url=data.get('url'),
                description=data.get('description')
            )
        elif source_type == 'tutorial':
            if not data.get('url'):
                return jsonify({'success': False, 'error': 'URL обязателен для туториала'}), 400
            success = publication_manager.add_tutorial(
                title=title,
                language=language,
                url=data.get('url'),
                difficulty=data.get('difficulty'),
                keywords=data.get('keywords')
            )
        else:
            return jsonify({'success': False, 'error': f'Неизвестный тип источника: {source_type}'}), 400
        
        if success:
            # Сохраняем онтологию
            publication_manager.save_ontology()
            return jsonify({'success': True, 'message': 'Источник добавлен'})
        else:
            return jsonify({'success': False, 'error': 'Не удалось добавить источник'}), 400
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sources/collect/<language>')
def api_collect_sources(language):
    """API для автоматического сбора источников"""
    try:
        from source_collector import SourceCollector
        
        collector = SourceCollector()
        sources = collector.collect_all_sources(language)
        
        return jsonify({
            'success': True,
            'language': language,
            'sources': sources
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tags')
def api_get_all_tags():
    """API для получения всех тегов из публикаций"""
    try:
        if not publication_manager:
            return jsonify({'success': False, 'error': 'Менеджер публикаций не инициализирован'}), 500
        
        # Получаем все публикации
        all_languages = search_engine.get_all_languages()
        if not all_languages:
            all_languages = ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp']
        
        tags_count = {}
        categories = set()
        
        for lang in all_languages:
            try:
                publications = publication_manager.get_publications_for_language(lang)
                for pub in publications:
                    # Извлекаем теги из keywords
                    keywords = pub.get('keywords', '')
                    if keywords:
                        tag_list = [tag.strip().lower() for tag in keywords.split(',') if tag.strip()]
                        for tag in tag_list:
                            tags_count[tag] = tags_count.get(tag, 0) + 1
            except:
                continue
        
        # Сортируем по популярности
        sorted_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)
        
        return jsonify({
            'success': True,
            'tags': [{'name': tag, 'count': count} for tag, count in sorted_tags],
            'total': len(sorted_tags)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tags/language/<name>')
def api_get_tags_for_language(name):
    """API для получения тегов для конкретного языка"""
    try:
        if not publication_manager:
            return jsonify({'success': False, 'error': 'Менеджер публикаций не инициализирован'}), 500
        
        publications = publication_manager.get_publications_for_language(name)
        tags_count = {}
        
        for pub in publications:
            keywords = pub.get('keywords', '')
            if keywords:
                tag_list = [tag.strip().lower() for tag in keywords.split(',') if tag.strip()]
                for tag in tag_list:
                    tags_count[tag] = tags_count.get(tag, 0) + 1
        
        sorted_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)
        
        return jsonify({
            'success': True,
            'language': name,
            'tags': [{'name': tag, 'count': count} for tag, count in sorted_tags],
            'total': len(sorted_tags)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Создаем шаблоны только при первом запуске (если отсутствуют файлы).
    # Иначе не перезаписываем пользовательские изменения в templates/.
    if not os.path.exists('templates/search.html'):
        create_templates()
    else:
        print("ℹ️ Шаблоны уже существуют, перезапись пропущена")
    
    print("🚀 Запуск веб-дашборда...")
    print("📊 Доступно по адресу: http://localhost:5000")
    print("📈 Дашборд: http://localhost:5000/dashboard")
    print("🌐 Языки: http://localhost:5000/languages")
    
    app.run(debug=True, host='0.0.0.0', port=5000)