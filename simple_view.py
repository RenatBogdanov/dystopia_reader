import json
import os
import requests
from tkinter import Tk, Label, Text, Scrollbar, Frame, Listbox, SINGLE, Canvas
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser
import sys
import subprocess

def load_json(folder_name):
    json_file_path = os.path.join('Data', folder_name, 'article_data.json')
    if not os.path.exists(json_file_path):
        print(f"Ошибка: Файл не найден - {json_file_path}")
        return None  # Возвращаем None, чтобы избежать дальнейших ошибок

    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def load_image(url):
    response = requests.get(url)
    img_data = Image.open(BytesIO(response.content))
    img_data = img_data.resize((500, 300), Image.LANCZOS)
    return ImageTk.PhotoImage(img_data)

def open_url(url):
    webbrowser.open(url)

def create_menu(root, folder_names):
    menu_frame = Frame(root)
    menu_frame.pack(side='left', fill='y')

    listbox = Listbox(menu_frame, height=20, selectmode=SINGLE)
    listbox.pack(padx=10, pady=10)

    for folder in folder_names:
        listbox.insert('end', folder)

    def on_select(event):
        selected_folder = listbox.get(listbox.curselection())
        # Запускаем снова скрипт с выбранной папкой
        subprocess.run([sys.executable, __file__, selected_folder])

    listbox.bind('<<ListboxSelect>>', on_select)

def create_gui(data=None, folder_names=None):
    root = Tk()
    root.title("Статья")

    create_menu(root, folder_names)  # Создаем боковое меню

    if data is not None:  # Проверка, нужно ли отображать данные статьи
        scrollbar = Scrollbar(root)
        scrollbar.pack(side='right', fill='y')

        canvas = Canvas(root, yscrollcommand=scrollbar.set)
        frame = Frame(canvas)

        scrollbar.config(command=canvas.yview)
        canvas.pack(side='right', fill='both', expand=True)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        title_label = Label(frame, text="Статья", font=("Arial", 14, "bold"), wraplength=600)
        title_label.pack(pady=10)

        image_url = data['article']['image_url']
        article_image = load_image(image_url)
        image_label = Label(frame, image=article_image)
        image_label.pack(pady=10)

        article_text = data['article']['text']
        text_box = Text(frame, wrap='word', height=10, width=60)
        text_box.insert('1.0', article_text)
        text_box.configure(state='disabled')
        text_box.pack(pady=10)

        related_label = Label(frame, text="Рекомендуемые статьи:", font=("Arial", 12, "bold"))
        related_label.pack(pady=10)

        for post in data['article']['related_posts']:
            post_msg = f"{post['title']} - Автор: {post['author']} ({post['date']})"
            post_link = Label(frame, text=post_msg, fg="blue", cursor="hand2")
            post_link.pack(anchor='w')
            post_link.bind("<Button-1>", lambda e, url=post['link']: open_url(url))

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

    root.mainloop()

def main():
    folder_names = [d for d in os.listdir('Data') if os.path.isdir(os.path.join('Data', d))]
    
    if len(sys.argv) < 2:
        create_gui(folder_names=folder_names)
        return

    folder_name = sys.argv[1]
    data = load_json(folder_name)
    
    # Если данные не были загружены, показываем только меню
    if data is None:
        create_gui(folder_names=folder_names)
    else:
        create_gui(data, folder_names)

if __name__ == "__main__":
    main()