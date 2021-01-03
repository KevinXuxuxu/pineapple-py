from abc import ABC
from collections import namedtuple
from typing import List


class Variable:

    def __init__(self, line_num: int, name: str):
        self.line_num = line_num
        self.name = name


class Statement(ABC):
    pass


class Assignment(Statement):

    def __init__(self, line_num: int, variable: Variable, string: str):
        self.line_num = line_num
        self.variable = variable
        self.string = string


class Print(Statement):

    def __init__(self, line_num: int, variable: Variable):
        self.line_num = line_num
        self.variable = variable


class SourceCode:

    def __init__(self, line_num: int, statements: List[Statement]):
        self.line_num = line_num
        self.statements = statements
