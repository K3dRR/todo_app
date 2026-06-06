class Task:  # Task - одна задача
    def __init__(self, task_id, title, priority, completed=False):
        self.id = task_id  # уник. номер задачи
        self.title = title  # название
        self.priority = priority  # приоритет
        self.completed = completed  # завершенность

    def to_dict(self):  # для сохранения в json
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):  # задача из json
        return Task(
            task_id=data["id"],
            title=data["title"],
            priority=data["priority"],
            completed=data["completed"]
        )

    def __str__(self):
        status = "+" if self.completed else "-"
        return f"[{status}] {self.title} ({self.priority})"

class TaskManager:  # Управление списком задач
    def __init__(self):
        self.tasks = []  # список всех задач
        self.next_id = 1  # id след. задачи

    def add_task(self, title, priority):  # добавить задачу
        task = Task(self.next_id, title, priority)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def remove_task(self, task_id):  # удалить задачу
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def toggle_completed(self, task_id):  # переключение статуса задачи
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                return True
        return False

    def get_all_tasks(self):  # Все задачи
        return self.tasks

    def get_task_by_id(self, task_id):  # Найти задачу
        for task in self.tasks:
            if task.id == task_id:
                return task
            return None
