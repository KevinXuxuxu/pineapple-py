import re

from definition import Variable, Statement, Assignment, Print, SourceCode

def parse(s: str) -> SourceCode:
    