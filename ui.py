import tkinter as tk
from tkinter import ttk, messagebox


class ToDoApp:
    def __init__(self, root, task_manager, storage):
        self.root = root
        self.task_manager = task_manager
        self.storage = storage
        self.selected_task_id = None
        self.canvas_window = None
        self.last_canvas_width = 0

        self.root.title("Мои задачи")
        self.root.geometry("650x500")
        self.root.minsize(650, 500)
        self.root.configure(bg='#e8eaf6')

        self.storage.load(self.task_manager)

        self.create_widgets()
        self.root.after(100, self.update_task_list)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#e8eaf6')
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_frame = tk.Frame(main_frame, bg='#e8eaf6')
        top_frame.pack(pady=15, padx=20, fill=tk.X)

        tk.Label(top_frame, text="Задача:", font=('Segoe UI', 10), bg='#e8eaf6', fg='#333333').grid(row=0, column=0, padx=5)
        self.title_entry = tk.Entry(top_frame, width=30, font=('Segoe UI', 10), relief='solid', bd=1)
        self.title_entry.grid(row=0, column=1, padx=5)
        self.title_entry.bind('<Return>', lambda event: self.add_task())

        tk.Label(top_frame, text="Приоритет:", font=('Segoe UI', 10), bg='#e8eaf6', fg='#333333').grid(row=0, column=2, padx=5)
        self.priority_combo = ttk.Combobox(top_frame, values=["Высокий", "Средний", "Низкий"], width=10, state="readonly")
        self.priority_combo.set("Средний")
        self.priority_combo.grid(row=0, column=3, padx=5)

        self.add_btn = tk.Button(top_frame, text="➕ Добавить", command=self.add_task, bg='#5C6BC0', fg='white',
                                 font=('Segoe UI', 10), relief='flat', padx=15, cursor='hand2')
        self.add_btn.grid(row=0, column=4, padx=10)

        top_frame.grid_columnconfigure(5, weight=1)

        list_frame = tk.Frame(main_frame, bg='#e8eaf6')
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        tk.Label(list_frame, text="Список задач:", font=('Segoe UI', 11, 'bold'), bg='#e8eaf6', fg='#333333',
                 anchor='w').pack(fill=tk.X, pady=(0, 5))

        list_container = tk.Frame(list_frame, bg='white')
        list_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(list_container, bg='white', highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        stats_frame = tk.Frame(main_frame, bg='#e8eaf6')
        stats_frame.pack(pady=10, padx=20, fill=tk.X)

        self.stats_label = tk.Label(stats_frame, text="", font=('Segoe UI', 10), bg='#e8eaf6', fg='#5C6BC0')
        self.stats_label.pack(side=tk.LEFT)

        bottom_frame = tk.Frame(main_frame, bg='#e8eaf6')
        bottom_frame.pack(pady=15, padx=20, fill=tk.X)

        self.complete_btn = tk.Button(bottom_frame, text="✅ Выполнить", command=self.complete_task,
                                      bg='#66BB6A', fg='white', font=('Segoe UI', 10), relief='flat', padx=15, cursor='hand2')
        self.complete_btn.pack(side=tk.LEFT, padx=5)

        self.edit_btn = tk.Button(bottom_frame, text="✏️ Редактировать", command=self.edit_task,
                                  bg='#FFA726', fg='white', font=('Segoe UI', 10), relief='flat', padx=15, cursor='hand2')
        self.edit_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(bottom_frame, text="🗑 Удалить", command=self.delete_task,
                                    bg='#EF5350', fg='white', font=('Segoe UI', 10), relief='flat', padx=15, cursor='hand2')
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(bottom_frame, text="💾 Сохранить", command=self.manual_save,
                                  bg='#78909C', fg='white', font=('Segoe UI', 10), relief='flat', padx=15, cursor='hand2')
        self.save_btn.pack(side=tk.RIGHT, padx=5)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        if event.width > 0 and self.canvas_window:
            self.canvas.itemconfig(self.canvas_window, width=event.width)


    def on_mousewheel(self, event):
        first, last = self.canvas.yview()

        if event.delta > 0 and first <= 0:
            return "break"

        if event.delta < 0 and last >= 1:
            return "break"

        self.canvas.yview_scroll(-int(event.delta / 120), "units")
        return "break"

    def get_priority_color(self, priority):
        colors = {"Высокий": "#FFEBEE", "Средний": "#FFF8E1", "Низкий": "#E8F5E9"}
        return colors.get(priority, "white")

    def get_priority_border_color(self, priority):
        colors = {"Высокий": "#EF9A9A", "Средний": "#FFCC80", "Низкий": "#A5D6A7"}
        return colors.get(priority, "#E0E0E0")

    def get_priority_text_color(self, priority):
        colors = {"Высокий": "#C62828", "Средний": "#EF6C00", "Низкий": "#2E7D32"}
        return colors.get(priority, "#333333")

    def update_task_list(self):
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 100:
            self.root.after(100, self.update_task_list)
            return

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            empty_label = tk.Label(self.scrollable_frame, text="✨ Нет задач. Добавьте первую задачу!",
                                   font=('Segoe UI', 11, 'italic'), bg='white', fg='#BDBDBD', pady=20)
            empty_label.pack()
            self.update_stats()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return

        text_width = max(self.canvas.winfo_width() - 260,150)

        for task in tasks:
            priority_color = self.get_priority_color(task.priority)

            task_frame = tk.Frame(self.scrollable_frame, bg=priority_color, relief='solid', bd=1)
            task_frame.pack(fill=tk.X, padx=5, pady=3)
            task_frame.task_id = task.id

            if self.selected_task_id == task.id:
                task_frame.config(relief='solid', bd=2,
                                  highlightbackground=self.get_priority_border_color(task.priority),
                                  highlightthickness=2)
            else:
                task_frame.config(highlightthickness=0)

            left_frame = tk.Frame(task_frame, bg=priority_color)
            left_frame.pack(side=tk.LEFT, padx=(10, 5), pady=10)

            status_label = tk.Label(left_frame, text="✅" if task.completed else "◻", font=('Segoe UI', 12),
                                    bg=priority_color, fg='#4CAF50' if task.completed else '#9E9E9E', cursor='hand2')
            status_label.pack()
            status_label.bind('<Button-1>', lambda e, t=task: self.toggle_from_label(t))
            text_frame = tk.Frame(task_frame, bg=priority_color)
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)

            priority_label = tk.Label(
                task_frame,
                text=f"[{task.priority}]",
                width=10,
                anchor="e",
                font=('Segoe UI', 9, 'bold'),
                bg=priority_color,
                fg=self.get_priority_text_color(task.priority)
            )

            priority_label.pack(side=tk.RIGHT, padx=10, pady=10)

            font = ('Segoe UI', 10, 'overstrike' if task.completed else 'normal')

            title_label = tk.Label(
                text_frame,
                text=task.title,
                font=font,
                bg=priority_color,
                fg='#9E9E9E' if task.completed else '#333333',
                anchor='w',
                justify='left',
                wraplength=text_width
            )
            title_label.pack(fill=tk.X)

            for w in (task_frame, left_frame, text_frame, title_label, priority_label):
                w.bind('<Button-1>', lambda e, tid=task.id: self.select_task(tid))

        self.update_stats()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def select_task(self, task_id):
        if self.selected_task_id == task_id:
            return
        self.selected_task_id = task_id
        for frame in self.scrollable_frame.winfo_children():
            if hasattr(frame, 'task_id'):
                if frame.task_id == task_id:
                    for t in self.task_manager.get_all_tasks():
                        if t.id == task_id:
                            priority = t.priority
                            break
                    frame.config(relief='solid', bd=2,
                                 highlightbackground=self.get_priority_border_color(priority),
                                 highlightthickness=2)
                else:
                    frame.config(relief='solid', bd=1, highlightthickness=0)

    def toggle_from_label(self, task):
        self.task_manager.toggle_completed(task.id)
        self.update_task_list()

    def update_stats(self):
        tasks = self.task_manager.get_all_tasks()
        total = len(tasks)
        completed = sum(1 for t in tasks if t.completed)
        remaining = total - completed
        self.stats_label.config(text=f"📊 Всего: {total} | ✅ Выполнено: {completed} | ⏳ Осталось: {remaining}")

    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Внимание", "Введите название задачи!")
            return
        priority = self.priority_combo.get()
        self.task_manager.add_task(title, priority)
        self.update_task_list()
        self.title_entry.delete(0, tk.END)
        self.priority_combo.set("Средний")

    def complete_task(self):
        if self.selected_task_id is None:
            messagebox.showinfo("Подсказка", "Нажмите на задачу в списке, чтобы выбрать её")
            return
        self.task_manager.toggle_completed(self.selected_task_id)
        self.update_task_list()

    def edit_task(self):
        if self.selected_task_id is None:
            messagebox.showinfo("Подсказка", "Нажмите на задачу в списке, чтобы выбрать её")
            return
        task = None
        for t in self.task_manager.get_all_tasks():
            if t.id == self.selected_task_id:
                task = t
                break
        if not task:
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактирование задачи")
        edit_window.geometry("400x250")
        edit_window.resizable(False, False)
        edit_window.configure(bg='#e8eaf6')
        edit_window.transient(self.root)
        edit_window.grab_set()

        tk.Label(edit_window, text="✏️ Редактировать задачу", font=('Segoe UI', 14, 'bold'),
                 bg='#e8eaf6', fg='#333333').pack(pady=15)

        tk.Label(edit_window, text="Название:", font=('Segoe UI', 10), bg='#e8eaf6', fg='#333333').pack(anchor='w', padx=30)
        title_entry = tk.Entry(edit_window, width=40, font=('Segoe UI', 10))
        title_entry.insert(0, task.title)
        title_entry.pack(pady=5, padx=30)

        tk.Label(edit_window, text="Приоритет:", font=('Segoe UI', 10), bg='#e8eaf6', fg='#333333').pack(anchor='w', padx=30, pady=(10,0))
        priority_combo = ttk.Combobox(edit_window, values=["Высокий", "Средний", "Низкий"], state="readonly", width=15)
        priority_combo.set(task.priority)
        priority_combo.pack(pady=5, padx=30)

        btn_frame = tk.Frame(edit_window, bg='#e8eaf6')
        btn_frame.pack(pady=20)

        def save_changes():
            new_title = title_entry.get().strip()
            if new_title:
                task.title = new_title
                task.priority = priority_combo.get()
                self.update_task_list()
                edit_window.destroy()
            else:
                messagebox.showwarning("Внимание", "Название не может быть пустым!")

        tk.Button(btn_frame, text="💾 Сохранить", command=save_changes,
                  bg='#5C6BC0', fg='white', font=('Segoe UI', 10), relief='flat', padx=15, cursor='hand2').pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Отмена", command=edit_window.destroy,
                  bg='#78909C', fg='white', font=('Segoe UI', 10), relief='flat', padx=15, cursor='hand2').pack(side=tk.LEFT, padx=5)

    def delete_task(self):
        if self.selected_task_id is None:
            messagebox.showinfo("Подсказка", "Нажмите на задачу в списке, чтобы выбрать её")
            return
        for task in self.task_manager.get_all_tasks():
            if task.id == self.selected_task_id:
                self.task_manager.remove_task(self.selected_task_id)
                self.selected_task_id = None
                self.update_task_list()
                break

    def manual_save(self):
        self.storage.save(self.task_manager.get_all_tasks())

    def on_closing(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.storage.save(self.task_manager.get_all_tasks())
        self.root.destroy()