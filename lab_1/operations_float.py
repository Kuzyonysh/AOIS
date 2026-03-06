from conversion_float import FloatNumber

class FloatOperations:
    @staticmethod
    def sum_to_binary_float(a, b):
        bits_a = FloatNumber.float_to_ieee(a)
        bits_b = FloatNumber.float_to_ieee(b)

        sign1 = bits_a[0]
        sign2 = bits_b[0]

        exp1 = sum(bits_a[i] * (2 ** (7 - (i - 1))) for i in range(1, 9)) - 127
        exp2 = sum(bits_b[i] * (2 ** (7 - (i - 1))) for i in range(1, 9)) - 127

        mant1 = [1] + bits_a[9:]
        mant2 = [1] + bits_b[9:]

        while exp1 > exp2:
            mant2.insert(0, 0)
            mant2.pop()
            exp2 += 1
        while exp2 > exp1:
            mant1.insert(0, 0)
            mant1.pop()
            exp1 += 1

        result_exp = exp1

        if sign1 == sign2:
            result_mant = [0] * len(mant1)
            carry = 0
            for i in range(len(mant1)-1, -1, -1):
                total = mant1[i] + mant2[i] + carry
                result_mant[i] = total % 2
                carry = total // 2
            if carry == 1:
                result_mant.insert(0, 1)
                result_mant.pop()
                result_exp += 1
            result_sign = sign1
        else:
            if mant1 > mant2:
                big, small = mant1, mant2
                result_sign = sign1
            else:
                big, small = mant2, mant1
                result_sign = sign2

            result_mant = [0] * len(big)
            borrow = 0
            for i in range(len(big)-1, -1, -1):
                diff = big[i] - small[i] - borrow
                if diff < 0:
                    result_mant[i] = diff + 2
                    borrow = 1
                else:
                    result_mant[i] = diff
                    borrow = 0
            while result_mant[0] == 0 and result_exp > -126:
                result_mant.pop(0)
                result_mant.append(0)
                result_exp -= 1

        result_mant = result_mant[1:]
        biased_exp = result_exp + 127

        exp_bits = [(biased_exp >> i) & 1 for i in range(7, -1, -1)]

        result = [result_sign] + exp_bits + result_mant
        result_decimal = FloatNumber.ieee_to_decimal(result)

        return result, result_decimal

    @staticmethod
    def subtract_binary_float(a, b):
        return FloatOperations.sum_to_binary_float(a, -b)

    @staticmethod
    def multiply_binary_float(a, b):
        bits_a = FloatNumber.float_to_ieee(a)
        bits_b = FloatNumber.float_to_ieee(b)

        sign_result = bits_a[0] ^ bits_b[0]

        exp_a = sum(bits_a[i] * (2 ** (7 - (i - 1))) for i in range(1, 9)) - 127
        exp_b = sum(bits_b[i] * (2 ** (7 - (i - 1))) for i in range(1, 9)) - 127
        exp_result = exp_a + exp_b

        mant_a = [1] + bits_a[9:]
        mant_b = [1] + bits_b[9:]

        n = 24
        result_mant = [0] * (2 * n)
        for i in range(n-1, -1, -1):
            if mant_b[i] == 1:
                carry = 0
                for j in range(n-1, -1, -1):
                    total = result_mant[i+j+1] + mant_a[j] + carry
                    result_mant[i+j+1] = total % 2
                    carry = total // 2
                result_mant[i] += carry

        if result_mant[0] == 1:
            exp_result += 1
            mant_final = result_mant[1:24]
        else:
            mant_final = result_mant[2:25]

        biased_exp = exp_result + 127
        exp_bits = [(biased_exp >> i) & 1 for i in range(7, -1, -1)]

        ieee_result = [sign_result] + exp_bits + mant_final
        result_decimal = FloatNumber.ieee_to_decimal(ieee_result)

        return ieee_result, result_decimal

    @staticmethod
    def division_ieee(a, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        if a == 0:
            return [0] * 32, 0.0

        bits_a = FloatNumber.float_to_ieee(a)
        bits_b = FloatNumber.float_to_ieee(b)
        sign = bits_a[0] ^ bits_b[0]

        exp_a = sum(bits_a[i] * (2 ** (7 - (i - 1))) for i in range(1, 9))
        exp_b = sum(bits_b[i] * (2 ** (7 - (i - 1))) for i in range(1, 9))
        exp_res = exp_a - exp_b + 127

        mA = 1 << 23
        for i in range(23):
            mA |= bits_a[9+i] << (22 - i)

        mB = 1 << 23
        for i in range(23):
            mB |= bits_b[9+i] << (22 - i)

        mant_int = (mA << 23) // mB
        shift = 0
        if mant_int >= (1 << 24):
            mant_int >>= 1
            shift = 1
        elif mant_int < (1 << 23):
            while mant_int < (1 << 23):
                mant_int <<= 1
                shift -= 1
        exp_res += shift

        if exp_res <= 0:
            return [0] * 32, 0.0
        if exp_res >= 255:
            return [sign] + [1]*8 + [0]*23, float("inf") if sign == 0 else float("-inf")

        mant_bits = [(mant_int >> (22 - i)) & 1 for i in range(23)]
        exp_bits = [(exp_res >> (7 - i)) & 1 for i in range(8)]
        ieee_result = [sign] + exp_bits + mant_bits
        dec_result = FloatNumber.ieee_to_decimal(ieee_result)

        return ieee_result, dec_result