import re

class BooleanFunction:
    def __init__(self, expr):
        self.expr = expr
    def extract_subexpressions(self):
        pattern = r'\([^()]+\)'
        subexprs = []
        expr = self.expr

        while re.search(pattern, expr):
            match = re.search(pattern, expr)
            sub = match.group()
            subexprs.append(sub)
            expr = expr.replace(sub, 'X', 1)
        return subexprs

    def replace_implication(self, expr):
        pattern = r'(\w+)\s*->\s*(\w+)'
        while re.search(pattern, expr):
            expr = re.sub(pattern, r'(not \1 or \2)', expr)
        return expr

    def replace_equivalence(self, expr):
        pattern = r'(\w+)\s*~\s*(\w+)'
        while re.search(pattern, expr):
            expr = re.sub(pattern, r'(\1 == \2)', expr)
        return expr

    def prepare_expression(self, expr):
        expr = expr.replace(' ', '')

        expr = self.replace_implication(expr)
        expr = self.replace_equivalence(expr)

        expr = expr.replace('!', ' not ')
        expr = expr.replace('&', ' and ')
        expr = expr.replace('|', ' or ')

        return expr

    def get_variables(self):
        return sorted({ch for ch in self.expr if ch in 'abcde'})

    def evaluate(self, values: dict):
        expr_eval = self.expr
        for var, val in values.items():
            expr_eval = expr_eval.replace(var, str(bool(val)))
        expr_eval = self.prepare_expression(expr_eval)
        return eval(expr_eval)

    def evaluate_with_steps(self, values: dict):
        steps = {}
        subexprs = self.extract_subexpressions()

        for sub in subexprs:
            temp = sub
            for var, val in values.items():
                temp = temp.replace(var, str(bool(val)))
            temp = self.prepare_expression(temp)
            result = eval(temp)
            steps[sub] = int(result)

        return steps