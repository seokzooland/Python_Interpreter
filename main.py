from enum import Enum


class TokenType(Enum):
    # Variable Type
    INT = 'int'
    CHAR = 'char'
    BOOLEAN = 'boolean'
    STRING = 'String'

    # Boolean String
    TRUE = 'true'
    FALSE = 'false'

    # Special statements
    IF = 'if'
    ELSE = "else"
    WHILE = 'while'
    CLASS = 'class'
    RETURN = 'return'

    # arithmetic operators
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    SLASH = '/'

    # Assignment operator
    ASSIGN = '='

    # Comparison operators
    LT = '<'
    GT = '>'
    EQ = '=='
    NE = '!='
    LE = '<='
    GE = '>='

    # Symbols
    SEMI = ';'
    LBLACE = '{'
    RBLACE = '}'
    LPAREN = '('
    RPAREN = ')'
    LBLACKET = '['
    RBLANKET = ']'
    COMMA = ','

    # spaces
    WS = ' '
    IG_WS = {'\n', '\t', ' '}


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return '{:<10} || {}'.format(self.type, self.value)


def is_digit(s):
    return '0' <= s <= '9' if s else False


def is_letter(s):
    if ('A' <= s <= 'Z') | ('a' <= s <= 'z'):
        return True
    else:
        return False


class Lexer:
    def __init__(self, sample):
        self.sample = sample
        self.token_list = []
        self.start = 0
        self.current = 0
        self.comp = ''

    def find_token(self):
        self.comp = self.sample[self.current]

        if is_digit(self.comp):
            while is_digit(self.comp):
                self.next_comp()
            self.add_token(TokenType.INT)

    def next_comp(self):
        self.current += 1
        self.comp = self.sample[self.current]

    def add_token(self, t_type):
        Token_Value = Token(t_type.name, self.sample[self.start: self.current])
        self.token_list.append(Token_Value)


Compiler = Lexer('1231243124124aefaefe')
Compiler.find_token()
for i in range(len(Compiler.token_list)):
    print(Compiler.token_list[i])
