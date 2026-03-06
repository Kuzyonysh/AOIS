class Excess3Calculator:
    def __init__(self):
        pass

    @staticmethod
    def digit_to_bits(digit):
        bits = [0] * 4
        i = 3
        n = digit
        while n > 0:
            bits[i] = n % 2
            n //= 2
            i -= 1
        return bits

    @staticmethod
    def digit_to_excess3(digit):
        return Excess3Calculator.digit_to_bits(digit + 3)

    @staticmethod
    def number_to_excess3(n):
        digits = str(n)
        result = []
        for d in digits:
            result.append(Excess3Calculator.digit_to_excess3(int(d)))
        return result

    @staticmethod
    def bits_to_digit(bits):
        val = 0
        for bit in bits:
            val = val * 2 + bit
        return val

    @staticmethod
    def excess3_to_digit(tetrad):
        val = Excess3Calculator.bits_to_digit(tetrad)
        return val - 3

    @staticmethod
    def excess3_to_number(excess3_list):
        result = 0
        for tetrad in excess3_list:
            result = result * 10 + Excess3Calculator.excess3_to_digit(tetrad)
        return result

    @staticmethod
    def add_tetrads_bits(a, b, carry_in):
        result = [0] * 4
        carry = carry_in

        for i in range(3, -1, -1):
            s = a[i] + b[i] + carry
            result[i] = s % 2
            carry = s // 2

        val = 0
        for i in range(4):
            val = val * 2 + result[i]

        if carry == 1:
            correction = [0, 0, 1, 1]  
        else:
            correction = [1, 1, 0, 1]  

        carry2 = 0
        for i in range(3, -1, -1):
            s = result[i] + correction[i] + carry2
            result[i] = s % 2
            carry2 = s // 2

        return result, carry

    @staticmethod
    def excess3_sum(a, b):
        A = Excess3Calculator.number_to_excess3(a)
        B = Excess3Calculator.number_to_excess3(b)

        while len(A) < len(B):
            A.insert(0, Excess3Calculator.digit_to_excess3(0))
        while len(B) < len(A):
            B.insert(0, Excess3Calculator.digit_to_excess3(0))

        A.reverse()
        B.reverse()

        result = []
        carry = 0
        for i in range(len(A)):
            temp, carry = Excess3Calculator.add_tetrads_bits(A[i], B[i], carry)
            result.append(temp)

        if carry == 1:
            result.append(Excess3Calculator.digit_to_excess3(1))

        result.reverse()
        result_number = Excess3Calculator.excess3_to_number(result)
        return result, result_number