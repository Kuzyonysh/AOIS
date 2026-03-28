import itertools
class CalculationMethod:
    def __init__(self, truth_table_obj):
        self.tt = truth_table_obj
        self.variables = self.tt.variables
        self.table = self.tt.generate()

    def get_terms(self):
        terms = []

        for val_dict, result in self.table:
            if result == 1:
                term = {}
                for var in self.variables:
                    term[var] = val_dict[var]
                terms.append(term)

        return terms

    def term_to_str(self, term):
        result = []
        for var in self.variables:
            if term[var] == 1:
                result.append(var)
            elif term[var] == 0:
                result.append(f"¬{var}")
        return "(" + "".join(result) + ")"


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
        for val_dict, _ in self.table:

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

        print("\nИсходная СДНФ:")
        print(" ∨ ".join(self.term_to_str(t) for t in terms))

        stage = 1
        while True:
            print(f"\nЭтап склеивания {stage}:")

            new_terms = self.combine_stage(terms)

            print("Результат:")
            print(" ∨ ".join(self.term_to_str(t) for t in new_terms))

            if new_terms == terms:
                break

            terms = new_terms
            stage += 1

        terms = self.remove_redundant(terms)

        print("\nПосле удаления лишних импликант:")
        print(" ∨ ".join(self.term_to_str(t) for t in terms))

        return terms

    def get_result(self):
        terms = self.minimize()

        return " ∨ ".join(self.term_to_str(t) for t in terms)
    def build_cover_table(self, terms):
        print("\nТаблица покрытия:")

        columns = []
        for val_dict, result in self.table:
            if result == 1:
                columns.append(self.term_to_str(val_dict))
        col_width = 10
        header = "Импликанта".ljust(15)
        for c in columns:
            header += c.ljust(col_width)
        print(header)
        for term in terms:
            row = self.term_to_str(term).ljust(15)

            for val_dict, result in self.table:
                if result == 1:
                    if self.covers(term, val_dict):
                        row += "X".ljust(col_width)
                    else:
                        row += "".ljust(col_width)
            print(row)


class KarnaughMap:
    def __init__(self, truth_table_obj):
        self.tt = truth_table_obj
        self.variables = self.tt.variables
        self.table = self.tt.generate()
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
        kmap = [[0 for _ in range(len(col_gray))] for _ in range(len(row_gray))]
        for val_dict, r in self.table:
            bits = [val_dict[v] for v in self.variables]
            row = row_gray.index(tuple(bits[:row_vars]))
            col = col_gray.index(tuple(bits[row_vars:]))
            kmap[row][col] = r
        return kmap, row_gray, col_gray
    def is_valid_group(self, kmap, coords):
        return all(kmap[i][j] == 1 for i, j in coords)
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
    def minimize(self):
        groups, kmap = self.find_groups()
        kmap, row_gray, col_gray = self.build_map()

        print("\nКарта Карно:")
        self.print_map(kmap)

        print("\nГруппы Карно:")
        terms = []
        for g in groups:
            print(g)
            terms.append(self.group_to_term(g, row_gray, col_gray))
        return terms
    def print_map(self, kmap):
        for row in kmap:
            print(row)