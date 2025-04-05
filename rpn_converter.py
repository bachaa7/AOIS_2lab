from Validator import ExpressionValidator

class RPNConverter:
    def __init__(self, expression):
        self.expression = expression.replace(" ", "")
        self.operators = ExpressionValidator.OPERATORS
        self.variables = ExpressionValidator.VARIABLES

    def convert_to_rpn(self):
        output = []
        stack = []
        i = 0

        while i < len(self.expression):
            char = self.expression[i]

            if char in self.variables:
                output.append(char)

            elif char == '!':
                stack.append(char)

            elif char in {'&', '|', '~'}:
                while stack and stack[-1] in self.operators and self.operators[stack[-1]] >= self.operators[char]:
                    output.append(stack.pop())
                stack.append(char)

            elif char == '-' and i + 1 < len(self.expression) and self.expression[i + 1] == '>':
                char = '->'
                i += 1
                while stack and stack[-1] in self.operators and self.operators[stack[-1]] >= self.operators[char]:
                    output.append(stack.pop())
                stack.append(char)

            elif char == '(':
                stack.append(char)

            elif char == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                else:
                    raise ValueError("Несбалансированные скобки")

            else:
                raise ValueError(f"Неожиданный символ: {char}")

            i += 1

        while stack:
            top = stack.pop()
            if top in '()':
                raise ValueError("Несбалансированные скобки")
            output.append(top)

        return output
