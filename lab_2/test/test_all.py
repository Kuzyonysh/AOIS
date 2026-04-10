import pytest

from evaluator import BooleanFunction
from truth_table import TruthTable
from derivatives import BooleanDerivative
from fictitious_variables import FictitiousVariables
from minimization import CalculationMethod, KarnaughMap
from post_classes import PostClasses
from scnf_sdnf import NormalForms
from zhegalkin import Zhegalkin

@pytest.fixture
def tt():
    return TruthTable("a & b")

@pytest.fixture
def tt_expr():
    return TruthTable("(a & b) | (!a & b)")

@pytest.fixture
def tt_multivars():
    return TruthTable("a & b & c")

@pytest.fixture
def tt_sknf():
    return TruthTable("a | b")

def test_boolean_function_evaluate():
    bf = BooleanFunction("a & b")
    assert bf.evaluate({"a": True, "b": True}) is True
    assert bf.evaluate({"a": True, "b": False}) is False

def test_boolean_function_evaluate_implication():
    bf = BooleanFunction("a -> b")
    assert bf.evaluate({"a": True, "b": True}) is True
    assert bf.evaluate({"a": True, "b": False}) is False
    assert bf.evaluate({"a": False, "b": False}) is True

def test_boolean_function_evaluate_equivalence():
    bf = BooleanFunction("a ~ b")
    assert bf.evaluate({"a": True, "b": True}) is True
    assert bf.evaluate({"a": True, "b": False}) is False

def test_boolean_function_prepare():
    bf = BooleanFunction("a -> b")
    expr = bf.prepare_expression("a -> b")
    assert "not a or b" in expr

def test_extract_subexpressions():
    bf = BooleanFunction("(a & b) | (a | c)")
    subs = bf.extract_subexpressions()
    assert len(subs) >= 1

def test_get_variables():
    bf = BooleanFunction("a & b & c")
    vars = bf.get_variables()
    assert vars == ['a', 'b', 'c']

def test_truth_table_generate(tt):
    table = tt.generate()
    assert isinstance(table, list)
    assert len(table) == 4

def test_truth_table_print(tt):
    tt.print_table()

def test_truth_table_variables(tt):
    assert tt.variables == ['a', 'b']

def test_truth_table_steps(tt_expr):
    tt_expr.print_table_with_steps()

def test_truth_table_empty_subexpr():
    tt = TruthTable("a & b")
    bf = tt.bf
    bf.expr = "a&b"
    tt.print_table_with_steps()

def test_partial_derivative(tt):
    bd = BooleanDerivative(tt)
    vec = bd.partial_derivative("a")
    assert isinstance(vec, list)
    assert len(vec) == len(tt.generate())

def test_partial_with_formula(tt):
    bd = BooleanDerivative(tt)
    vector, formula = bd.partial_with_formula("a")
    assert isinstance(vector, list)
    assert isinstance(formula, str)

def test_vector_to_sdnf(tt):
    bd = BooleanDerivative(tt)
    vec = [0, 1, 0, 1]
    res = bd.vector_to_sdnf(vec)
    assert isinstance(res, str)

def test_mixed_derivative(tt):
    bd = BooleanDerivative(tt)
    vec, form = bd.mixed_derivative(["a", "b"])
    assert isinstance(vec, list)
    assert isinstance(form, str)

def test_fictitious(tt):
    fv = FictitiousVariables(tt)
    res = fv.find_fictitious()
    assert isinstance(res, list)

def test_fictitious_with_tautology():
    tt = TruthTable("a | !a")
    fv = FictitiousVariables(tt)
    res = fv.find_fictitious()
    assert isinstance(res, list)
def test_get_terms_dnf(tt):
    cm = CalculationMethod(tt, form="dnf")
    terms = cm.get_terms()
    assert isinstance(terms, list)

def test_get_terms_knf(tt_sknf):
    cm = CalculationMethod(tt_sknf, form="knf")
    terms = cm.get_terms()
    assert isinstance(terms, list)

def test_combine_dnf(tt):
    cm = CalculationMethod(tt, form="dnf")
    terms = cm.get_terms()
    if len(terms) > 1:
        combined = cm.combine_stage(terms)
        assert isinstance(combined, list)

def test_combine_knf(tt_sknf):
    cm = CalculationMethod(tt_sknf, form="knf")
    terms = cm.get_terms()
    if len(terms) > 1:
        combined = cm.combine_stage(terms)
        assert isinstance(combined, list)

def test_minimize_dnf(tt):
    cm = CalculationMethod(tt, form="dnf")
    res = cm.minimize()
    assert isinstance(res, list)

def test_minimize_knf(tt_sknf):
    cm = CalculationMethod(tt_sknf, form="knf")
    res = cm.minimize()
    assert isinstance(res, list)


def test_get_result_knf(tt_sknf):
    cm = CalculationMethod(tt_sknf, form="knf")
    result = cm.get_result()
    assert isinstance(result, str)

def test_term_to_str_dnf(tt):
    cm = CalculationMethod(tt, form="dnf")
    term = {"a": 1, "b": 0}
    result = cm.term_to_str(term)
    assert isinstance(result, str)

def test_term_to_str_knf(tt_sknf):
    cm = CalculationMethod(tt_sknf, form="knf")
    term = {"a": 1, "b": 0}
    result = cm.term_to_str(term)
    assert isinstance(result, str)

def test_can_combine(tt):
    cm = CalculationMethod(tt, form="dnf")
    t1 = {"a": 1, "b": 0}
    t2 = {"a": 1, "b": 1}
    result = cm.can_combine(t1, t2)
    assert result is not None

def test_covers(tt):
    cm = CalculationMethod(tt, form="dnf")
    term = {"a": 1, "b": "X"}
    val = {"a": 1, "b": 0}
    assert cm.covers(term, val) is True

def test_covers_x():
    cm = CalculationMethod(TruthTable("a & b"))
    fake_term = {"a": "X", "b": "X"}
    val = {"a": 0, "b": 1}
    cm.covers(fake_term, val)

def test_is_redundant_false():
    cm = CalculationMethod(TruthTable("a & b"))
    terms = cm.get_terms()
    if len(terms) > 0:
        cm.is_redundant(terms[0], terms)

def test_minimize_fixpoint():
    cm = CalculationMethod(TruthTable("a & b"))
    res = cm.minimize()
    assert isinstance(res, list)

def test_cover_table():
    cm = CalculationMethod(TruthTable("a & b"))
    cm.build_cover_table(cm.get_terms())

def test_cover_table_knf(tt_sknf):
    cm = CalculationMethod(tt_sknf, form="knf")
    terms = cm.get_terms()
    cm.build_cover_table(terms)

def test_is_redundant_true():
    cm = CalculationMethod(TruthTable("a & b | a & !b"))
    terms = cm.get_terms()
    if len(terms) > 1:
        cm.is_redundant(terms[0], terms)

def test_combine_all_paths():
    cm = CalculationMethod(TruthTable("(a & b) | (a & !b) | (!a & b)"))
    terms = cm.get_terms()
    cm.combine_stage(terms)

def test_get_target_value_dnf(tt):
    cm = CalculationMethod(tt, form="dnf")
    assert cm.get_target_value() == 1

def test_get_target_value_knf(tt_sknf):
    cm = CalculationMethod(tt_sknf, form="knf")
    assert cm.get_target_value() == 0

def test_remove_redundant(tt):
    cm = CalculationMethod(tt, form="dnf")
    terms = cm.get_terms()
    result = cm.remove_redundant(terms)
    assert isinstance(result, list)

def test_post_classes(tt):
    pc = PostClasses(tt)
    res = pc.check_all()
    assert isinstance(res, dict)
    assert "T0" in res

def test_normal_forms(tt_expr):
    nf = NormalForms(tt_expr)
    sdnf = nf.build_sdnf()
    sknf = nf.build_sknf()
    assert isinstance(sdnf, str)
    assert isinstance(sknf, str)

def test_numeric_forms(tt_expr):
    nf = NormalForms(tt_expr)
    assert isinstance(nf.sdnf_numeric(), str)
    assert isinstance(nf.sknf_numeric(), str)
    assert isinstance(nf.index_form(), str)

def test_build_sdnf(tt):
    nf = NormalForms(tt)
    sdnf = nf.build_sdnf()
    assert isinstance(sdnf, str)

def test_build_sknf(tt):
    nf = NormalForms(tt)
    sknf = nf.build_sknf()
    assert isinstance(sknf, str)

def test_zhegalkin(tt_expr):
    zh = Zhegalkin(tt_expr)
    vector = zh.get_vector()
    coeffs = zh.get_coefficients()
    poly = zh.build_polynomial()
    assert isinstance(vector, list)
    assert isinstance(coeffs, list)
    assert isinstance(poly, str)

def test_zhegalkin_get_vector(tt):
    zh = Zhegalkin(tt)
    vector = zh.get_vector()
    assert isinstance(vector, list)

def test_zhegalkin_get_coefficients(tt):
    zh = Zhegalkin(tt)
    coeffs = zh.get_coefficients()
    assert isinstance(coeffs, list)

def test_regex_branches():
    bf = BooleanFunction("a -> b ~ c")
    assert bf.replace_implication("a -> b")
    assert bf.replace_equivalence("a ~ b")

def test_extract_loop():
    bf = BooleanFunction("((a))")
    res = bf.extract_subexpressions()
    assert isinstance(res, list)

def test_evaluate_with_steps():
    bf = BooleanFunction("a & b")
    steps = bf.evaluate_with_steps({"a": True, "b": True})
    assert isinstance(steps, dict)

def test_truth_table_multivars(tt_multivars):
    table = tt_multivars.generate()
    assert len(table) == 8
def test_simplify_partial_derivative():
    tt = TruthTable("a & b")
    bd = BooleanDerivative(tt)
    
    simplified = bd.simplify_derivative(var="a")
    assert simplified == "(!b)" or simplified == "(b)"  
    simplified = bd.simplify_derivative(var="b")
    assert "a" in simplified or "!a" in simplified
def test_karnaugh_gray_code():
    cm = KarnaughMap(TruthTable("a & b"))
    assert cm.gray_code(0) == [()]
    assert len(cm.gray_code(2)) == 4


def test_karnaugh_build_map_shape():
    cm = KarnaughMap(TruthTable("a & b"))

    kmap, row_gray, col_gray = cm.build_map()

    assert isinstance(kmap, list)
    assert len(kmap) > 0
    assert len(kmap[0]) > 0
    assert isinstance(row_gray, list)
    assert isinstance(col_gray, list)


def test_karnaugh_get_minterms():
    cm = KarnaughMap(TruthTable("a & b"))

    kmap, _, _ = cm.build_map()
    mins = cm.get_minterms(kmap)

    assert isinstance(mins, list)


def test_karnaugh_cell_to_bits():
    cm = KarnaughMap(TruthTable("a & b"))

    row_gray = cm.gray_code(1)
    col_gray = cm.gray_code(1)

    bits = cm.cell_to_bits(0, 0, row_gray, col_gray)

    assert isinstance(bits, tuple)


def test_karnaugh_combine_success():
    cm = KarnaughMap(TruthTable("a & b"))

    a = ("0", "1")
    b = ("0", "0")

    res = cm.combine(a, b)

    assert res is not None
    assert "X" in res


def test_karnaugh_combine_fail():
    cm = KarnaughMap(TruthTable("a & b"))

    a = ("0", "1")
    b = ("1", "0")

    assert cm.combine(a, b) is None


def test_karnaugh_build_implicants():
    cm = KarnaughMap(TruthTable("a & b"))

    minterms = [("0", "1"), ("0", "0")]
    primes = cm.build_implicants(minterms)

    assert isinstance(primes, list)


def test_karnaugh_minimize_runs():
    cm = KarnaughMap(TruthTable("a & b"))

    result = cm.minimize()

    assert isinstance(result, list)


def test_karnaugh_minimize_complex():
    cm = KarnaughMap(TruthTable("(a & b) | (!a & b) | (a & !b)"))

    result = cm.minimize()

    assert isinstance(result, list)


def test_karnaugh_single_variable():
    cm = KarnaughMap(TruthTable("a"))

    result = cm.minimize()

    assert isinstance(result, list)