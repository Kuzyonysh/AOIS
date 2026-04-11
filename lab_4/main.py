from HashTable import HashTable
from TablePrinter import TablePrinter
from exception import KeyExistsError, TableFullError, KeyNotFoundError


class Menu:
    def __init__(self):
        self.hash_table = HashTable()
        self.printer = TablePrinter()
        self.preload_data()

    def preload_data(self):
        data = [
            ("Иванов", "Математика"),
            ("Петров", "Физика"),
            ("Сидоров", "Информатика"),
            ("Смирнов", "Математика"),
            ("Кузнецов", "Химия"),
            ("Попов", "Биология"),
            ("Васильев", "Математика"),
            ("Новиков", "Физика"),
            ("Федоров", "Информатика"),
            ("Морозов", "Математика"),
            ("Титов", "Физика"),
            ("Орлов", "Химия"),
            ("Белов", "Биология"),
            ("Громов", "Информатика"),
            ("Зайцев", "Математика")
        ]

        print(">>> Предзагрузка данных...\n")

        for key, value in data:
            try:
                print(f"Добавляем: {key} → {value}")
                self.hash_table.insert(key, value)
            except Exception as e:
                print(f"Ошибка при добавлении {key}: {e}")

    def run(self):
        while True:
            self.print_menu()
            choice = input("Выберите действие: ")

            if choice == "1":
                self.insert()
            elif choice == "2":
                self.search()
            elif choice == "3":
                self.update()
            elif choice == "4":
                self.delete()
            elif choice == "5":
                self.display()
            elif choice == "6":
                self.load_factor()
            elif choice == "0":
                print("Выход...")
                break
            else:
                print("Неверный ввод!")

    def print_menu(self):
        print("\n=== МЕНЮ ===")
        print("1. Добавить запись")
        print("2. Найти запись")
        print("3. Обновить запись")
        print("4. Удалить запись")
        print("5. Показать таблицу")
        print("6. Коэффициент заполнения")
        print("0. Выход")

    def insert(self):
        key = input("Введите ключ (фамилия): ")
        value = input("Введите значение: ")

        try:
            self.hash_table.insert(key, value)
            print("Запись добавлена")

        except KeyExistsError as e:
            print("Ошибка:", e)

        except TableFullError as e:
            print("Ошибка:", e)

        except Exception as e:
            print("Неизвестная ошибка:", e)

    def search(self):
        key = input("Введите ключ: ")

        try:
            result = self.hash_table.get(key)
            if result is None:
                print("Не найдено")
            else:
                print("Найдено:", result)

        except Exception as e:
            print("Ошибка:", e)

    def update(self):
        key = input("Введите ключ: ")
        value = input("Введите новое значение: ")

        try:
            self.hash_table.update(key, value)
            print("Обновлено")

        except KeyNotFoundError as e:
            print("Ошибка:", e)

        except Exception as e:
            print("Ошибка:", e)

    def delete(self):
        key = input("Введите ключ: ")

        try:
            self.hash_table.delete(key)
            print("Удалено")

        except KeyNotFoundError as e:
            print("Ошибка:", e)

        except Exception as e:
            print("Ошибка:", e)

    def display(self):
        try:
            self.printer.print_table(self.hash_table)
        except Exception as e:
            print("Ошибка:", e)

    def load_factor(self):
        try:
            print("Коэффициент заполнения:", self.hash_table.load_factor())
        except Exception as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    menu = Menu()
    menu.run()
