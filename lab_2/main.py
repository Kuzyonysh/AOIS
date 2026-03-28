from truth_table import TruthTable
from scnf_sdnf import NormalForms
from post_classes import PostClasses
from zhegalkin import Zhegalkin
from fictitious_variables import FictitiousVariables
from derivatives import BooleanDerivative
from minimization import CalculationMethod, KarnaughMap

def main():
    expr = input("Введите логическую функцию \n> ")

    tt = TruthTable(expr)
    nf = NormalForms(tt)

    while True:
        print("\nВыберите действие:")
        print("1 - Построить таблицу истинности")
        print("2 - Построить СДНФ и вывести числовую форму")
        print("3 - Построить СКНФ и вывести числовую форму")
        print("4 - Вывести индексную форму функции")
        print("5 - Проверка принадлежности к классам Поста")
        print("6 - Полином Жегалкина (метод Паскаля)")
        print("7 - Поиск фиктивных переменных")
        print("8 - Булева производная (частная)")
        print("9 - Булева производная (смешанная)")
        print("10 - Минимизация функции (расчетный метод)")
        print("11 - Минимизация функции (расчетно-табличный метод)")
        print("12 - Минимизация функции (табличный метод)")
        print("0 - Выйти")

        choice = input("> ")
        
        if choice == "1":
            print("\n--- Таблица истинности ---")
            tt.print_table()
            
        elif choice == "2":
            print("\n--- СДНФ ---")
            print(nf.build_sdnf())
            print("Числовая форма СДНФ:", nf.sdnf_numeric())
            
        elif choice == "3":
            print("\n--- СКНФ ---")
            print(nf.build_sknf())
            print("Числовая форма СКНФ:", nf.sknf_numeric())
            
        elif choice == "4":
            print("\n--- Индексная форма функции ---")
            print(nf.index_form())
            
        elif choice == "5":
            pc = PostClasses(tt)
            results = pc.check_all()
            print("\n--- Классы Поста ---")
            for key, value in results.items():
                print(f"{key}: {'Да' if value else 'Нет'}")
                
        elif choice == "6":
            zh = Zhegalkin(tt)
            print("\n--- Полином Жегалкина ---")
            print(zh.build_polynomial())
            
        elif choice == "7":
            fv = FictitiousVariables(tt)
            result = fv.find_fictitious()
            print("\n--- Фиктивные переменные ---")
            if result:
                print(", ".join(result))
            else:
                print("Фиктивных переменных нет")
                
        elif choice == "8":
            bd = BooleanDerivative(tt)
            print("\nПеременные:", ", ".join(tt.variables))
            var = input("Введите переменную для производной: ")
            vector, formula = bd.partial_with_formula(var)
            simplified = bd.simplify_derivative(var)
            print("\n--- Частная производная ---")
            print("Вектор:", vector)
            print("Формула:", simplified)
            
        elif choice == "9":
            bd = BooleanDerivative(tt)
            print("\nПеременные:", ", ".join(tt.variables))
            vars_input = input("Введите переменные для смешанной производной (через пробел): ")
            vars_list = vars_input.split()
    
            vector, formula = bd.mixed_derivative(vars_list)
    
            print("\n--- Смешанная производная ---")
            derivative_str = "∂" + "".join(vars_list) + "f/∂" + "∂".join(vars_list)
            print("Вектор:", vector)
            print("Формула:", bd.simplify_derivative(vars_list=vars_list))
            
        elif choice == "10":
            print("\nВыберите форму минимизации:")
            print("1 - СДНФ (Дизъюнктивная форма)")
            print("2 - СКНФ (Конъюнктивная форма)")
            form_choice = input("> ")
            form = "dnf" if form_choice == "1" else "knf" if form_choice == "2" else "dnf"
            
            cm = CalculationMethod(tt, form)
            print("\n--- Расчетный метод (Квайн-МакКласки) ---")
            result = cm.get_result()
            print(f"\nИтог ({'ДНФ' if form == 'dnf' else 'КНФ'}):")
            print(result)
            
        elif choice == "11":
            print("\nВыберите форму минимизации:")
            print("1 - СДНФ (Дизъюнктивная форма)")
            print("2 - СКНФ (Конъюнктивная форма)")
            form_choice = input("> ")
            form = "dnf" if form_choice == "1" else "knf" if form_choice == "2" else "dnf"
            
            calc = CalculationMethod(tt, form)
            print("\n--- Расчетно-табличный метод ---")
            terms = calc.minimize()
            calc.build_cover_table(terms)
            
            if form == "dnf":
                result = " ∨ ".join(calc.term_to_str(t) for t in terms)
            else:
                result = " & ".join(calc.term_to_str(t) for t in terms)
            
            print(f"\nИтог ({'ДНФ' if form == 'dnf' else 'КНФ'}):")
            print(result)
            
        elif choice == "12":
            print("\nВыберите форму минимизации:")
            print("1 - СДНФ (Дизъюнктивная форма)")
            print("2 - СКНФ (Конъюнктивная форма)")
            form_choice = input("> ")
            form = "dnf" if form_choice == "1" else "knf" if form_choice == "2" else "dnf"
            
            km = KarnaughMap(tt, form)
            terms = km.minimize()
            
            if form == "dnf":
                result = " ∨ ".join(km.term_to_str(t) for t in terms)
            else:
                result = " & ".join(km.term_to_str(t) for t in terms)
            
            print(f"\nМинимизированная функция ({'ДНФ' if form == 'dnf' else 'КНФ'}):")
            print(result)
            
        elif choice == "0":
            print("Выход из программы.")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
