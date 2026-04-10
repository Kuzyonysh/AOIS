import pytest

from HashUtils import HashUtils
from Node import Node
from HashTable import HashTable
from TablePrinter import TablePrinter
from exception import KeyExistsError,  KeyNotFoundError



def test_get_value():
    utils = HashUtils(20)
    assert utils.get_vlue("КУ") == utils.alphabet['К'] * 33 + utils.alphabet['У']


def test_hash_range():
    utils = HashUtils(20)
    h = utils.hash("КУ")
    assert 0 <= h < 20


def test_probe():
    utils = HashUtils(20)
    base = 5
    assert utils.probe(base, 0) == 5
    assert utils.probe(base, 1) == 6
    assert utils.probe(base, 19) == (5 + 19) % 20


def test_node_creation():
    node = Node("Кузьмич", "матем")
    assert node.key == "Кузьмич"
    assert node.value == "матем"
    assert node.C == 0
    assert node.U == 1
    assert node.D == 0


def test_node_deleted_property():
    node = Node("Кузьмич", "матем")
    assert node.deleted is False

    node.D = 1
    assert node.deleted is True


def test_print_table(capsys):
    ht = HashTable(10)
    printer = TablePrinter()

    ht.insert("Кузьмич", "матем")

    printer.print_table(ht)

    captured = capsys.readouterr()
    assert "Кузьмич" in captured.out
    assert "матем" in captured.out


def test_insert_and_get():
    ht = HashTable(10)
    ht.insert("Кузнецов", "матем")

    assert ht.get("Кузнецов") == "матем"


def test_duplicate_key():
    ht = HashTable(10)
    ht.insert("Кузнецов", "матем")

    with pytest.raises(KeyExistsError):
        ht.insert("Кузнецов", "физика")


def test_update():
    ht = HashTable(10)
    ht.insert("Кузнецов", "матем")

    ht.update("Кузнецов", "физика")
    assert ht.get("Кузнецов") == "физика"


def test_update_not_found():
    ht = HashTable(10)

    with pytest.raises(KeyNotFoundError):
        ht.update("Кузнецов", "матем")


def test_delete():
    ht = HashTable(10)
    ht.insert("Кузнецов", "матем")

    ht.delete("Кузнецов")
    assert ht.get("Кузнецов") is None


def test_delete_not_found():
    ht = HashTable(10)

    with pytest.raises(KeyNotFoundError):
        ht.delete("Кузнецов")


def test_load_factor():
    ht = HashTable(10)

    ht.insert("Кузнецов", "матем")
    ht.insert("Кузьмич", "физика")

    assert ht.load_factor() == 2 / 10


def test_collision():
    ht = HashTable(20)

    # одинаковые первые буквы → одинаковый V → коллизия
    ht.insert("Кузнецов", "матем")
    ht.insert("Кузьмич", "физика")

    values = [x for x in ht.table if x is not None]

    assert any(node.C == 1 for node in values)