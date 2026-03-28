import itertools
from evaluator import BooleanFunction


class TruthTable:
    def __init__(self, expr):
        self.expr = expr
        self.bf = BooleanFunction(expr)
        self.variables = self.bf.get_variables()

    def generate(self):
        table = []

        for values in itertools.product([0, 1], repeat=len(self.variables)):
            val_dict = dict(zip(self.variables, values))

            result = self.bf.evaluate(val_dict)

            table.append((val_dict, int(result)))

        return table

    def print_table(self):
        table = self.generate()

        print(" ".join(self.variables), "| F")
        for val_dict, result in table:
            row = [str(val_dict[var]) for var in self.variables]
            print(" ".join(row), "|", result)

    def print_table_with_steps(self):
        table = self.generate()  
        subexprs = self.bf.extract_subexpressions()
    
        if not subexprs:
            subexprs = [self.expr]

    
        print(" ".join(self.variables), "|", " | ".join(subexprs))

        for values in itertools.product([0, 1], repeat=len(self.variables)):
            val_dict = dict(zip(self.variables, values))
            steps = self.bf.evaluate_with_steps(val_dict)

            row = list(values)
            step_values = [str(steps.get(sub, self.bf.evaluate(val_dict))) for sub in subexprs]
            print(" ".join(map(str, row)), "|", " | ".join(step_values))