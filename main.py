import tkinter as tk
from models import TaskManager
from storage import Storage
from ui import ToDoApp

def main():
    task_manager = TaskManager()
    storage = Storage()

    root = tk.Tk()
    app = ToDoApp(root, task_manager, storage)
    root.mainloop()

if __name__ == '__main__':
    main()

