from HashTable import HashTable
from TablePrinter import TablePrinter
class Menu:
    def __init__(self):
        self.hash_table = HashTable()
        self.printer = TablePrinter()

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
        self.hash_table.insert(key, value)

    def search(self):
        key = input("Введите ключ: ")
        result = self.hash_table.get(key)
        if result is None:
            print("Не найдено")
        else:
            print("Найдено:", result)

    def update(self):
        key = input("Введите ключ: ")
        value = input("Введите новое значение: ")
        self.hash_table.update(key, value)

    def delete(self):
        key = input("Введите ключ: ")
        self.hash_table.delete(key)

    def display(self):
        self.printer.print_table(self.hash_table)

    def load_factor(self):
        print("Коэффициент заполнения:", self.hash_table.load_factor())

if __name__ == "__main__":
    menu = Menu()
    menu.run()