from exception import KeyExistsError, TableFullError, KeyNotFoundError
from Node import Node
from HashUtils import HashUtils


class HashTable:
    def __init__(self, size=20):
        self.size = size
        self.table = [None] * size
        self.utils = HashUtils(size)

    def insert(self, key, value):
        base_index = self.utils.hash(key)

        first_deleted_index = None
        collision = False

        for i in range(self.size):
            index = self.utils.probe(base_index, i)
            cell = self.table[index]

            if cell is None:
                node = Node(key, value)
                node.C = 1 if collision else 0

                if first_deleted_index is not None:
                    self.table[first_deleted_index] = node
                else:
                    self.table[index] = node
                return

            if cell.deleted:
                if first_deleted_index is None:
                    first_deleted_index = index
                collision = True
                continue

            if cell.key == key:
                if not cell.deleted:
                    raise KeyExistsError(f"Ключ '{key}' уже существует")

            collision = True
        if first_deleted_index is not None:
            node = Node(key, value)
            node.C = 1 if collision else 0
            self.table[first_deleted_index] = node
            return

        raise TableFullError("Хеш-таблица переполнена")

    def get(self, key):
        base_index = self.utils.hash(key)

        for i in range(self.size):
            index = self.utils.probe(base_index, i)
            cell = self.table[index]

            if cell is None:
                return None

            if not cell.deleted and cell.key == key:
                return cell.value

        return None

    def update(self, key, value):
        base_index = self.utils.hash(key)

        for i in range(self.size):
            index = self.utils.probe(base_index, i)
            cell = self.table[index]

            if cell is None:
                break

            if cell.deleted:
                continue

            if cell.key == key:
                cell.value = value
                return

        raise KeyNotFoundError(f"Ключ '{key}' не найден")

    def delete(self, key):
        base_index = self.utils.hash(key)

        for i in range(self.size):
            index = self.utils.probe(base_index, i)
            cell = self.table[index]

            if cell is None:
                break

            if cell.deleted:
                continue

            if cell.key == key:
                cell.D = 1
                cell.U = 0
                return

        raise KeyNotFoundError(f"Ключ '{key}' не найден")


    def load_factor(self):
        count = sum(1 for x in self.table if x is not None and not x.deleted)
        return count / self.size