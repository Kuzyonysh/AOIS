class IntegerNumber:
    def __init__(self):
        pass

    @staticmethod
    def conversion_to_binary_straight(n):
        bits = [0] * 32

        if n < 0:
            bits[0] = 1
            n = -n
        else:
            bits[0] = 0

        i = 31
        while n != 0:
            bits[i] = n % 2
            i -= 1
            n //= 2

        return bits

    @staticmethod
    def conversion_to_binary_inversion(n):
        bits = IntegerNumber.conversion_to_binary_straight(abs(n))

        if n >= 0:
            return bits

        for i in range(32):
            bits[i] = 1 - bits[i]

        return bits

    @staticmethod
    def conversion_to_binary_additional(n):

        if n >= 0:
            return IntegerNumber.conversion_to_binary_straight(n)

        bits = IntegerNumber.conversion_to_binary_inversion(n)

        carry = 1

        for i in range(31, -1, -1):
            s = bits[i] + carry
            bits[i] = s % 2
            carry = s // 2

        return bits
    @staticmethod
    def negate_additional(bits):

        neg = bits.copy()

        for i in range(32):
            neg[i] = 1 - neg[i]

        carry = 1

        for i in range(31, -1, -1):
            s = neg[i] + carry
            neg[i] = s % 2
            carry = s // 2

        return neg

    @staticmethod
    def binary_straight_to_decimal(bits):

        sign = bits[0]
        value = 0

        power = 0

        for i in range(31, 0, -1):
            value += bits[i] * (2 ** power)
            power += 1

        if sign == 1:
            value = -value

        return value

    @staticmethod
    def binary_inverse_to_decimal(bits):

        if bits[0] == 0:
            return IntegerNumber.binary_straight_to_decimal(bits)

        temp = [0] * 32
        temp[0] = 0

        for i in range(1, 32):
            temp[i] = 1 - bits[i]

        result = IntegerNumber.binary_straight_to_decimal(temp)

        return -result

    @staticmethod
    def binary_additional_to_decimal(bits):

        if bits[0] == 0:
            return IntegerNumber.binary_straight_to_decimal(bits)

        temp = bits.copy()

        i = 31

        while i >= 0:
            if temp[i] == 1:
                temp[i] = 0
                break
            else:
                temp[i] = 1
            i -= 1

        for i in range(1, 32):
            temp[i] = 1 - temp[i]

        temp[0] = 0

        result = IntegerNumber.binary_straight_to_decimal(temp)

        return -result
