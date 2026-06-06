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
