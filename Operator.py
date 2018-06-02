from enum import Enum


class Operator:
    def __init__(self, char, precedence, association):
        self.char = char
        self.prec = precedence
        self.assoc = association

    # May be redundant
    def holds(self, char):
        if char == self.char:
            return True
        return False


class Assoc(Enum):
    LEFT = 0
    RIGHT = 1


operators = [
    Operator('+', 2, Assoc.LEFT),
    Operator('-', 2, Assoc.LEFT),
    Operator('*', 3, Assoc.LEFT),
    Operator('/', 3, Assoc.LEFT),
    Operator('^', 4, Assoc.RIGHT),
]


def is_operator(char):
    for op in operators:
        if char == op:
            return (True, op)
    return False
