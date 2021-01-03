from enum import Enum, Tuple


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


KEYWORDS = {
    'print': TokenType.TOKEN_PRINT
}


class Lexer:

    def __init__(self, source_code: str):
        self.tokens = []
        self.head = 0
        self.line_num = 1

    def get_next_token(self) -> Tuple[int, TokenType, str]:
        self.skip_ignored()
        if self.finished():
            return self.line_num, TokenType.TOKEN_EOF, 'EOF'
        
        next_chr = self.source_code[self.head]
        if next_chr == '$':
            self.head += 1
            return self.line_num, TokenType.TOKEN_VAR_PREFIX, '$'
        if next_chr == '(':
            self.head += 1
            return self.line_num, TokenType.TOKEN_LEFT_PAREN, '('
        if next_chr == ')':
            self.head += 1
            return self.line_num, TokenType.TOKEN_RIGHT_PAREN, ')'
        if next_chr == '=':
            self.head += 1
            return self.line_num, TokenType.TOKEN_EQUAL, '='
        if next_chr == '"':
            if self.source_code[self.head:].startswith('""'):
                self.head += 2
                return self.line_num, TokenType.TOKEN_DUOQUOTE, '""'
            self.head += 1
            return self.line_num, TokenType.TOKEN_QUOTE, '"'
        
        

    def next_token_is(self, guess: TokenType) -> Tuple[int, str]:
        line_num, token_type, token = self.get_next_token()
        if token_type != guess:
            raise LexerException("next_token_is(): syntax error neat {}".format(token))
        return line_num, token