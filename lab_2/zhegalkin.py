class Zhegalkin:
    def __init__(self, truth_table_obj):
        self.tt = truth_table_obj
        self.table = self.tt.generate()
        self.variables = self.tt.variables

    
    def get_vector(self):
        return [result for _, result in self.table]
    
    def build_pascals_triangle(self):
        triangle = []
        row = self.get_vector()
        triangle.append(row)

        while len(row) > 1:
            new_row = []
            for i in range(len(row) - 1):
                new_row.append(row[i] ^ row[i + 1])
            triangle.append(new_row)
            row = new_row

        return triangle

    def get_coefficients(self):
        triangle = self.build_pascals_triangle()
        return [row[0] for row in triangle]

    def build_polynomial(self):
        coeffs = self.get_coefficients()
        terms = []

        n = len(self.variables)

        for i, coef in enumerate(coeffs):
            if coef == 1:
                if i == 0:
                    terms.append("1")
                else:
                    binary = format(i, f'0{n}b')
                    term = ""

                    for j, bit in enumerate(binary):
                        if bit == '1':
                            term += self.variables[j]

                    terms.append(term)

        return " + ".join(terms) if terms else "0"