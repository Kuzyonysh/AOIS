
class CalculationMethod:
    def __init__(self, truth_table_obj, form="dnf"):
        """
        form: "dnf" - минимизация СДНФ, "knf" - минимизация СКНФ
        """
        self.tt = truth_table_obj
        self.variables = self.tt.variables
        self.table = self.tt.generate()
        self.form = form  # "dnf" или "knf"

    def get_target_value(self):
        return 1 if self.form == "dnf" else 0

    def get_terms(self):
        terms = []
        target = self.get_target_value()
        
        for val_dict, result in self.table:
            if result == target:
                term = {}
                for var in self.variables:
                    term[var] = val_dict[var]
                terms.append(term)
        
        return terms

    def term_to_str(self, term):
        result = []
        for var in self.variables:
            if term[var] == "X":
                continue
            if self.form == "dnf":
                if term[var] == 1:
                    result.append(var)
                elif term[var] == 0:
                    result.append(f"¬{var}")
            else:
                if term[var] == 0:
                    result.append(var)
                elif term[var] == 1:
                    result.append(f"¬{var}")
        
        if self.form == "dnf":
            return "(" + "".join(result) + ")"
        else:
            return "(" + "∨".join(result) + ")"

    def can_combine(self, t1, t2):
        diff = 0
        new_term = {}
        
        for var in self.variables:
            if t1[var] != t2[var]:
                diff += 1
                new_term[var] = "X"
            else:
                new_term[var] = t1[var]
        
        if diff == 1:
            return new_term
        return None

    def combine_stage(self, terms):
        new_terms = []
        used = [False] * len(terms)
        
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                combined = self.can_combine(terms[i], terms[j])
                
                if combined:
                    used[i] = True
                    used[j] = True
                    
                    if combined not in new_terms:
                        new_terms.append(combined)
        
        for i in range(len(terms)):
            if not used[i]:
                if terms[i] not in new_terms:
                    new_terms.append(terms[i])
        
        return new_terms

    def covers(self, term, val_dict):
        for var in self.variables:
            if term[var] == "X":
                continue
            if term[var] != val_dict[var]:
                return False
        return True

    def is_redundant(self, term, all_terms):
        target = self.get_target_value()
        
        for val_dict, result in self.table:
            if result != target:
                continue
                
            if self.covers(term, val_dict):
                covered_by_other = False
                
                for t in all_terms:
                    if t == term:
                        continue
                    if self.covers(t, val_dict):
                        covered_by_other = True
                        break
                
                if not covered_by_other:
                    return False
        
        return True

    def remove_redundant(self, terms):
        result = []
        
        for term in terms:
            if not self.is_redundant(term, terms):
                result.append(term)
        
        return result

    def minimize(self):
        terms = self.get_terms()
        
        if not terms:
            return [] if self.form == "dnf" else []
        
        form_name = "СДНФ" if self.form == "dnf" else "СКНФ"
        print(f"\nИсходная {form_name}:")
        if self.form == "dnf":
            print(" ∨ ".join(self.term_to_str(t) for t in terms))
        else:
            print(" & ".join(self.term_to_str(t) for t in terms))
        
        stage = 1
        while True:
            print(f"\nЭтап склеивания {stage}:")
            
            new_terms = self.combine_stage(terms)
            
            print("Результат:")
            if self.form == "dnf":
                print(" ∨ ".join(self.term_to_str(t) for t in new_terms))
            else:
                print(" & ".join(self.term_to_str(t) for t in new_terms))
            
            if new_terms == terms:
                break
            
            terms = new_terms
            stage += 1
        
        terms = self.remove_redundant(terms)
        
        print(f"\nПосле удаления лишних импликант (минимальная {form_name}):")
        if self.form == "dnf":
            print(" ∨ ".join(self.term_to_str(t) for t in terms))
        else:
            print(" & ".join(self.term_to_str(t) for t in terms))
        
        return terms

    def get_result(self):
        terms = self.minimize()
        
        if self.form == "dnf":
            return " ∨ ".join(self.term_to_str(t) for t in terms)
        else:
            return " & ".join(self.term_to_str(t) for t in terms)
    
    def build_cover_table(self, terms):
        form_name = "ДНФ" if self.form == "dnf" else "КНФ"
        target = self.get_target_value()
        
        print(f"\nТаблица покрытия для {form_name}:")
        
        columns = []
        for val_dict, result in self.table:
            if result == target:
                col_str = ""
                for var in self.variables:
                    col_str += str(int(val_dict[var]))
                columns.append(col_str)
        
        col_width = 10
        header = "Импликанта".ljust(15)
        for c in columns:
            header += c.ljust(col_width)
        print(header)
        print("-" * len(header))
        
        for term in terms:
            row = self.term_to_str(term).ljust(15)
            
            for val_dict, result in self.table:
                if result == target:
                    if self.covers(term, val_dict):
                        row += "X".ljust(col_width)
                    else:
                        row += "".ljust(col_width)
            print(row)
class KarnaughMap:
    def __init__(self, truth_table_obj, form="dnf"):
        """
        form: "dnf" - минимизация СДНФ, "knf" - минимизация СКНФ
        """
        self.tt = truth_table_obj
        self.variables = self.tt.variables
        self.table = self.tt.generate()
        self.form = form  # "dnf" или "knf"
    
    def get_target_value(self):
        return 1 if self.form == "dnf" else 0
    
    def gray(self, n):
        if n == 1:
            return [(0,), (1,)]
        prev = self.gray(n - 1)
        return [(0,) + x for x in prev] + [(1,) + x for x in reversed(prev)]
    
    def build_map(self):
        n = len(self.variables)
        row_vars = n // 2
        col_vars = n - row_vars
        row_gray = self.gray(row_vars)
        col_gray = self.gray(col_vars)
        
        # Заполняем карту значением, противоположным целевому (для поиска групп)
        target = self.get_target_value()
        kmap = [[1-target for _ in range(len(col_gray))] for _ in range(len(row_gray))]
        
        for val_dict, r in self.table:
            if r == target:
                bits = [val_dict[v] for v in self.variables]
                row = row_gray.index(tuple(bits[:row_vars]))
                col = col_gray.index(tuple(bits[row_vars:]))
                kmap[row][col] = target
        
        return kmap, row_gray, col_gray
    
    def is_valid_group(self, kmap, coords):
        target = self.get_target_value()
        return all(kmap[i][j] == target for i, j in coords)
    
    def find_groups(self):
        kmap, row_gray, col_gray = self.build_map()
        
        rows, cols = len(kmap), len(kmap[0])
        
        sizes = [(4,4), (4,2), (2,4), (2,2), (1,4), (4,1), (1,2), (2,1), (1,1)]
        
        used_global = set()
        groups = []
        
        for h, w in sizes:
            used_local = set()
            
            for i in range(rows):
                for j in range(cols):
                    coords = set()
                    
                    for di in range(h):
                        for dj in range(w):
                            r = (i + di) % rows
                            c = (j + dj) % cols
                            coords.add((r, c))
                    
                    coords = frozenset(coords)
                    if coords in used_local:
                        continue
                    if not self.is_valid_group(kmap, coords):
                        continue
                    if coords.issubset(used_global):
                        continue
                    groups.append(list(coords))
                    used_local.add(coords)
                    used_global.update(coords)
        
        return groups, kmap
    
    def group_to_term(self, group, row_gray, col_gray):
        vars = self.variables
        
        values = []
        for i, j in group:
            values.append(row_gray[i] + col_gray[j])
        
        term = {}
        
        for idx, var in enumerate(vars):
            col_vals = [v[idx] for v in values]
            
            if all(v == 1 for v in col_vals):
                term[var] = 1
            elif all(v == 0 for v in col_vals):
                term[var] = 0
            else:
                term[var] = "X"
        
        return term
    
    def term_to_str(self, term):
        result = []
        for var in self.variables:
            if term[var] == "X":
                continue
            if self.form == "dnf":
                if term[var] == 1:
                    result.append(var)
                else:
                    result.append(f"¬{var}")
            else:
                if term[var] == 0:
                    result.append(var)
                else:
                    result.append(f"¬{var}")
        
        if self.form == "dnf":
            return "(" + "".join(result) + ")"
        else:
            return "(" + "∨".join(result) + ")"
    
    def minimize(self):
        groups, kmap = self.find_groups()
        kmap, row_gray, col_gray = self.build_map()
        
        form_name = "СДНФ" if self.form == "dnf" else "СКНФ"
        print(f"\nКарта Карно для {form_name}:")
        self.print_map(kmap)
        
        print(f"\nГруппы Карно для {form_name}:")
        terms = []
        for g in groups:
            print(g)
            term = self.group_to_term(g, row_gray, col_gray)
            terms.append(term)
        
        print(f"\nМинимальная {form_name}:")
        if self.form == "dnf":
            result = " ∨ ".join(self.term_to_str(t) for t in terms)
        else:
            result = " & ".join(self.term_to_str(t) for t in terms)
        print(result)
        
        return terms
    
    def print_map(self, kmap):
        for row in kmap:
            print(row)
