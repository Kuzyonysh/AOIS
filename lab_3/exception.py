class HashTableError(Exception):
    pass
class KeyExistsError(HashTableError):
    pass
class TableFullError(HashTableError):
    pass
class KeyNotFoundError(HashTableError):
    pass