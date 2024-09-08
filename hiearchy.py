import json
import os

def create_hierarchy(data, root_dir):
    """Создает иерархию папок на основе JSON-данных без использования index.html."""
    for url, title in data.items():
        path_parts = url.strip('/').split('/')
        current_dir = root_dir
        for part in path_parts[1:]:
            current_dir = os.path.join(current_dir, part)
            os.makedirs(current_dir, exist_ok=True)

# Загрузка JSON-данных
with open('links.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Создание иерархии
create_hierarchy(data, 'output')  # Укажите желаемый корневой каталог

print("Иерархия папок создана!")
