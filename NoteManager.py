import json
import csv
from datetime import datetime

class NoteManager:
    def __init__(self):
        self.notes_file = "notes.json"
        self.notes = self.load_notes()

    def load_notes(self):
        """Загрузка заметок из JSON-файла."""
        try:
            with open(self.notes_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_notes(self):
        """Сохранение заметок в JSON-файл."""
        with open(self.notes_file, "w") as file:
            json.dump(self.notes, file, indent=4)

    def add_note(self):
        """Создание новой заметки."""
        title = input("Введите заголовок заметки: ").strip()
        if not title:
            print("Заголовок заметки обязателен.")
            return

        content = input("Введите содержимое заметки: ").strip()
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        note_id = len(self.notes) + 1

        self.notes.append({
            "id": note_id,
            "title": title,
            "content": content,
            "timestamp": timestamp
        })
        self.save_notes()
        print("Заметка добавлена.")

    def list_notes(self):
        """Просмотр списка заметок."""
        if not self.notes:
            print("Список заметок пуст.")
            return

        for note in self.notes:
            print(f"[{note['id']}] {note['title']} - Последнее обновление: {note['timestamp']}")

    def view_note_details(self):
        """Просмотр подробностей заметки."""
        try:
            note_id = int(input("Введите ID заметки: "))
            note = next(note for note in self.notes if note["id"] == note_id)
            print(f"\nЗаголовок: {note['title']}")
            print(f"Содержимое:\n{note['content']}")
            print(f"Последнее обновление: {note['timestamp']}")
        except StopIteration:
            print("Заметка с таким ID не найдена.")
        except ValueError:
            print("ID должен быть числом.")

    def edit_note(self):
        """Редактирование существующей заметки."""
        try:
            note_id = int(input("Введите ID заметки для редактирования: "))
            note = next(note for note in self.notes if note["id"] == note_id)

            print(f"Редактирование заметки: {note['title']}")
            new_title = input("Введите новый заголовок (оставьте пустым для сохранения текущего): ").strip()
            if new_title:
                note["title"] = new_title

            new_content = input("Введите новое содержимое (оставьте пустым для сохранения текущего): ").strip()
            if new_content:
                note["content"] = new_content

            note["timestamp"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            print("Заметка обновлена.")
        except StopIteration:
            print("Заметка с таким ID не найдена.")
        except ValueError:
            print("ID должен быть числом.")

    def delete_note(self):
        """Удаление заметки."""
        try:
            note_id = int(input("Введите ID заметки для удаления: "))
            self.notes = [note for note in self.notes if note["id"] != note_id]
            self.save_notes()
            print("Заметка удалена.")
        except ValueError:
            print("ID должен быть числом.")

    def import_notes(self):
        """Импорт заметок из CSV."""
        filename = input("Введите имя файла CSV для импорта: ").strip()
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.notes.append({
                        "id": len(self.notes) + 1,
                        "title": row["title"],
                        "content": row["content"],
                        "timestamp": row["timestamp"]
                    })
                self.save_notes()
                print("Заметки импортированы.")
        except FileNotFoundError:
            print("Файл не найден.")
        except KeyError:
            print("Некорректный формат CSV-файла.")

    def export_notes(self):
        """Экспорт заметок в CSV."""
        filename = input("Введите имя файла CSV для экспорта: ").strip()
        with open(filename, "w", newline="") as file:
            fieldnames = ["title", "content", "timestamp"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for note in self.notes:
                writer.writerow({
                    "title": note["title"],
                    "content": note["content"],
                    "timestamp": note["timestamp"]
                })
            print("Заметки экспортированы.")

    def manage_notes(self):
        """Основное меню управления заметками."""
        while True:
            print("\nУправление заметками:")
            print("1. Создать заметку")
            print("2. Просмотреть список заметок")
            print("3. Просмотреть подробности заметки")
            print("4. Редактировать заметку")
            print("5. Удалить заметку")
            print("6. Импорт заметок из CSV")
            print("7. Экспорт заметок в CSV")
            print("8. Назад")

            choice = input("Введите номер действия: ")

            if choice == '1':
                self.add_note()
            elif choice == '2':
                self.list_notes()
            elif choice == '3':
                self.view_note_details()
            elif choice == '4':
                self.edit_note()
            elif choice == '5':
                self.delete_note()
            elif choice == '6':
                self.import_notes()
            elif choice == '7':
                self.export_notes()
            elif choice == '8':
                break
            else:
                print("Неверный выбор.")
