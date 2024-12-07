import json
import csv
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks_file = "tasks.json"
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из JSON-файла."""
        try:
            with open(self.tasks_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        """Сохранение задач в JSON-файл."""
        with open(self.tasks_file, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        """Добавление новой задачи."""
        title = input("Введите название задачи: ").strip()
        if not title:
            print("Название задачи обязательно.")
            return

        description = input("Введите описание задачи: ").strip()
        priority = input("Введите приоритет задачи (Высокий, Средний, Низкий): ").strip()
        if priority not in {"Высокий", "Средний", "Низкий"}:
            print("Недопустимый приоритет. Используйте 'Высокий', 'Средний' или 'Низкий'.")
            return

        due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ").strip()
        try:
            datetime.strptime(due_date, "%d-%m-%Y")  # Проверка формата даты
        except ValueError:
            print("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
            return

        task_id = len(self.tasks) + 1
        self.tasks.append({
            "id": task_id,
            "title": title,
            "description": description,
            "done": False,
            "priority": priority,
            "due_date": due_date
        })
        self.save_tasks()
        print("Задача добавлена.")

    def list_tasks(self, filter_by=None):
        """Просмотр списка задач с возможностью фильтрации."""
        tasks = self.tasks
        if filter_by == "status":
            status = input("Введите статус (выполнено/не выполнено): ").strip().lower()
            if status == "выполнено":
                tasks = [task for task in tasks if task["done"]]
            elif status == "не выполнено":
                tasks = [task for task in tasks if not task["done"]]
            else:
                print("Неверный статус.")
                return
        elif filter_by == "priority":
            priority = input("Введите приоритет (Высокий, Средний, Низкий): ").strip()
            tasks = [task for task in tasks if task["priority"] == priority]
        elif filter_by == "due_date":
            due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ").strip()
            tasks = [task for task in tasks if task["due_date"] == due_date]

        if not tasks:
            print("Нет задач, соответствующих критериям.")
            return

        for task in tasks:
            status = "Выполнено" if task["done"] else "Не выполнено"
            print(f"[{task['id']}] {task['title']} - {status}, Приоритет: {task['priority']}, Срок: {task['due_date']}")

    def mark_task_done(self):
        """Отметка задачи как выполненной."""
        try:
            task_id = int(input("Введите ID задачи: "))
            task = next(task for task in self.tasks if task["id"] == task_id)
            task["done"] = True
            self.save_tasks()
            print("Задача отмечена как выполненная.")
        except StopIteration:
            print("Задача с таким ID не найдена.")
        except ValueError:
            print("ID должен быть числом.")

    def edit_task(self):
        """Редактирование существующей задачи."""
        try:
            task_id = int(input("Введите ID задачи для редактирования: "))
            task = next(task for task in self.tasks if task["id"] == task_id)

            print(f"Редактирование задачи: {task['title']}")
            new_title = input("Новое название (оставьте пустым для сохранения текущего): ").strip()
            if new_title:
                task["title"] = new_title

            new_description = input("Новое описание (оставьте пустым для сохранения текущего): ").strip()
            if new_description:
                task["description"] = new_description

            new_priority = input("Новый приоритет (Высокий, Средний, Низкий): ").strip()
            if new_priority in {"Высокий", "Средний", "Низкий"}:
                task["priority"] = new_priority

            new_due_date = input("Новый срок выполнения (ДД-ММ-ГГГГ): ").strip()
            if new_due_date:
                try:
                    datetime.strptime(new_due_date, "%d-%m-%Y")  # Проверка формата даты
                    task["due_date"] = new_due_date
                except ValueError:
                    print("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")

            self.save_tasks()
            print("Задача обновлена.")
        except StopIteration:
            print("Задача с таким ID не найдена.")
        except ValueError:
            print("ID должен быть числом.")

    def delete_task(self):
        """Удаление задачи."""
        try:
            task_id = int(input("Введите ID задачи для удаления: "))
            self.tasks = [task for task in self.tasks if task["id"] != task_id]
            self.save_tasks()
            print("Задача удалена.")
        except ValueError:
            print("ID должен быть числом.")

    def import_tasks(self):
        """Импорт задач из CSV."""
        filename = input("Введите имя файла CSV для импорта: ").strip()
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tasks.append({
                        "id": len(self.tasks) + 1,
                        "title": row["title"],
                        "description": row["description"],
                        "done": row["done"].lower() == "true",
                        "priority": row["priority"],
                        "due_date": row["due_date"]
                    })
                self.save_tasks()
                print("Задачи импортированы.")
        except FileNotFoundError:
            print("Файл не найден.")

    def export_tasks(self):
        """Экспорт задач в CSV."""
        filename = input("Введите имя файла CSV для экспорта: ").strip()
        with open(filename, "w", newline="") as file:
            fieldnames = ["title", "description", "done", "priority", "due_date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({
                    "title": task["title"],
                    "description": task["description"],
                    "done": task["done"],
                    "priority": task["priority"],
                    "due_date": task["due_date"]
                })
            print("Задачи экспортированы.")

    def manage_tasks(self):
        """Основное меню управления задачами."""
        while True:
            print("\nУправление задачами:")
            print("1. Добавить задачу")
            print("2. Просмотреть задачи")
            print("3. Отметить задачу выполненной")
            print("4. Редактировать задачу")
            print("5. Удалить задачу")
            print("6. Импорт задач из CSV")
            print("7. Экспорт задач в CSV")
            print("8. Фильтровать задачи")
            print("9. Назад")

            choice = input("Введите номер действия: ")

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                self.mark_task_done()
            elif choice == '4':
                self.edit_task()
            elif choice == '5':
                self.delete_task()
            elif choice == '6':
                self.import_tasks()
            elif choice == '7':
                self.export_tasks()
            elif choice == '8':
                filter_by = input("Фильтровать по (status/priority/due_date): ").strip()
                self.list_tasks(filter_by)
            elif choice == '9':
                break
            else:
                print("Неверный выбор.")
