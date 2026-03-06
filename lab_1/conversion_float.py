class FloatNumber:
    def __init__(self):
        pass

    @staticmethod
    def float_to_ieee(value):

        if value == 0:
            return [0] * 32

        sign_bit = 0

        if value < 0:
            sign_bit = 1
            value = -value

        integer_part = int(value)
        fractional_part = value - integer_part

        int_bits = []
        n = integer_part

        if n == 0:
            int_bits = [0]
        else:
            while n > 0:
                int_bits.insert(0, n % 2)
                n //= 2

        frac_bits = []
        frac = fractional_part

        for _ in range(30):

            frac *= 2

            if frac >= 1:
                frac_bits.append(1)
                frac -= 1
            else:
                frac_bits.append(0)

        if integer_part != 0:

            exponent = len(int_bits) - 1
            mantissa_bits = int_bits[1:] + frac_bits

        else:

            first_one = 0

            while frac_bits[first_one] == 0:
                first_one += 1

            exponent = -(first_one + 1)
            mantissa_bits = frac_bits[first_one + 1:]

        biased_exp = exponent + 127

        exp_bits = []
        rem = biased_exp

        for i in range(7, -1, -1):

            bit = rem // (2 ** i)
            exp_bits.append(bit)
            rem = rem % (2 ** i)

        mantissa_bits = mantissa_bits[:23]

        while len(mantissa_bits) < 23:
            mantissa_bits.append(0)

        return [sign_bit] + exp_bits + mantissa_bits

    @staticmethod
    def ieee_to_decimal(bits):

        sign = bits[0]
        exponent_bits = bits[1:9]

        exponent = 0
        power = 7

        for bit in exponent_bits:
            exponent += bit * (2 ** power)
            power -= 1

        mantissa_bits = bits[9:]

        mantissa = 1.0
        power = -1

        for bit in mantissa_bits:

            if bit == 1:
                mantissa += 2 ** power

            power -= 1

        real_exp = exponent - 127

        result = mantissa * (2 ** real_exp)

        if sign == 1:
            result = -result

        return result