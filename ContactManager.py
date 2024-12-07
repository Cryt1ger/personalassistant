import json
import csv

class ContactManager:
    def __init__(self):
        self.contacts_file = "contacts.json"
        self.contacts = self.load_contacts()

    def load_contacts(self):
        """Загрузка контактов из JSON-файла."""
        try:
            with open(self.contacts_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_contacts(self):
        """Сохранение контактов в JSON-файл."""
        with open(self.contacts_file, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self):
        """Добавление нового контакта."""
        name = input("Введите имя контакта: ").strip()
        if not name:
            print("Имя контакта обязательно.")
            return

        phone = input("Введите номер телефона: ").strip()
        email = input("Введите адрес электронной почты: ").strip()
        contact_id = len(self.contacts) + 1

        self.contacts.append({
            "id": contact_id,
            "name": name,
            "phone": phone,
            "email": email
        })
        self.save_contacts()
        print("Контакт добавлен.")

    def search_contact(self):
        """Поиск контакта по имени или номеру телефона."""
        query = input("Введите имя или номер телефона для поиска: ").strip()
        results = [contact for contact in self.contacts if query.lower() in contact["name"].lower() or query in contact["phone"]]

        if not results:
            print("Контакты не найдены.")
        else:
            for contact in results:
                print(f"[{contact['id']}] {contact['name']} - Телефон: {contact['phone']}, Email: {contact['email']}")

    def edit_contact(self):
        """Редактирование контакта."""
        try:
            contact_id = int(input("Введите ID контакта для редактирования: "))
            contact = next(contact for contact in self.contacts if contact["id"] == contact_id)

            print(f"Редактирование контакта: {contact['name']}")
            new_name = input("Введите новое имя (оставьте пустым для сохранения текущего): ").strip()
            if new_name:
                contact["name"] = new_name

            new_phone = input("Введите новый номер телефона (оставьте пустым для сохранения текущего): ").strip()
            if new_phone:
                contact["phone"] = new_phone

            new_email = input("Введите новый адрес электронной почты (оставьте пустым для сохранения текущего): ").strip()
            if new_email:
                contact["email"] = new_email

            self.save_contacts()
            print("Контакт обновлен.")
        except StopIteration:
            print("Контакт с таким ID не найден.")
        except ValueError:
            print("ID должен быть числом.")

    def delete_contact(self):
        """Удаление контакта."""
        try:
            contact_id = int(input("Введите ID контакта для удаления: "))
            self.contacts = [contact for contact in self.contacts if contact["id"] != contact_id]
            self.save_contacts()
            print("Контакт удален.")
        except ValueError:
            print("ID должен быть числом.")

    def import_contacts(self):
        """Импорт контактов из CSV."""
        filename = input("Введите имя файла CSV для импорта: ").strip()
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.contacts.append({
                        "id": len(self.contacts) + 1,
                        "name": row["name"],
                        "phone": row["phone"],
                        "email": row["email"]
                    })
                self.save_contacts()
                print("Контакты импортированы.")
        except FileNotFoundError:
            print("Файл не найден.")
        except KeyError:
            print("Некорректный формат CSV-файла.")

    def export_contacts(self):
        """Экспорт контактов в CSV."""
        filename = input("Введите имя файла CSV для экспорта: ").strip()
        with open(filename, "w", newline="") as file:
            fieldnames = ["name", "phone", "email"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow({
                    "name": contact["name"],
                    "phone": contact["phone"],
                    "email": contact["email"]
                })
            print("Контакты экспортированы.")

    def manage_contacts(self):
        """Основное меню управления контактами."""
        while True:
            print("\nУправление контактами:")
            print("1. Добавить контакт")
            print("2. Поиск контакта")
            print("3. Редактировать контакт")
            print("4. Удалить контакт")
            print("5. Импорт контактов из CSV")
            print("6. Экспорт контактов в CSV")
            print("7. Назад")

            choice = input("Введите номер действия: ")

            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.search_contact()
            elif choice == '3':
                self.edit_contact()
            elif choice == '4':
                self.delete_contact()
            elif choice == '5':
                self.import_contacts()
            elif choice == '6':
                self.export_contacts()
            elif choice == '7':
                break
            else:
                print("Неверный выбор.")
