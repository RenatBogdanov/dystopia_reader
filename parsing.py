import requests
from bs4 import BeautifulSoup
import os
import json
import sys

def main():
    # Проверка наличия аргумента командной строки
    if len(sys.argv) < 2:
        print("Ошибка: Необходимо указать URL статьи в качестве аргумента.")
        return

    # URL веб-страницы (из аргумента командной строки)
    url = sys.argv[1] 

    # Создание папки Data, если её нет
    data_folder = "Data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Получение имени папки для статьи из URL
    folder_name = os.path.join(data_folder, url.split('/')[-1])  # извлечение последнего сегмента URL и добавление к папке Data
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)  # создание папки для статьи, если её нет

    # Получение HTML-кода страницы
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 1. Извлечение основного текста статьи
    main_content = soup.find('div', class_='single_content')
    article_paragraphs = main_content.find_all('p')
    article_text = ' '.join([p.text.strip() for p in article_paragraphs if p.text.strip()])

    # 2. Извлечение изображения статьи
    image_div = soup.find('div', class_='post__image')
    article_image_url = image_div.find('img')['src'] if image_div and image_div.find('img') else None

    # Загрузка и сохранение основного изображения
    if article_image_url:
        article_image_response = requests.get(article_image_url)
        if article_image_response.status_code == 200:
            with open(os.path.join(folder_name, 'article_image.jpg'), 'wb') as img_file:
                img_file.write(article_image_response.content)

    # 3. Извлечение дополнительных записей
    related_posts = []
    related_section = soup.find('div', class_='poxojie_zapisi')

    if related_section:
        post_items = related_section.find_all('div', class_='post__item')
        for post in post_items:
            post_title = post.find('div', class_='post__title').text.strip() if post.find('div', class_='post__title') else 'Заголовок не найден'
            post_author_link = post.find('div', class_='post__author').find('a')
            post_author = post_author_link.text.strip() if post_author_link else 'Автор не найден'
            post_date = post.find('div', class_='post__category-date').text.strip() if post.find('div', class_='post__category-date') else 'Дата не найдена'
            post_image_url = post.find('img')['src'] if post.find('img') else None
            post_link = post.find('a', class_='post__link')['href'] if post.find('a', class_='post__link') else 'Ссылка не найдена'

            # Загрузка и сохранение изображения для каждой похожей записи
            if post_image_url:
                post_image_response = requests.get(post_image_url)
                if post_image_response.status_code == 200:
                    image_filename = os.path.basename(post_image_url)
                    with open(os.path.join(folder_name, image_filename), 'wb') as img_file:
                        img_file.write(post_image_response.content)

            related_posts.append({
                'title': post_title,
                'author': post_author,
                'date': post_date,
                'image_url': post_image_url,
                'link': post_link
            })

    # 4. Сохранение данных в JSON
    data_to_save = {
        'article': {
            'text': article_text,
            'image_url': article_image_url,
            'related_posts': related_posts
        }
    }

    json_file_path = os.path.join(folder_name, 'article_data.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)

    # 5. Вывод результата в консоль
    print("Содержимое JSON:")
    print(json.dumps(data_to_save, ensure_ascii=False, indent=4))

    # Вывод результатов (опционально)
    print(f"Данные о статье сохранены в папке: {folder_name}")

if __name__ == "__main__":
    main()