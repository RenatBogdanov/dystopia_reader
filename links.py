import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import re

base_url = 'https://dystopia.me/'  # Основной URL
visited_links = {}  # Словарь для хранения URL и названий страниц

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def clean_title(title):
    cleaned_title = re.sub(r' — «Дистопия»', '', title)  # Удаляет " — Дистопия"
    cleaned_title = re.sub(r' — автор', '', cleaned_title)  # Удаляет " — автор"
    cleaned_title = re.sub(r' — Автор', '', cleaned_title)  # Удаляет " — автор"
    return cleaned_title.strip()

def crawl(url):
    if url not in visited_links:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else 'Без заголовка'
            cleaned_title = clean_title(title)

            visited_links[url] = cleaned_title
            print(f"Найдена новая страница: {url} ({cleaned_title})")
            print(f"Количество найденных страниц: {len(visited_links)}n")

            #time.sleep(1)

            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)

                if is_valid(full_url) and base_url in full_url:
                    crawl(full_url)
        except requests.RequestException as e:
            print(f"Ошибка: не удалось загрузить {url} - {e}")

if __name__ == "__main__":
    crawl(base_url)

    with open('links.json', 'w', encoding='utf-8') as json_file:
        json.dump(visited_links, json_file, ensure_ascii=False, indent=4)

    print("Ссылки и названия страниц успешно сохранены в 'links.json'.")