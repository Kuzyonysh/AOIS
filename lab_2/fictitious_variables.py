class FictitiousVariables:
    def __init__(self, truth_table_obj):
        self.tt = truth_table_obj
        self.table = self.tt.generate()
        self.variables = self.tt.variables

    def find_fictitious(self):
        fictitious_vars = []

        for var in self.variables:
            is_fictitious = True

            for i in range(len(self.table)):
                for j in range(len(self.table)):
                    x1, f1 = self.table[i]
                    x2, f2 = self.table[j]

                    if all(
                        (x1[v] == x2[v]) for v in self.variables if v != var
                    ) and x1[var] != x2[var]:

                        if f1 != f2:
                            is_fictitious = False
                            break

                if not is_fictitious:
                    break

            if is_fictitious:
                fictitious_vars.append(var)

        return fictitious_vars