class Binary32:
    def __init__(self, bits=None):
        if bits:
            self.bits = bits[:]
        else:
            self.bits = [0] * 32


