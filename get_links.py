import json

# Загрузить ссылки из links.json
with open('links.json', 'r', encoding='utf-8') as f:  # Добавили encoding='utf-8'
    links = json.load(f)

# Вывести ссылки
for link in links:
    print(link)
