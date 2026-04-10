class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value

        self.C = 0   # коллизия
        self.U = 1   # занято
        self.D = 0   # удалено
    @property
    def deleted(self):
        return self.D == 1