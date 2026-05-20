# test_github_token.py
import requests
import sys

try:
    from github_config import GITHUB_TOKEN
except ImportError:
    print("❌ Файл github_config.py не найден")
    sys.exit(1)

def test_github_token():
    """Тестирование GitHub токена"""
    print("🧪 ТЕСТИРОВАНИЕ GITHUB TOKEN")
    print("=" * 40)
    
    if not GITHUB_TOKEN or GITHUB_TOKEN == "github_pat_xxxxxxxxxxxxxxxxxxxxxxxx":
        print("❌ Замените GITHUB_TOKEN на реальный токен в github_config.py")
        return False
    
    # Тестовый запрос
    url = "https://api.github.com/search/repositories?q=language:python&sort=stars&per_page=1"
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'User-Agent': 'ProgrammingLanguageOntology/1.0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            rate_limit_remaining = response.headers.get('X-RateLimit-Remaining', 'N/A')
            rate_limit_total = response.headers.get('X-RateLimit-Limit', 'N/A')
            
            print(f"✅ Токен работает!")
            print(f"📈 Rate limit: {rate_limit_remaining}/{rate_limit_total}")
            print(f"🐍 Python репозиториев: {data.get('total_count', 'N/A')}")
            return True
            
        elif response.status_code == 401:
            print("❌ Неверный токен - проверьте правильность токена")
            return False
        elif response.status_code == 403:
            print("❌ Rate limit превышен или недостаточно прав")
            print(f"Заголовки: {dict(response.headers)}")
            return False
        else:
            print(f"❌ Неизвестная ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"🚨 Исключение: {e}")
        return False

if __name__ == "__main__":
    test_github_token()