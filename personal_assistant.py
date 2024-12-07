import json
from datetime import datetime
from NoteManager import NoteManager
from TaskManager import TaskManager
from ContactManager import ContactManager
from FinanceManager import FinanceManager
from Calculator import Calculator
import csv


def main():
    print("Добро пожаловать в Персональный помощник!")

    while True:
        print("\nВыберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            note_manager = NoteManager()
            note_manager.manage_notes()

        elif choice == '2':
            task_manager = TaskManager()
            task_manager.manage_tasks()

        elif choice == '3':
            contact_manager = ContactManager()
            contact_manager.manage_contacts()

        elif choice == '4':
            finance_manager = FinanceManager()
            finance_manager.manage_finances()

        elif choice == '5':
            calc = Calculator()
            calc.start_calculator()

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, пожалуйста, выберите правильный пункт.")

if __name__ == "__main__":
    main()