from conversion_int import IntegerNumber
from utils import BinaryUtils  


class IntegerOperations:
    @staticmethod
    def sum_in_additional(a, b):
        bits_a = IntegerNumber.conversion_to_binary_additional(a)
        bits_b = IntegerNumber.conversion_to_binary_additional(b)

        print(f"A = {a} в доп. коде: {bits_a}")
        print(f"B = {b} в доп. коде: {bits_b}")

        result = [0] * 32
        carry = 0

        for i in range(31, -1, -1):
            sum_bits = bits_a[i] + bits_b[i] + carry
            result[i] = sum_bits % 2
            carry = sum_bits // 2

        overflow = False
        if bits_a[0] == bits_b[0] and result[0] != bits_a[0]:
            overflow = True

        if overflow:
            print("Переполнение")
            return None
        result_decimal = IntegerNumber.binary_additional_to_decimal(result)
        return result, result_decimal

    @staticmethod
    def subtraction_in_additional(a, b):
        bits_a = IntegerNumber.conversion_to_binary_additional(a)
        bits_b = IntegerNumber.conversion_to_binary_additional(b)
        neg_b = IntegerNumber.negate_additional(bits_b)

        print(f"A = {a} в доп. коде: {bits_a}")
        print(f"B = {b} в доп. коде: {bits_b}")

        result = [0] * 32
        carry = 0
        for i in range(31, -1, -1):
            s = bits_a[i] + neg_b[i] + carry
            result[i] = s % 2
            carry = s // 2

        overflow = False
        if bits_a[0] == bits_b[0] and result[0] != bits_a[0]:
            overflow = True

        if overflow:
            print("Переполнение")
            return None
        result_decimal = IntegerNumber.binary_additional_to_decimal(result)
        return result, result_decimal

    @staticmethod
    def multiplication_in_straight(a, b):
        bits_a = IntegerNumber.conversion_to_binary_straight(a)
        bits_b = IntegerNumber.conversion_to_binary_straight(b)

        print(f"A = {a} в прямом коде: {bits_a}")
        print(f"B = {b} в прямом коде: {bits_b}")

        result_sign = 0 if bits_a[0] == bits_b[0] else 1
        mod_a = bits_a[1:]
        mod_b = bits_b[1:]

        result_mod = [0] * 62
        for i in range(31):
            if mod_b[30 - i] == 1:
                carry = 0
                for j in range(31):
                    total = result_mod[i + j] + mod_a[30 - j] + carry
                    result_mod[i + j] = total % 2
                    carry = total // 2
                k = i + 31
                while carry == 1:
                    total = result_mod[k] + carry
                    result_mod[k] = total % 2
                    carry = total // 2
                    k += 1

        overflow = any(result_mod[31:62])
        if overflow:
            print("Переполнение")
            return None

        result = [0] * 32
        result[0] = result_sign
        for i in range(31):
            result[31 - i] = result_mod[i]

        result_decimal = IntegerNumber.binary_straight_to_decimal(result)
        return result, result_decimal

    @staticmethod
    def division_in_straight(a, b, precision=5):
        if b == 0:
            print("Ошибка: деление на ноль")
            return None

        bits_a = IntegerNumber.conversion_to_binary_straight(a)
        bits_b = IntegerNumber.conversion_to_binary_straight(b)

        sign_result = 0 if bits_a[0] == bits_b[0] else 1
        mod_a = bits_a[1:]
        mod_b = bits_b[1:]

        dividend = mod_a + [0] * precision
        divisor = mod_b[:]

        quotient = [0] * (31 + precision)
        remainder = [0] * len(divisor)

        for i in range(31 + precision):
            BinaryUtils.shift_left(remainder)
            remainder[-1] = dividend[i]
            if BinaryUtils.compare_bits(remainder, divisor) >= 0:
                remainder = BinaryUtils.subtract_bits(remainder, divisor)
                quotient[i] = 1
            else:
                quotient[i] = 0

        result_bits = [0] * 32
        result_bits[0] = sign_result
        for i in range(1, 32):
            result_bits[i] = quotient[i - 1] if i - 1 < 31 else 0

        integer_part_bits = [0] + quotient[:31]
        fractional_part_bits = [0] * (32 - precision) + quotient[31:31 + precision]

        integer_part = IntegerNumber.binary_straight_to_decimal(integer_part_bits)
        fractional_part = IntegerNumber.binary_straight_to_decimal(fractional_part_bits) / (2 ** precision)

        decimal_result = integer_part + fractional_part
        if sign_result == 1:
            decimal_result = -decimal_result

        return result_bits, decimal_result