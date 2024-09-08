import json
import os
import requests
from tkinter import Tk, Label, Text, Scrollbar, Frame, PhotoImage, Canvas
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser
import sys

def load_json(folder_name):
    # Путь к JSON-файлу
    json_file_path = os.path.join('Data', folder_name, 'article_data.json')
    if not os.path.exists(json_file_path):
        print(f"Ошибка: Файл не найден - {json_file_path}")
        sys.exit(1)
    
    # Загрузка данных из JSON-файла
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def load_image(url):
    response = requests.get(url)
    img_data = Image.open(BytesIO(response.content))
    img_data = img_data.resize((500, 300), Image.LANCZOS)  # изменяем размер с использованием LANCZOS
    return ImageTk.PhotoImage(img_data)

def open_url(url):
    webbrowser.open(url)

def create_gui(data):
    # Создание корневого окна
    root = Tk()
    root.title("Статья")

    # Настройка Scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side='right', fill='y')

    # Настройка Canvas и Frame для текста статьи
    canvas = Canvas(root, yscrollcommand=scrollbar.set)
    frame = Frame(canvas)

    # Настройка скролла
    scrollbar.config(command=canvas.yview)
    canvas.pack(side='left', fill='both', expand=True)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    # Заголовок статьи
    title_label = Label(frame, text="Статья", font=("Arial", 14, "bold"), wraplength=600)
    title_label.pack(pady=10)

    # Изображение статьи
    image_url = data['article']['image_url']
    article_image = load_image(image_url)
    image_label = Label(frame, image=article_image)
    image_label.pack(pady=10)

    # Текст статьи
    article_text = data['article']['text']
    text_box = Text(frame, wrap='word', height=10, width=60)
    text_box.insert('1.0', article_text)
    text_box.configure(state='disabled')  # делает текст недоступным для редактирования
    text_box.pack(pady=10)

    # Рекомендуемые статьи
    related_label = Label(frame, text="Рекомендуемые статьи:", font=("Arial", 12, "bold"))
    related_label.pack(pady=10)

    for post in data['article']['related_posts']:
        post_msg = f"{post['title']} - Автор: {post['author']} ({post['date']})"
        post_link = Label(frame, text=post_msg, fg="blue", cursor="hand2")
        post_link.pack(anchor='w')
        post_link.bind("<Button-1>", lambda e, url=post['link']: open_url(url))

    # Обновляем размер окна
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))

    # Запуск главного цикла
    root.mainloop()

def main():
    # Проверка наличия аргумента командной строки
    if len(sys.argv) < 2:
        print("Ошибка: Необходимо указать название папки в Data в качестве аргумента.")
        return

    # Название папки из аргумента командной строки
    folder_name = sys.argv[1]

    # Загрузка JSON и создание GUI
    data = load_json(folder_name)
    create_gui(data)

if __name__ == "__main__":
    main()