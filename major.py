import subprocess
import json

# Загрузить ссылки из links.json
with open('links.json', 'r', encoding='utf-8') as f:
    links = json.load(f)

# Обработка первых 10 ссылок
for i, link in enumerate(links):
    if i >= 10:
        break
    subprocess.run(['python', 'parsing.py', link])
