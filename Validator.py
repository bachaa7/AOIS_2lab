class ExpressionValidator:
    OPERATORS = {'!': 3, '&': 2, '|': 2, '->': 1}
    VARIABLES = {'a', 'b', 'c', 'd', 'e'}

    @staticmethod
    def validate(expression):
        expression = expression.replace(" ", "")  # Убираем пробелы
        if not expression:
            raise ValueError("Выражение не может быть пустым")

        # Стек для проверки скобок
        stack = []
        last_char = ''
        prev_operator = False
        valid_chars = ExpressionValidator.VARIABLES | {'(', ')', '!', '&', '|', '->'}
        i = 0

        while i < len(expression):
            char = expression[i]

            # Проверяем переменные
            if char in ExpressionValidator.VARIABLES:
                if last_char in ExpressionValidator.VARIABLES:
                    raise ValueError("Между переменными должен быть оператор")
                prev_operator = False

            # Открывающая скобка
            elif char == '(':
                stack.append(char)
                prev_operator = False

            # Закрывающая скобка
            elif char == ')':
                if not stack:
                    raise ValueError("Несбалансированные скобки")
                stack.pop()
                prev_operator = True

            # Отрицание
            elif char == '!':
                # Разрешаем множественные отрицания (!!a)
                if last_char == '!':
                    prev_operator = True  # Это часть последовательности отрицаний
                else:
                    prev_operator = True

            # Операторы AND и OR
            elif char == '&' or char == '|':
                if prev_operator:
                    raise ValueError(f"Нельзя ставить оператор '{char}' после другого оператора")
                prev_operator = True

            # Оператор импликации
            elif char == '-' and i + 1 < len(expression) and expression[i + 1] == '>':
                if last_char in ExpressionValidator.OPERATORS or last_char == '':
                    raise ValueError("Оператор '->' не может быть в начале или после другого оператора")
                prev_operator = True
                i += 1  # Пропускаем следующий символ '>'

            else:
                raise ValueError(f"Некорректный символ: {char}")

            last_char = char
            i += 1

        if stack:
            raise ValueError("Несбалансированные скобки")

        # Проверка на окончание оператора
        if prev_operator and last_char not in {'!', ')'}:
            raise ValueError("Выражение заканчивается оператором")

        return True