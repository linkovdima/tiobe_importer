import json
import schedule
import time
from datetime import datetime
from pathlib import Path

from ontology_manager import OntologyManager
from tiobe_importer import TIOBEImporter
from config import LOG_PATH, UPDATE_SCHEDULE

class TIOBEUpdater:
    def __init__(self):
        self.om = OntologyManager()
        self.importer = TIOBEImporter(self.om)
        
        # Создаем папку для логов
        LOG_PATH.parent.mkdir(exist_ok=True)
    
    def run_update(self, use_demo_fallback=True):
        """Запуск одного обновления"""
        print("\n" + "="*50)
        print(f"🔄 ЗАПУСК ОБНОВЛЕНИЯ TIOBE - {datetime.now()}")
        print("="*50)
        
        try:
            # Получаем актуальные рейтинги
            rankings = self.importer.scrape_tiobe_ranking(use_demo_fallback)
            
            if not rankings:
                print("❌ Не удалось получить рейтинги")
                return False
            
            # Обновляем онтологию
            result = self.importer.update_ontology_with_rankings(rankings)
            
            # Сохраняем онтологию
            save_success = self.om.save_ontology()
            
            # Логируем результат
            self._log_update(result, save_success, rankings)
            
            # Выводим отчет
            self._print_report(result, rankings)
            
            return result['updated_count'] > 0
            
        except Exception as e:
            print(f"❌ Критическая ошибка при обновлении: {e}")
            self._log_error(e)
            return False
    
    def _print_report(self, result, rankings):
        """Печать отчета об обновлении"""
        print("\n📊 ОТЧЕТ ОБ ОБНОВЛЕНИИ:")
        print(f"   • Обработано записей: {result['total_rankings']}")
        print(f"   • Успешно обновлено: {result['updated_count']}")
        print(f"   • Ошибок обновления: {len(result['failed_updates'])}")
        
        if result['failed_updates']:
            print(f"   • Языки с ошибками: {', '.join(result['failed_updates'])}")
        
        # Топ-5 языков
        print(f"\n🏆 ТОП-5 ЯЗЫКОВ:")
        for i, lang in enumerate(rankings[:5], 1):
            print(f"   {i}. {lang['name']} - #{lang['rank']} ({lang['rating']})")
    
    def _log_update(self, result, save_success, rankings):
        """Логирование результатов обновления"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'success': save_success and result['updated_count'] > 0,
            'updated_count': result['updated_count'],
            'failed_count': len(result['failed_updates']),
            'failed_languages': result['failed_updates'],
            'top_language': rankings[0]['name'] if rankings else None,
            'total_rankings': len(rankings)
        }
        
        try:
            # Читаем существующие логи
            logs = []
            if LOG_PATH.exists():
                with open(LOG_PATH, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            logs.append(json.loads(line.strip()))
            
            # Добавляем новую запись
            logs.append(log_entry)
            
            # Сохраняем (оставляем последние 100 записей)
            with open(LOG_PATH, 'w', encoding='utf-8') as f:
                for entry in logs[-100:]:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                    
            print(f"💾 Лог сохранен: {LOG_PATH}")
            
        except Exception as e:
            print(f"⚠️ Ошибка сохранения лога: {e}")
    
    def _log_error(self, error):
        """Логирование ошибки"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'error',
            'message': str(error)
        }
        
        try:
            with open(LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps(error_entry, ensure_ascii=False) + '\n')
        except:
            pass
    
    def start_scheduled_updates(self):
        """Запуск обновлений по расписанию"""
        print("⏰ Запуск планировщика обновлений...")
        
        # Ежедневное обновление (для тестирования)
        schedule.every().day.at(UPDATE_SCHEDULE['daily']).do(self.run_update)
        
        # Ежемесячное обновление (основное)
        # schedule.every().month.do(self.run_update)
        
        print(f"📅 Расписание:")
        print(f"   • Ежедневно в {UPDATE_SCHEDULE['daily']}")
        # print(f"   • Ежемесячно 1-го числа в {UPDATE_SCHEDULE['monthly'].split()[1]}")
        
        print("\n🔄 Планировщик запущен. Для остановки: Ctrl+C")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Проверка каждую минуту
        except KeyboardInterrupt:
            print("\n⏹️ Планировщик остановлен")

def main():
    """Основная функция"""
    updater = TIOBEUpdater()
    
    print("🚀 СИСТЕМА АВТОМАТИЧЕСКОГО ОБНОВЛЕНИЯ TIOBE")
    print("="*50)
    
    # Проверяем аргументы командной строки
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "update":
            # Однократное обновление
            updater.run_update()
        elif sys.argv[1] == "schedule":
            # Запуск по расписанию
            updater.start_scheduled_updates()
        elif sys.argv[1] == "test":
            # Тестовый режим (только демо-данные)
            print("🧪 ТЕСТОВЫЙ РЕЖИМ (демо-данные)")
            updater.run_update(use_demo_fallback=True)
    else:
        # Интерактивный режим
        print("Выберите режим:")
        print("1. Однократное обновление")
        print("2. Запуск по расписанию")
        print("3. Тестовый режим (демо-данные)")
        
        choice = input("Введите номер (1-3): ").strip()
        
        if choice == "1":
            updater.run_update()
        elif choice == "2":
            updater.start_scheduled_updates()
        elif choice == "3":
            updater.run_update(use_demo_fallback=True)
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    main()