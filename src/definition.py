from abc import ABC
from collections import namedtuple
from typing import List


class Variable:

    def __init__(self, line_num: int, name: str):
        self.line_num = line_num
        self.name = name

    def __repr__(self) -> str:
        return 'Variable({}, {})'.format(self.line_num, self.name)


class Statement(ABC):
    pass


class Assignment(Statement):

    def __init__(self, line_num: int, variable: Variable, string: str):
        self.line_num = line_num
        self.variable = variable
        self.string = string

    def __repr__(self) -> str:
        return 'Assignment({}, {}, {})'.format(self.line_num, self.variable, self.string)


class Print(Statement):

    def __init__(self, line_num: int, variable: Variable):
        self.line_num = line_num
        self.variable = variable

    def __repr__(self) -> str:
        return 'Print({}, {})'.format(self.line_num, self.variable)


class SourceCode:

    def __init__(self, line_num: int, statements: List[Statement]):
        self.line_num = line_num
        self.statements = statements

    def __repr__(self) -> str:
        return 'SourceCode({}, {})'.format(self.line_num, self.statements)
