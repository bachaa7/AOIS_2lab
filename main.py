from Validator import ExpressionValidator
from rpn_converter import RPNConverter
from Truth_table_processor import TruthTableProcessor
from Table_generate import TruthTableGenerator

def main():
    expression = input("Введите логическое выражение: ")

    # Проверка выражения
    try:
        ExpressionValidator.validate(expression)
    except ValueError as e:
        print(f"Ошибка в выражении: {e}")
        return

    try:
        # Проверяем, что выражение корректное
        ExpressionValidator.validate(expression)

        # Генерируем таблицу истинности
        generator = TruthTableGenerator(expression)
        print("\nТаблица истинности:")
        generator.display_table()

    except ValueError as e:
        print(f"Ошибка: {e}")


    # Преобразование в ОПН
    rpn_converter = RPNConverter(expression)
    rpn_expression = rpn_converter.convert_to_rpn()
    #print(f"Обратная польская нотация: {' '.join(rpn_expression)}")

    # Генерация таблицы истинности
    truth_table_generator = TruthTableGenerator(expression)
    truth_table = truth_table_generator.generate_truth_table()

    # Нахождение нормальных форм
    processor = TruthTableProcessor(truth_table, truth_table_generator.variables)
    normal_forms = processor.get_normal_forms()

    print("\nСДНФ:", normal_forms["СДНФ"])
    print("СКНФ:", normal_forms["СКНФ"])
    print("Индексы СДНФ:", normal_forms["СДНФ Индексы"],"|")
    print("Индексы СКНФ:", normal_forms["СКНФ Индексы"],"&")

    # Индексная форма
    index_form = truth_table_generator.compute_index_form()
    print("\nБинарная форма:", index_form["binary"])
    print("Десятичная форма:", index_form["decimal"])

if __name__ == "__main__":
    main()


#a | b & !c
