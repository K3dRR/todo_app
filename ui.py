import tkinter as tk
from tkinter import ttk

class ToDoApp:
    def __init__(self, root, task_manager, storage):
        self.root = root
        self.task_manager = task_manager
        self.storage = storage

        self.root.title("Мои задачи")
        self.root.geometry("550x450")
        self.root.resizable(True, True)

        self.storage.load(self.task_manager)

        self.create_widgets()

        self.refresh_task_list()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(top_frame, text="Задача:").pack(side=tk.LEFT, padx=5)
        self.title_entry = tk.Entry(top_frame, width=30)
        self.title_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(top_frame, text="Приоритет:").pack(side=tk.LEFT, padx=5)
        self.priority_combo = ttk.Combobox(top_frame, values=["Высокий", "Средний", "Низкий"], width=10, state="readonly")
        self.priority_combo.set("Средний")
        self.priority_combo.pack(side=tk.LEFT, padx=5)

        self.add_btn = tk.Button(top_frame, text="+ Добавить", command=self.add_task)
        self.add_btn.pack(side=tk.LEFT, padx=10)

        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tasks_listbox = tk.Listbox(list_frame, height=15, yscrollcommand=scrollbar.set)
        self.tasks_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tasks_listbox.yview)


        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10, padx=10, fill=tk.X)

        self.complete_btn = tk.Button(bottom_frame, text="✅ Выполнить", command=self.complete_task)
        self.complete_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(bottom_frame, text="Удалить", command=self.delete_task)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

    def refresh_task_list(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.task_manager.get_all_tasks():
            status = "✅" if task.completed else "◻"
            display = f"[{status}] {task.title} ({task.priority})"
            self.tasks_listbox.insert(tk.END, display)

    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            return
        priority = self.priority_combo.get()
        self.task_manager.add_task(title, priority)
        self.refresh_task_list()

        self.title_entry.delete(0, tk.END)
        self.priority_combo.set("Средний")

    def complete_task(self):
        selection = self.tasks_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        task = self.task_manager.get_all_tasks()[index]
        self.task_manager.toggle_completed(task.id)
        self.refresh_task_list()

    def delete_task(self):
        selection = self.tasks_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        task = self.task_manager.get_all_tasks()[index]
        self.task_manager.remove_task(task.id)
        self.refresh_task_list()

    def on_closing(self):
        self.storage.save(self.task_manager.get_all_tasks())
        self.root.destroy()
