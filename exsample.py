def binary_straight_to_decimal(bits):

    sign = bits[0]
    value = 0
    power = 0
    for i in range(31, 0, -1):
        value += bits[i] * (2**power)
        power += 1

    if sign == 1:
        value = -value
    return value


def binary_inverse_to_decimal(bits):
    if bits[0] == 0:
        return binary_straight_to_decimal(bits)
    temp = [0] * 32
    temp[0] = 0
    i = 1
    while i < 32:
        if bits[i] == 0:
            temp[i] = 1
        else:
            temp[i] = 0
        i = i + 1

    result = binary_straight_to_decimal(temp)
    return -result


def compare_bits(a, b):
    for i in range(len(a)):
        if a[i] > b[i]:
            return 1
        elif a[i] < b[i]:
            return -1
    return 0


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


def shift_left(bits):
    n = len(bits)
    for i in range(n - 1):
        bits[i] = bits[i + 1]
    bits[n - 1] = 0


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


def division_in_straight(a, b, precision=5):
    if b == 0:
        print("Ошибка: деление на ноль")
        return None

    bits_a = conversion_to_binary_straight(a)
    bits_b = conversion_to_binary_straight(b)

    sign_result = 0 if bits_a[0] == bits_b[0] else 1

    mod_a = bits_a[1:]
    mod_b = bits_b[1:]

    dividend = mod_a + [0] * precision
    divisor = mod_b[:]

    quotient = [0] * (31 + precision)
    remainder = [0] * len(divisor)

    for i in range(31 + precision):
        shift_left(remainder)
        remainder[-1] = dividend[i]
        if compare_bits(remainder, divisor) >= 0:
            remainder = subtract_bits(remainder, divisor)
            quotient[i] = 1
        else:
            quotient[i] = 0
    result_bits = [0] * 32
    result_bits[0] = sign_result
    for i in range(1, 32):
        if i - 1 < 31:
            result_bits[i] = quotient[i - 1]
        else:
            result_bits[i] = 0
    integer_part_bits = [0] + quotient[:31]  
    fractional_part_bits = [0] * (32 - precision) + quotient[
        31 : 31 + precision
    ] 
    integer_part = binary_straight_to_decimal(integer_part_bits)
    fractional_part = binary_straight_to_decimal(fractional_part_bits) / (2**precision)
    decimal_result = integer_part + fractional_part
    if sign_result == 1:
        decimal_result = -decimal_result

    return result_bits, decimal_result
def conversion_to_binary_inversion(n):
    bits = conversion_to_binary_straight(abs(n))
    if n > 0:
        return bits
    else:
        for i in range(32):
            bits[i] = 1 - bits[i]
        return bits

def conversion_to_binary_additional(n):
    if n > 0:
        return conversion_to_binary_straight(abs(n))
    bits = conversion_to_binary_inversion(n)
    carry = 1
    for i in range(31, -1, -1):
        s = bits[i] + carry
        bits[i] = s % 2
        carry = s // 2
    return bits
def binary_additional_to_decimal(bits):
    if bits[0]==0:
        return binary_straight_to_decimal(bits)
    else:
        temp=[0]*32
        i=0
        while i<32:
            temp[i]=bits[i]
            i+=1
        i=31
        while i>=0:
            if temp[i]==1:
                temp[i]=0
                break
            else:
                temp[i]=1
                i-=1
        i = 1
        while i < 32:
            if temp[i] == 0:
                temp[i] = 1
            else:
                temp[i] = 0
            i += 1

        temp[0] = 0
        result = binary_straight_to_decimal(temp)
        return -result
def sum_in_additional(a, b):
    bits_a = conversion_to_binary_additional(a)
    bits_b = conversion_to_binary_additional(b)
    print(f"A = {a} в доп. коде: {bits_a}")
    print(f"B = {b} в доп. коде: {bits_b}")

    result = [0] * 32
    carry = 0
    for i in range(31, -1, -1):
        sum_bits = bits_a[i] + bits_b[i] + carry
        result[i] = sum_bits % 2
        carry = sum_bits // 2
    overflow = False
    if bits_a[0] == bits_b[0]:  
        if result[0] != bits_a[0]:  
            overflow = True
    
    if overflow:
        print("Переполнение")
        return None
    else:
        result1=binary_additional_to_decimal(result)
        return result,result1
a = sum_in_additional(-15,-3)

print(a)
