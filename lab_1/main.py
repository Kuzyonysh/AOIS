from conversion_int import IntegerNumber
from conversion_float import FloatNumber
from Excess3 import Excess3Calculator
from operations_integer import IntegerOperations
from operations_float import FloatOperations

def menu():
    while True:
        print("1. Перевод числа в прямой, обратный и дополнительный коды")
        print("2. Сложение двух чисел в дополнительном коде")
        print("3. Вычитание двух чисел в дополнительном коде")
        print("4. Умножение двух чисел в прямом коде")
        print("5. Деление двух чисел в прямом коде")
        print("6. Сложение чисел с плавающей точкой")
        print("7. Вычитание чисел с плавающей точкой")
        print("8. Умножение чисел с плавающей точкой")
        print("9. Деление чисел с плавающей точкой")
        print("10. Сложение чисел в Excess-3")
        print("0. Выход")
        choice = input("Выберите операцию: ")

        if choice == "0":
            break

        elif choice == "1":
            n = int(input("Введите число: "))
            straight = IntegerNumber.conversion_to_binary_straight(n)
            inversion = IntegerNumber.conversion_to_binary_inversion(n)
            additional = IntegerNumber.conversion_to_binary_additional(n)
            print(f"Прямой код:      {straight} -> {IntegerNumber.binary_straight_to_decimal(straight)}")
            print(f"Обратный код:    {inversion} -> {IntegerNumber.binary_inverse_to_decimal(inversion)}")
            print(f"Дополнительный:  {additional} -> {IntegerNumber.binary_additional_to_decimal(additional)}")

        elif choice == "2":
            a = int(input("Введите первое число: "))
            b = int(input("Введите второе число: "))
            res = IntegerOperations.sum_in_additional(a, b)
            if res:
                bits, dec = res
                print(f"Результат (доп. код): {bits} -> {dec}")

        elif choice == "3":
            a = int(input("Введите уменьшаемое: "))
            b = int(input("Введите вычитаемое: "))
            res = IntegerOperations.subtraction_in_additional(a, b)
            if res:
                bits, dec = res
                print(f"Результат (доп. код): {bits} -> {dec}")

        elif choice == "4":
            a = int(input("Введите первое число: "))
            b = int(input("Введите второе число: "))
            res = IntegerOperations.multiplication_in_straight(a, b)
            if res:
                bits, dec = res
                print(f"Результат (прямой код): {bits} -> {dec}")

        elif choice == "5":
            a = int(input("Введите делимое: "))
            b = int(input("Введите делитель: "))
            res = IntegerOperations.division_in_straight(a, b, precision=5)
            if res:
                bits, dec = res
                print(f"Результат (прямой код): {bits} -> {dec}")

        elif choice == "6":
            a = float(input("Введите первое число: "))
            b = float(input("Введите второе число: "))
            bits, dec = FloatOperations.sum_to_binary_float(a, b)
            print(f"Результат IEEE-754: {bits} -> {dec}")

        elif choice == "7":
            a = float(input("Введите уменьшаемое: "))
            b = float(input("Введите вычитаемое: "))
            bits, dec = FloatOperations.subtract_binary_float(a, b)
            print(f"Результат IEEE-754: {bits} -> {dec}")

        elif choice == "8":
            a = float(input("Введите первое число: "))
            b = float(input("Введите второе число: "))
            bits, dec = FloatOperations.multiply_binary_float(a, b)
            print(f"Результат IEEE-754: {bits} -> {dec}")

        elif choice == "9":
            a = float(input("Введите делимое: "))
            b = float(input("Введите делитель: "))
            bits, dec = FloatOperations.division_ieee(a, b)
            print(f"Результат IEEE-754: {bits} -> {dec}")

        elif choice == "10":
            a = int(input("Введите первое число: "))
            b = int(input("Введите второе число: "))
            bits, dec = Excess3Calculator.excess3_sum(a, b)
            print(f"Результат Excess-3: {bits} -> {dec}")

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    menu()