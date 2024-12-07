class Calculator:
    def start_calculator(self):
        print("\nКалькулятор:")
        while True:
            expression = input("Введите выражение (или 'назад' для выхода): ")
            if expression.lower() == 'назад':
                break
            try:
                result = eval(expression)
                print(f"Результат: {result}")
            except ZeroDivisionError:
                print("Ошибка: Деление на ноль!")
            except Exception as e:
                print(f"Ошибка: {e}")