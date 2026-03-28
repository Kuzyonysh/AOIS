from truth_table import TruthTable 

class NormalForms:

    def __init__(self, truth_table_obj: TruthTable):
        self.tt = truth_table_obj  
        self.variables = self.tt.variables
        self.table = self.tt.generate() 
    def build_sdnf(self):
        terms = []

        for val_dict, result in self.table:
            if result == 1:
                term = []
                for var in self.variables:
                    term.append(var if val_dict[var] == 1 else f"¬{var}")
                terms.append("(" + "∧".join(term) + ")")

        return " ∨ ".join(terms)

    def build_sknf(self):
        terms = []

        for val_dict, result in self.table:
            if result == 0:
                term = []
                for var in self.variables:
                    term.append(f"¬{var}" if val_dict[var] == 1 else var)
                terms.append("(" + "∨".join(term) + ")")

        return " ∧ ".join(terms)

    def sdnf_numeric(self):
        nums = [str(i) for i, (_, result) in enumerate(self.table) if result == 1]
        return "{" + ", ".join(nums) + "}"

    def sknf_numeric(self):
        nums = [str(i) for i, (_, result) in enumerate(self.table) if result == 0]
        return "{" + ", ".join(nums) + "}"
    def index_form(self):
        return "".join(str(result) for _, result in self.table)