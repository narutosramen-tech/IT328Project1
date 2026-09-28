from enum import Enum

class RegexSymbol(Enum):
    A = "a"
    B = "b"
    EPSILON = "e"
    EMPTY_SET = "es"

    def __str__(self):
        return self.value