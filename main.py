import tkinter as tk
from models import TaskManager
from storage import Storage
from ui import ToDoApp
import sys, os

def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, path)

def main():
    task_manager = TaskManager()
    storage = Storage()

    root = tk.Tk()
    icon_path = resource_path("app.ico")
    try:
        root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")

    app = ToDoApp(root, task_manager, storage)
    root.mainloop()

if __name__ == '__main__':
    main()

