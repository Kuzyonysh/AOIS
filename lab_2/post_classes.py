from zhegalkin import Zhegalkin
class PostClasses:
    def __init__(self, truth_table_obj):
        self.tt = truth_table_obj
        self.table = self.tt.generate()
        self.variables = self.tt.variables

    def is_T0(self):
        return self.table[0][1] == 0

    def is_T1(self):
        return self.table[-1][1] == 1

    def is_self_dual(self):
        n = len(self.table)
        for i in range(n):
            if self.table[i][1] == self.table[n - i - 1][1]:
                return False
        return True
    
    def is_monotonic(self):
        for i in range(len(self.table)):
            for j in range(len(self.table)):
                x1, f1 = self.table[i]
                x2, f2 = self.table[j]

                if all(x1[var] <= x2[var] for var in self.variables):
                    if f1 > f2:
                        return False
        return True

    def is_linear(self):
        zh = Zhegalkin(self.tt)
        poly = zh.build_polynomial()

        terms = poly.split(" + ")
        for term in terms:
            if len(term) > 1:
                return False
        return True

    def check_all(self):
        return {
            "T0": self.is_T0(),
            "T1": self.is_T1(),
            "S (самодвойственная)": self.is_self_dual(),
            "M (монотонная)": self.is_monotonic(),
            "L (линейная)": self.is_linear()
        }