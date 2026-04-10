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
        pattern = r'([a-zA-Z!()]+)\s*->\s*([a-zA-Z!()]+)'
        expr = re.sub(pattern, r'(not \1 or \2)', expr)
        return expr

    def replace_equivalence(self, expr):
        pattern = r'([a-zA-Z!()]+)\s*~\s*([a-zA-Z!()]+)'
        expr = re.sub(pattern, r'(\1 == \2)', expr)
        return expr

    def prepare_expression(self, expr):
        expr = expr.replace(' ', '')
        
        expr = self.replace_equivalence(expr)  
        expr = self.replace_implication(expr)  
        
        expr = expr.replace('!', ' not ')
        expr = expr.replace('&', ' and ')
        expr = expr.replace('|', ' or ')
        
        expr = re.sub(r'\s+', ' ', expr)
        
        return expr

    def get_variables(self):
        return sorted(set(re.findall(r'[a-zA-Z]', self.expr)))

    def evaluate(self, values: dict):
        expr_eval = self.expr
        
        for var in sorted(values.keys(), key=len, reverse=True):
            val = 'True' if values[var] else 'False'
            expr_eval = re.sub(r'\b' + var + r'\b', val, expr_eval)
    
        expr_eval = self.prepare_expression(expr_eval)
        
        if not expr_eval.strip():
            return False
        
        try:
            result = eval(expr_eval)
            return bool(result)
        except Exception as e:
            print(f"Ошибка при вычислении: {expr_eval}")
            print(f"Ошибка: {e}")
            return False

    def evaluate_with_steps(self, values: dict):
        steps = {}
        subexprs = self.extract_subexpressions()

        for sub in subexprs:
            temp = sub
            for var in sorted(values.keys(), key=len, reverse=True):
                val = 'True' if values[var] else 'False'
                temp = re.sub(r'\b' + var + r'\b', val, temp)
            
            temp = self.prepare_expression(temp)
            try:
                result = eval(temp)
                steps[sub] = int(result)
            except Exception as e:
                print(f"Ошибка при вычислении подвыражения: {temp}")
                print(f"Ошибка: {e}")
                steps[sub] = 0

        return steps