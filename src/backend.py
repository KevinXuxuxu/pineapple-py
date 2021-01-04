import sys

from definition import Variable, Statement, Assignment, Print, SourceCode
from lexer import Lexer
from parser import parse


class Interpreter:

    def __init__(self, source_code: str):
        self.lexer = Lexer(source_code)
        self.ast = parse(self.lexer)
        self.variables = {}

    def resolve_print(self, print_statement: Print) -> None:
        print(self.variables[print_statement.variable.name])

    def resolve_assignment(self, assignment: Assignment) -> None:
        self.variables[assignment.variable.name] = assignment.string

    def resolve_statement(self, statement: Statement) -> None:
        if isinstance(statement, Print):
            self.resolve_print(statement)
        elif isinstance(statement, Assignment):
            self.resolve_assignment(statement)
        else:
            raise RuntimeError(
                'resolve_statement(): unexpected statement type: {}'.format(statement))

    def resolve_source_code(self, ast: SourceCode) -> None:
        for statement in ast.statements:
            self.resolve_statement(statement)

    def execute(self) -> None:
        self.resolve_source_code(self.ast)


def main():
    source_file = sys.argv[1]
    with open(source_file) as f:
        source_code = f.read()
    interpreter = Interpreter(source_code)
    interpreter.execute()


if __name__ == '__main__':
    main()
