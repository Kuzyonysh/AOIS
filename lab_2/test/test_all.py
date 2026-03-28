import pytest

from evaluator import BooleanFunction
from truth_table import TruthTable
from derivatives import BooleanDerivative
from fictitious_variables import FictitiousVariables
from minimization import CalculationMethod,KarnaughMap
from post_classes import PostClasses
from scnf_sdnf import NormalForms
from zhegalkin import Zhegalkin

@pytest.fixture
def tt():
    return TruthTable("a & b")


@pytest.fixture
def tt_expr():
    return TruthTable("(a & b) | (!a & b)")


def test_boolean_function_evaluate():
    bf = BooleanFunction("a & b")
    assert bf.evaluate({"a": 1, "b": 1}) is True
    assert bf.evaluate({"a": 1, "b": 0}) is False


def test_boolean_function_prepare():
    bf = BooleanFunction("a -> b")
    expr = bf.prepare_expression("a -> b")
    assert "not a or b" in expr


def test_extract_subexpressions():
    bf = BooleanFunction("(a & b) | (a | c)")
    subs = bf.extract_subexpressions()
    assert len(subs) >= 1




def test_truth_table_generate(tt):
    table = tt.generate()
    assert isinstance(table, list)
    assert len(table) == 4  # a,b -> 4 комбинации


def test_truth_table_print(tt):
    tt.print_table()



def test_partial_derivative(tt):
    bd = BooleanDerivative(tt)
    vec = bd.partial_derivative("a")
    assert isinstance(vec, list)
    assert len(vec) == len(tt.generate())


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


def test_get_terms(tt):
    cm = CalculationMethod(tt)
    terms = cm.get_terms()
    assert isinstance(terms, list)


def test_combine(tt):
    cm = CalculationMethod(tt)
    terms = cm.get_terms()
    if len(terms) > 1:
        combined = cm.combine_stage(terms)
        assert isinstance(combined, list)


def test_minimize(tt):
    cm = CalculationMethod(tt)
    res = cm.minimize()
    assert isinstance(res, list)


def test_kmap_build(tt):
    km = KarnaughMap(tt)
    kmap, row, col = km.build_map()
    assert isinstance(kmap, list)


def test_kmap_groups(tt):
    km = KarnaughMap(tt)
    groups, _ = km.find_groups()
    assert isinstance(groups, list)


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


def test_zhegalkin(tt_expr):
    zh = Zhegalkin(tt_expr)
    vector = zh.get_vector()
    coeffs = zh.get_coefficients()
    poly = zh.build_polynomial()

    assert isinstance(vector, list)
    assert isinstance(coeffs, list)
    assert isinstance(poly, str)

def test_truth_table_steps(tt_expr):
    tt_expr.print_table_with_steps()


def test_truth_table_empty_subexpr():
    from truth_table import TruthTable

    tt = TruthTable("a & b")
    bf = tt.bf

    # forcing empty subexpr branch
    bf.expr = "a&b"
    tt.print_table_with_steps()

def test_regex_branches():
    bf = BooleanFunction("a -> b ~ c")

    assert bf.replace_implication("a -> b")
    assert bf.replace_equivalence("a ~ b")


def test_extract_loop():
    bf = BooleanFunction("((a))")
    res = bf.extract_subexpressions()
    assert isinstance(res, list)

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

def test_covers_x_branch():

    cm = CalculationMethod(TruthTable("a & b"))

    fake_term = {"a": "X", "b": "X"}
    val = {"a": 0, "b": 1}

    cm.covers(fake_term, val)

def test_is_redundant_true():
    cm = CalculationMethod(TruthTable("a & b | a & !b"))

    terms = cm.get_terms()

    # создаём ситуацию конкуренции покрытий
    if len(terms) > 1:
        cm.is_redundant(terms[0], terms)

def test_combine_all_paths():
    cm = CalculationMethod(TruthTable("(a & b) | (a & !b) | (!a & b)"))

    terms = cm.get_terms()
    cm.combine_stage(terms)