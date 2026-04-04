
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
        self.tt = truth_table_obj
        self.variables = self.tt.variables
        self.table = self.tt.generate()
        self.form = form.lower()

    def target(self):
        return 1 if self.form == "dnf" else 0

    def gray_code(self, n):
        if n == 0:
            return [()]
        prev = self.gray_code(n - 1)
        return [(0,) + x for x in prev] + [(1,) + x for x in reversed(prev)]

    def build_map(self):
        n = len(self.variables)
        rows = 1 << ((n + 1) // 2)
        cols = 1 << (n // 2)

        row_gray = self.gray_code((n + 1) // 2)
        col_gray = self.gray_code(n // 2)

        t = self.target()
        kmap = [[1 - t for _ in range(cols)] for _ in range(rows)]

        for vals_dict, res in self.table:
            if res == t:
                bits = tuple(vals_dict[v] for v in self.variables)
                row_bits = bits[:len(row_gray[0])]
                col_bits = bits[len(row_gray[0]):]

                r_i = row_gray.index(row_bits)
                c_i = col_gray.index(col_bits)
                kmap[r_i][c_i] = t

        return kmap, row_gray, col_gray

    def get_minterms(self, kmap):
        target = self.target()
        return [
            (i, j)
            for i in range(len(kmap))
            for j in range(len(kmap[0]))
            if kmap[i][j] == target
        ]

    def cell_to_bits(self, i, j, row_gray, col_gray):
        return row_gray[i] + col_gray[j]

    def combine(self, a, b):
        diff = 0
        res = []

        for x, y in zip(a, b):
            if x != y:
                diff += 1
                res.append("X")
            else:
                res.append(x)

        return tuple(res) if diff == 1 else None

    def build_implicants(self, minterms_bits):
        current = set(minterms_bits)
        primes = set()

        while True:
            used = set()
            new = set()

            current = list(current)

            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    c = self.combine(current[i], current[j])
                    if c:
                        new.add(c)
                        used.add(current[i])
                        used.add(current[j])

            for x in current:
                if x not in used:
                    primes.add(x)

            if not new:
                break

            current = new

        return list(primes)
    def term_to_dict(self, pattern):
        term = {}

        for i, v in enumerate(self.variables):
            if pattern[i] == "X":
                continue
            term[v] = int(pattern[i])

        return term

    def term_to_str(self, term):
        parts = []

        for v in self.variables:
            val = term.get(v)
            if val is None:
                continue

            if self.form == "dnf":
                parts.append(v if val == 1 else f"¬{v}")
            else:
                parts.append(v if val == 0 else f"¬{v}")

        if not parts:
            return "1" if self.form == "dnf" else "0"

        if self.form == "dnf":
            return "".join(parts)
        else:
            return "(" + "∨".join(parts) + ")"

    def minimize(self):
        kmap, row_gray, col_gray = self.build_map()

        print("\n=== Карта Карно ===")
        for row in kmap:
            print([str(x) for x in row])

        minterms = self.get_minterms(kmap)

        minterms_bits = [
            self.cell_to_bits(i, j, row_gray, col_gray)
            for i, j in minterms
        ]
        primes = self.build_implicants(minterms_bits)

        terms = [self.term_to_dict(p) for p in primes]

        print("\n=== Минимальная форма ===")

        joiner = " ∨ " if self.form == "dnf" else " ∧ "
        result = joiner.join(self.term_to_str(t) for t in terms)

        print(result)

        return terms
