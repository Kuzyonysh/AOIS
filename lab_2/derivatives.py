
class BooleanDerivative:
    def __init__(self, truth_table_obj):
        self.tt = truth_table_obj
        self.table = self.tt.generate()
        self.variables = self.tt.variables
        self.bf = self.tt.bf

  
    def partial_derivative(self, var):
        vector = []

        for val_dict, _ in self.table:
            val0 = val_dict.copy()
            val1 = val_dict.copy()

            val0[var] = 0
            val1[var] = 1

            f0 = int(self.bf.evaluate(val0))
            f1 = int(self.bf.evaluate(val1))

            vector.append(f0 ^ f1)

        return vector

    
    def vector_to_sdnf(self, vector):
        terms = []

        for i, (val_dict, _) in enumerate(self.table):
            if vector[i] == 1:
                term = []

                for v in self.variables:
                    if val_dict[v] == 1:
                        term.append(v)
                    else:
                        term.append(f"!{v}")

                terms.append("(" + " & ".join(term) + ")")

        return " | ".join(terms) if terms else "0"

    
    def partial_with_formula(self, var):
        vector = self.partial_derivative(var)
        formula = self.vector_to_sdnf(vector)
        return vector, formula

    
    def mixed_derivative(self, vars_list):
        vector = self.partial_derivative(vars_list[0])

        for var in vars_list[1:]:
            vector = self._vector_derivative(vector, var)

        return vector, self.vector_to_sdnf(vector)

    def _vector_derivative(self, vector, var):
        new_vector = []

        idx_shift = 1 << (len(self.variables) - self.variables.index(var) - 1)

        for i in range(len(vector)):
            j = i ^ idx_shift
            new_vector.append(vector[i] ^ vector[j])

        return new_vector
  