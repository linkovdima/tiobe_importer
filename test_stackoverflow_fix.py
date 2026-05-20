# test_stackoverflow_fix.py
import requests
import json

def test_stackoverflow_api():
    """Тестирование Stack Overflow API с разными методами"""
    print("🧪 ТЕСТ STACK OVERFLOW API")
    print("=" * 40)
    
    tags_to_test = ['python', 'java', 'c%23']
    
    for tag in tags_to_test:
        print(f"\n🔍 Тестируем тег: {tag}")
        
        # Метод 1: Стандартный запрос
        url1 = f"https://api.stackexchange.com/2.3/tags/{tag}/info?site=stackoverflow"
        print(f"📡 Запрос 1: {url1}")
        
        try:
            response1 = requests.get(url1, timeout=10)
            print(f"   Статус: {response1.status_code}")
            
            if response1.status_code == 200:
                data1 = response1.json()
                print(f"   Ключи ответа: {list(data1.keys())}")
                
                if 'items' in data1 and data1['items']:
                    print(f"   ✅ Данные: {data1['items'][0].get('count', 'N/A')} вопросов")
                else:
                    print(f"   ❌ Нет items в ответе")
                    print(f"   Полный ответ: {json.dumps(data1, indent=2)[:500]}...")
            else:
                print(f"   ❌ Ошибка HTTP: {response1.status_code}")
                
        except Exception as e:
            print(f"   🚨 Исключение: {e}")
        
        # Метод 2: Упрощенный запрос
        url2 = f"https://api.stackexchange.com/2.3/tags?inname={tag}&site=stackoverflow"
        print(f"📡 Запрос 2: {url2}")
        
        try:
            response2 = requests.get(url2, timeout=10)
            print(f"   Статус: {response2.status_code}")
            
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"   Ключи ответа: {list(data2.keys())}")
                
                if 'items' in data2 and data2['items']:
                    print(f"   ✅ Данные: {data2['items'][0].get('count', 'N/A')} вопросов")
                else:
                    print(f"   ❌ Нет items в ответе")
            else:
                print(f"   ❌ Ошибка HTTP: {response2.status_code}")
                
        except Exception as e:
            print(f"   🚨 Исключение: {e}")
        
        print("⏳ Ждем 2 секунды...")
        import time
        time.sleep(2)

if __name__ == "__main__":
    test_stackoverflow_api()