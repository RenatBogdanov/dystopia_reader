import json
import subprocess
from tqdm import tqdm  # Импортируем tqdm для индикатора прогресса

def main():
    # Чтение данных из links.json
    with open('links.json', 'r', encoding='utf-8') as f:
        links = json.load(f)

    # Перебираем все ссылки с индикатором прогресса
    for url in tqdm(links.keys(), desc="Обработка ссылок", unit="ссылка"):
        print(f"\n Запуск parsing.py для {url}")
        # Запускаем parsing.py с аргументом-ссылкой
        subprocess.run(['python', 'parsing.py', url])  # Убедитесь, что путь к python доступен в системе

if __name__ == "__main__":  # Исправлено на __name__ и __main__
    main()
