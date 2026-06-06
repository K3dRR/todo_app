# Сохранение задач

import json
import os
from models import Task

class Storage:  # Сохранение и загрузка
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def save(self, tasks):  # Сохранить
        tasks_data = [task.to_dict() for task in tasks]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)

        print(f"Сохранено {len(tasks)} задач в файл {self.filename}")

    def load(self, task_manager):  # Загрузка
        if not os.path.exists(self.filename):
            print(f"Файл {self.filename} не найден")
            return

        with open(self.filename, "r", encoding="utf-8") as f:
            tasks_data = json.load(f)

        for data in tasks_data:
            task = Task.from_dict(data)
            task_manager.tasks.append(task)

            if task.id >= task_manager.next_id:
                task_manager.next_id = task.id + 1

        print(f"Загружено {len(tasks_data)} задач из файла {self.filename}")