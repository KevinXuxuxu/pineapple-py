import re

from definition import Variable, Statement, Assignment, Print, SourceCode
from lexer import TokenType, Lexer


class ParseException(Exception):
    pass


def parse_ignored(lexer: Lexer) -> None:
    if lexer.look_ahead() == TokenType.TOKEN_IGNORED:
        lexer.next_token_is(TokenType.TOKEN_IGNORED)


def parse_variable(lexer: Lexer) -> Variable:
    line_num = lexer.next_token_is(TokenType.TOKEN_VAR_PREFIX).line_num
    name = lexer.next_token_is(TokenType.TOKEN_NAME).token
    parse_ignored(lexer)
    return Variable(line_num, name)


def parse_string(lexer: Lexer) -> str:
    if lexer.look_ahead() == TokenType.TOKEN_DUOQUOTE:
        lexer.next_token_is(TokenType.TOKEN_DUOQUOTE)
        return ''
    lexer.next_token_is(TokenType.TOKEN_QUOTE)
    string = lexer.scan_before_token('"')
    lexer.next_token_is(TokenType.TOKEN_QUOTE)
    return string


def parse_assignment(lexer: Lexer) -> Assignment:
    var = parse_variable(lexer)
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_EQUAL)
    parse_ignored(lexer)
    string = parse_string(lexer)
    parse_ignored(lexer)
    return Assignment(var.line_num, var, string)


def parse_print(lexer: Lexer) -> Print:
    line_num = lexer.next_token_is(TokenType.TOKEN_PRINT).line_num
    lexer.next_token_is(TokenType.TOKEN_LEFT_PAREN)
    parse_ignored(lexer)
    variable = parse_variable(lexer)
    parse_ignored(lexer)
    lexer.next_token_is(TokenType.TOKEN_RIGHT_PAREN)
    parse_ignored(lexer)
    return Print(line_num, variable)


def parse_statement(lexer: Lexer) -> Statement:
    if lexer.look_ahead() == TokenType.TOKEN_PRINT:
        return parse_print(lexer)
    if lexer.look_ahead() == TokenType.TOKEN_VAR_PREFIX:
        return parse_assignment(lexer)
    raise ParseException('parse_statement(): unexpected token {}'.format(lexer.look_ahead()))


def parse(lexer: Lexer) -> SourceCode:
    statements = []
    line_num = lexer.line_num
    while lexer.look_ahead() != TokenType.TOKEN_EOF:
        statements.append(parse_statement(lexer))
    return SourceCode(line_num, statements)
