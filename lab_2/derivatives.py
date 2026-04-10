
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
    def simplify_derivative(self, var=None, vars_list=None):
   
        if var is not None:

            vector, formula = self.partial_with_formula(var)
        elif vars_list is not None:
            vector, formula = self.mixed_derivative(vars_list)
        else:
            raise ValueError("Укажите var или vars_list")
    
        if formula == "0":
            return "0"
        terms = [term.strip('()') for term in formula.split(' | ')]
        simplified = self._simplify_terms(terms)
        if not simplified:
            return "0"
    
        result_terms = []
        for term in simplified:
            if term == '1':
                result_terms.append("1")
            else:
                var_list = term.split(' & ')
                result_terms.append("(" + " & ".join(var_list) + ")")
    
        return " | ".join(result_terms)

    def _simplify_terms(self, terms):   
        if len(terms) <= 1:
            return terms
    
        changed = True
        while changed:
            changed = False
            new_terms = []
            used = [False] * len(terms)
        
            for i in range(len(terms)):
                if used[i]:
                    continue
                
                term1_parts = terms[i].split(' & ') if terms[i] != '1' else ['1']
                term1 = set(term1_parts)
                merged = False
            
                for j in range(i + 1, len(terms)):
                    if used[j]:
                        continue
                    
                    term2_parts = terms[j].split(' & ') if terms[j] != '1' else ['1']
                    term2 = set(term2_parts)
                    sym_diff = term1.symmetric_difference(term2)
                    if len(sym_diff) == 2:
                        vars_diff = list(sym_diff)
                        var1 = vars_diff[0].replace('!', '')
                        var2 = vars_diff[1].replace('!', '')
                    
                        if var1 == var2:
                            common = term1.intersection(term2)
                            if '1' in common:
                                common.remove('1')
                        
                            if common:
                                new_terms.append(' & '.join(sorted(list(common))))
                            else:
                                new_terms.append('1')
                        
                            used[i] = used[j] = True
                            merged = True
                            changed = True
                            break
            
                if not merged and not used[i]:
                    new_terms.append(terms[i])
        
            terms = new_terms
        terms = list(set(terms))
        final_terms = []
        for i, term1 in enumerate(terms):
            if term1 == '1':
                return ['1']
            
            set1 = set(term1.split(' & '))
            absorbed = False
        
            for j, term2 in enumerate(terms):
                if i != j and term2 != '1':
                    set2 = set(term2.split(' & '))
                    if set2.issubset(set1):
                        absorbed = True
                        break
        
            if not absorbed:
                final_terms.append(term1)
    
        return final_terms if final_terms else ['0']
    def compress_vector(self, vector, var):
        step = 2 ** (len(self.variables) - self.variables.index(var) - 1)
        return vector[:step]
    def compress_vector_multi(self, vector, vars_list):
        step = 1
        for var in vars_list:
            step *= 2
        return vector[:len(vector) // step]