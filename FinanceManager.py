import json
import csv
from collections import defaultdict

class FinanceManager:
    def __init__(self):
        self.finance_file = "finance.json"
        self.records = self.load_records()

    def load_records(self):
        """Загрузка финансовых записей из JSON-файла."""
        try:
            with open(self.finance_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_records(self):
        """Сохранение финансовых записей в JSON-файл."""
        with open(self.finance_file, "w") as file:
            json.dump(self.records, file, indent=4)

    def add_record(self):
        """Добавление новой финансовой записи."""
        try:
            amount = float(input("Введите сумму операции (для доходов положительное, для расходов отрицательное): ").strip())
            if amount == 0:
                print("Сумма не может быть равной нулю.")
                return

            category = input("Введите категорию операции (например, 'Еда', 'Транспорт'): ").strip()
            date = input("Введите дату операции (ДД-ММ-ГГГГ): ").strip()
            description = input("Введите описание операции: ").strip()

            record_id = len(self.records) + 1

            self.records.append({
                "id": record_id,
                "amount": amount,
                "category": category,
                "date": date,
                "description": description
            })

            self.save_records()
            print("Финансовая запись добавлена.")
        except ValueError:
            print("Ошибка ввода суммы. Пожалуйста, введите корректное число.")

    def view_records(self):
        """Просмотр всех финансовых записей с возможностью фильтрации."""
        print("1. Просмотр всех записей")
        print("2. Фильтрация по категории")
        print("3. Фильтрация по дате")

        choice = input("Введите номер действия: ")

        if choice == '1':
            self.display_records(self.records)
        elif choice == '2':
            category = input("Введите категорию для фильтрации: ").strip()
            filtered_records = [record for record in self.records if record["category"].lower() == category.lower()]
            self.display_records(filtered_records)
        elif choice == '3':
            date = input("Введите дату для фильтрации (ДД-ММ-ГГГГ): ").strip()
            filtered_records = [record for record in self.records if record["date"] == date]
            self.display_records(filtered_records)
        else:
            print("Неверный выбор.")

    def display_records(self, records):
        """Вывод всех записей."""
        if not records:
            print("Нет записей для отображения.")
            return
        for record in records:
            print(f"[{record['id']}] {record['amount']} | {record['category']} | {record['date']} | {record['description']}")

    def generate_report(self):
        """Генерация отчёта о финансовой активности за определённый период."""
        start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ").strip()
        end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ").strip()

        report_records = [record for record in self.records if start_date <= record["date"] <= end_date]

        if not report_records:
            print("Нет записей за указанный период.")
        else:
            self.display_records(report_records)

    def calculate_balance(self):
        """Подсчёт общего баланса (доходы минус расходы)."""
        balance = sum(record["amount"] for record in self.records)
        print(f"Общий баланс: {balance:.2f} руб.")

    def group_by_category(self):
        """Группировка расходов и доходов по категориям."""
        categories = defaultdict(float)
        for record in self.records:
            categories[record["category"]] += record["amount"]

        for category, total in categories.items():
            print(f"{category}: {total:.2f} руб.")

    def import_records(self):
        """Импорт финансовых записей из CSV."""
        filename = input("Введите имя файла CSV для импорта: ").strip()
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.records.append({
                        "id": len(self.records) + 1,
                        "amount": float(row["amount"]),
                        "category": row["category"],
                        "date": row["date"],
                        "description": row["description"]
                    })
                self.save_records()
                print("Записи успешно импортированы.")
        except FileNotFoundError:
            print("Файл не найден.")
        except KeyError:
            print("Некорректный формат CSV-файла.")

    def export_records(self):
        """Экспорт финансовых записей в CSV."""
        filename = input("Введите имя файла CSV для экспорта: ").strip()
        with open(filename, "w", newline="") as file:
            fieldnames = ["amount", "category", "date", "description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.records:
                writer.writerow({
                    "amount": record["amount"],
                    "category": record["category"],
                    "date": record["date"],
                    "description": record["description"]
                })
            print("Записи успешно экспортированы.")

    def manage_finances(self):
        """Основное меню управления финансовыми записями."""
        while True:
            print("\nУправление финансовыми записями:")
            print("1. Добавить финансовую запись")
            print("2. Просмотр всех записей")
            print("3. Генерация отчёта за период")
            print("4. Подсчёт баланса")
            print("5. Группировка по категориям")
            print("6. Импорт записей из CSV")
            print("7. Экспорт записей в CSV")
            print("8. Назад")

            choice = input("Введите номер действия: ")

            if choice == '1':
                self.add_record()
            elif choice == '2':
                self.view_records()
            elif choice == '3':
                self.generate_report()
            elif choice == '4':
                self.calculate_balance()
            elif choice == '5':
                self.group_by_category()
            elif choice == '6':
                self.import_records()
            elif choice == '7':
                self.export_records()
            elif choice == '8':
                break
            else:
                print("Неверный выбор.")
