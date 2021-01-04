import re
from enum import Enum
from typing import Tuple


class LexerException(Exception):
    pass


class TokenType(Enum):

    TOKEN_EOF = 0
    TOKEN_VAR_PREFIX = 1
    TOKEN_LEFT_PAREN = 2
    TOKEN_RIGHT_PAREN = 3
    TOKEN_EQUAL = 4
    TOKEN_QUOTE = 5
    TOKEN_DUOQUOTE = 6
    TOKEN_NAME = 7
    TOKEN_PRINT = 8
    TOKEN_IGNORED = 9


KEYWORDS = {
    'print': TokenType.TOKEN_PRINT
}


class TokenInfo:

    def __init__(self, line_num: int, token_type: TokenType, token: str):
        self.line_num = line_num
        self.token_type = token_type
        self.token = token

    def __repr__(self) -> Tuple[int, TokenType, str]:
        return str((self.line_num, self.token_type, self.token))


class Lexer:

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.head = 0
        self.line_num = 1
        self.next_token_info = None

    def next_source_code_is(self, prefix: str) -> bool:
        return self.source_code[self.head:].startswith(prefix)

    def finished(self) -> bool:
        return self.head >= len(self.source_code)

    def scan_pattern(self, pattern) -> str:
        result = re.findall(pattern, self.source_code[self.head:])
        if len(result) != 1:
            raise LexerException(
                'scan_pattern(): returned unexpected result: {} for pattern {}'.format(
                    result, pattern))
        return result[0]

    def scan_name(self) -> str:
        return self.scan_pattern(r'^[_a-zA-Z][_a-zA-Z0-9]*')

    def scan_ignored(self) -> str:
        return self.scan_pattern(r'^[\t\n\v\f\r ]+')

    def scan_before_token(self, token: str) -> str:
        result = self.source_code[self.head:].split(token)
        if len(result) <= 1:
            raise LexerException("scan_before_token(): missing token {}".format(token))
        self.head += len(result[0])
        self.process_new_line(result[0])
        return result[0]

    def process_new_line(self, ignored) -> None:
        i = 0
        while i < len(ignored):
            if ignored[i:][:2] in ['\r\n', '\n\r']:
                i += 2
                self.line_num += 1
            else:
                if ignored[i] in ['\r', '\n']:
                    self.line_num += 1
                i += 1

    def get_next_token(self) -> TokenInfo:
        # next token info already loaded
        if self.next_token_info is not None:
            next_token_info = self.next_token_info
            self.next_token_info = None
            return next_token_info

        # load next token
        if self.finished():
            return TokenInfo(self.line_num, TokenType.TOKEN_EOF, 'EOF')
        
        next_chr = self.source_code[self.head]
        if next_chr == '$':
            self.head += 1
            return TokenInfo(self.line_num, TokenType.TOKEN_VAR_PREFIX, '$')
        if next_chr == '(':
            self.head += 1
            return TokenInfo(self.line_num, TokenType.TOKEN_LEFT_PAREN, '(')
        if next_chr == ')':
            self.head += 1
            return TokenInfo(self.line_num, TokenType.TOKEN_RIGHT_PAREN, ')')
        if next_chr == '=':
            self.head += 1
            return TokenInfo(self.line_num, TokenType.TOKEN_EQUAL, '=')
        if next_chr == '"':
            if self.next_source_code_is('""'):
                self.head += 2
                return TokenInfo(self.line_num, TokenType.TOKEN_DUOQUOTE, '""')
            self.head += 1
            return TokenInfo(self.line_num, TokenType.TOKEN_QUOTE, '"')
        if next_chr == '_' or next_chr.isalpha():
            name = self.scan_name()
            if name in KEYWORDS:
                self.head += len(name)
                return TokenInfo(self.line_num, KEYWORDS[name], name)
            self.head += len(name)
            return TokenInfo(self.line_num, TokenType.TOKEN_NAME, name)
        if next_chr in ['\t', '\n', '\v', '\f', '\r', ' ']:
            ignored = self.scan_ignored()
            line_num = self.line_num
            self.head += len(ignored)
            self.process_new_line(ignored)
            return TokenInfo(line_num, TokenType.TOKEN_IGNORED, ignored)
        
        raise LexerException('get_next_token(): unexpected symbol {}'.format(next_chr))

    def next_token_is(self, guess: TokenType) -> TokenInfo:
        next_token_info = self.get_next_token()
        if next_token_info.token_type != guess:
            raise LexerException(
                'next_token_is(): syntax error near {}, expecting {} but got {}'.format(
                    next_token_info.token, guess, next_token_info))
        return next_token_info

    def look_ahead(self) -> TokenType:
        if self.next_token_info is None:
            self.next_token_info = self.get_next_token()
        return self.next_token_info.token_type
