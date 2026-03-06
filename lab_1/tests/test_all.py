import pytest

from conversion_int import IntegerNumber
from conversion_float import FloatNumber
from operations_integer import IntegerOperations
from operations_float import FloatOperations
from Excess3 import Excess3Calculator
from utils import BinaryUtils
from classBinary import Binary32


def test_binary32_default():
    b = Binary32()
    assert len(b.bits) == 32
    assert all(bit == 0 for bit in b.bits)


def test_binary32_custom_bits():
    bits = [1] * 32
    b = Binary32(bits)
    assert b.bits == bits


def test_integer_sum_negative():
    result, dec = IntegerOperations.sum_in_additional(-5, -3)
    assert dec == -8


def test_integer_subtraction_negative():
    result, dec = IntegerOperations.subtraction_in_additional(-10, -5)
    assert dec == -5


def test_integer_division_fraction():
    result, dec = IntegerOperations.division_in_straight(7, 2)
    assert dec == pytest.approx(3.5, rel=1e-1)


def test_float_sum_negative():
    bits, result = FloatOperations.sum_to_binary_float(-4.5, -1.5)
    assert result == pytest.approx(-6.0)


def test_float_multiply_negative():
    bits, result = FloatOperations.multiply_binary_float(-3.0, 2.0)
    assert result == pytest.approx(-6.0)


def test_float_division_negative():
    bits, result = FloatOperations.division_ieee(-6.0, 2.0)
    assert result == pytest.approx(-3.0)


def test_excess3_zero():
    code = Excess3Calculator.number_to_excess3(0)
    number = Excess3Calculator.excess3_to_number(code)
    assert number == 0


def test_compare_bits_equal():
    a = [1, 0, 1]
    b = [1, 0, 1]
    assert BinaryUtils.compare_bits(a, b) == 0


def test_straight_binary_positive():
    bits = IntegerNumber.conversion_to_binary_straight(5)
    assert IntegerNumber.binary_straight_to_decimal(bits) == 5


def test_straight_binary_negative():
    bits = IntegerNumber.conversion_to_binary_straight(-7)
    assert IntegerNumber.binary_straight_to_decimal(bits) == -7


def test_inverse_code():
    bits = IntegerNumber.conversion_to_binary_inversion(-5)
    assert IntegerNumber.binary_inverse_to_decimal(bits) == -5


def test_additional_code():
    bits = IntegerNumber.conversion_to_binary_additional(-9)
    assert IntegerNumber.binary_additional_to_decimal(bits) == -9


def test_negate_additional():
    bits = IntegerNumber.conversion_to_binary_additional(6)
    neg = IntegerNumber.negate_additional(bits)
    assert IntegerNumber.binary_additional_to_decimal(neg) == -6


def test_integer_sum():
    result, dec = IntegerOperations.sum_in_additional(5, 3)
    assert dec == 8


def test_integer_subtraction():
    result, dec = IntegerOperations.subtraction_in_additional(10, 3)
    assert dec == 7


def test_integer_multiplication():
    result, dec = IntegerOperations.multiplication_in_straight(4, 3)
    assert dec == 12


def test_integer_division():
    result, dec = IntegerOperations.division_in_straight(10, 2)
    assert dec == pytest.approx(5)


def test_float_to_ieee_and_back():
    value = 5.5
    bits = FloatNumber.float_to_ieee(value)
    result = FloatNumber.ieee_to_decimal(bits)
    assert result == pytest.approx(value)


def test_float_zero():
    bits = FloatNumber.float_to_ieee(0)
    assert bits == [0] * 32


def test_float_negative():
    value = -3.25
    bits = FloatNumber.float_to_ieee(value)
    result = FloatNumber.ieee_to_decimal(bits)
    assert result == pytest.approx(value)


def test_float_sum():
    bits, result = FloatOperations.sum_to_binary_float(5.5, 2.25)
    assert result == pytest.approx(7.75)


def test_float_subtract():
    bits, result = FloatOperations.subtract_binary_float(5.5, 2.5)
    assert result == pytest.approx(3.0)


def test_float_multiply():
    bits, result = FloatOperations.multiply_binary_float(3.0, 2.0)
    assert result == pytest.approx(6.0)


def test_float_division():
    bits, result = FloatOperations.division_ieee(6.0, 2.0)
    assert result == pytest.approx(3.0)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        FloatOperations.division_ieee(5, 0)


def test_digit_to_excess3():
    tetrad = Excess3Calculator.digit_to_excess3(5)
    digit = Excess3Calculator.excess3_to_digit(tetrad)
    assert digit == 5


def test_number_to_excess3():
    code = Excess3Calculator.number_to_excess3(123)
    number = Excess3Calculator.excess3_to_number(code)
    assert number == 123


def test_excess3_sum():
    result, number = Excess3Calculator.excess3_sum(25, 37)
    assert number == 62


def test_compare_bits():
    a = [0, 1, 0, 1]
    b = [0, 0, 1, 1]
    assert BinaryUtils.compare_bits(a, b) == 1


def test_subtract_bits():
    a = [1, 0, 0, 0]
    b = [0, 1, 0, 0]
    result = BinaryUtils.subtract_bits(a, b)
    assert result == [0, 1, 0, 0]


def test_shift_left():
    bits = [1, 0, 1, 1]
    BinaryUtils.shift_left(bits)
    assert bits == [0, 1, 1, 0]
