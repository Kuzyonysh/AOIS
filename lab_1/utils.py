class BinaryUtils:

    @staticmethod
    def compare_bits(a, b):

        for i in range(len(a)):
            if a[i] > b[i]:
                return 1
            elif a[i] < b[i]:
                return -1

        return 0

    @staticmethod
    def subtract_bits(a, b):

        n = len(a)

        result = [0] * n

        borrow = 0

        for i in range(n - 1, -1, -1):

            diff = a[i] - b[i] - borrow

            if diff < 0:
                diff += 2
                borrow = 1
            else:
                borrow = 0

            result[i] = diff

        return result

    @staticmethod
    def shift_left(bits):

        n = len(bits)

        for i in range(n - 1):
            bits[i] = bits[i + 1]

        bits[n - 1] = 0