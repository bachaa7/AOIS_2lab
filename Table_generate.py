import itertools
from Validator import ExpressionValidator
from rpn_converter import RPNConverter
from Logic_solver import LogicSolver


class TruthTableGenerator:
    def __init__(self, expression):
        self.expression = expression
        self.variables = sorted(ExpressionValidator.VARIABLES & set(expression))
        self.rpn_converter = RPNConverter(expression)
        self.subexpressions = []
        self.subexpression_strings = []

    def generate_truth_table(self):
        self.parse_subexpressions()
        rpn_expr = self.rpn_converter.convert_to_rpn()
        table = []

        for values in itertools.product([False, True], repeat=len(self.variables)):
            variable_values = dict(zip(self.variables, values))

            subresults = []
            for subexpr in self.subexpressions:
                solver = LogicSolver(subexpr)
                subresults.append(solver.compute(variable_values))

            solver = LogicSolver(rpn_expr)
            final_result = solver.compute(variable_values)

            table.append((variable_values, subresults, final_result))

        return table

    def compute_index_form(self):
        truth_table = self.generate_truth_table()
        binary_repr = "".join(str(int(final_result)) for _, _, final_result in truth_table)
        decimal_value = int(binary_repr, 2)

        return {
            "binary": binary_repr,
            "decimal": decimal_value
        }

    def rpn_to_str(self, expr):
        stack = []
        for token in expr:
            if token in self.variables:
                stack.append(token)
            elif token == '!':
                val = stack.pop()
                stack.append(f"!{val}")
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(f"({a} {token} {b})")
        return stack[0]

    def parse_subexpressions(self):
        stack = []
        rpn_expr = self.rpn_converter.convert_to_rpn()

        for token in rpn_expr:
            if token in self.variables:
                stack.append([token])
            elif token == '!':
                operand = stack.pop()
                new_expr = operand + [token]
                stack.append(new_expr)
                self.subexpressions.append(new_expr)
            else:
                right = stack.pop()
                left = stack.pop()
                new_expr = left + right + [token]
                stack.append(new_expr)
                self.subexpressions.append(new_expr)

        for expr in self.subexpressions:
            self.subexpression_strings.append(self.rpn_to_str(expr))

    def display_table(self):
        table = self.generate_truth_table()
        col_width = 6

        headers = self.variables + self.subexpression_strings + ["Result"]
        header_row = " | ".join(f"{h:<{col_width}}" for h in headers)
        print("Таблица истинности:")
        print(header_row)
        print("-" * len(header_row))

        for row in table:
            variable_values, subresults, result = row
            values_str = " | ".join(f"{int(variable_values[var]):<{col_width}}" for var in self.variables)
            sub_strs = " | ".join(f"{int(val):<{col_width}}" for val in subresults)
            result_str = f"{int(result):<{col_width}}"
            print(f"{values_str} | {sub_strs} | {result_str}")



