from enum import Enum


class TokenType(Enum):
    # vtype
    VTYPE = 'vtype'

    INTEGER = 'int'
    CHAR = 'char'
    BOOLEAN = 'boolean'
    STRING = 'String'

    # Boolean String
    TRUE = 'true'
    FALSE = 'false'

    # Special statements
    ID = 'identifier'

    IF = 'if'
    ELSE = "else"
    WHILE = 'while'
    CLASS = 'class'
    RETURN = 'return'

    # Arithmetic operators
    OP = 'operator'

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

    # Spaces
    WS = ' '
    IG_WS = {'\n', '\t', ' '}


# 토큰 인자 -> 이름, 값(string) 저장
class Token:
    def __init__(self, t_type, t_value):
        self.type = t_type
        self.value = t_value


# 숫자확인 -> return bool
def is_digit(s):
    return '0' <= s <= '9' if s else False


# 문자확인 -> return bool
def is_letter(s):
    if ('A' <= s <= 'Z') | ('a' <= s <= 'z') | (s == '_'):
        return True
    else:
        return False


class Lexer:
    def __init__(self, sample):
        self.sample = sample + '\0'         # input text 에 NULL 삽입
        self.token_list = []                # Tokenized Token List
        self.start = 0                      # 분석 시작 index
        self.current = 0                    # 분석중 index
        self.sample_len = len(self.sample)  # input text 길이
        self.comp = ''                      # input text 의 분석중인 component

    # NULL 만날 때까지 Token 찾음
    def token_finder(self):
        while self.sample[self.current] != '\0':
            self.start = self.current
            self.find_token()
            self.start = self.current

    # 토큰 찾기
    def find_token(self):
        self.comp = self.sample[self.current]

        # 숫자로 시작
        if is_digit(self.comp):
            while is_digit(self.comp):
                self.next_comp()

            # 0으로 시작하는 숫자들 예외처리(0 단일 제외)
            try:
                if (self.sample[self.start] == '0') & ((self.current - self.start) >1):
                    raise Exception('Invalid Token')
                self.add_token(TokenType.INTEGER)
            except (ValueError, Exception):
                print('{}는 유효한 토큰이 아닙니다.'.format(self.sample[self.start:self.current]))

        # 문자로 시작
        elif is_letter(self.comp):
            while is_letter(self.comp) | is_digit(self.comp):
                self.next_comp()
            # if
            if self.sample[self.start:self.current] == 'if':
                self.add_token(TokenType.IF)
            # else
            elif self.sample[self.start:self.current] == 'else':
                self.add_token(TokenType.ELSE)
            # while
            elif self.sample[self.start:self.current] == 'while':
                self.add_token(TokenType.WHILE)
            # class
            elif self.sample[self.start:self.current] == 'class':
                self.add_token(TokenType.CLASS)
            # return
            elif self.sample[self.start:self.current] == 'return':
                self.add_token(TokenType.RETURN)
            # True / False
            elif self.sample[self.start:self.current] == 'True':
                self.add_token(TokenType.BOOLEAN)
            elif self.sample[self.start:self.current] == 'False':
                self.add_token(TokenType.BOOLEAN)
            # int, char, Boolean, String -> vtype
            elif self.sample[self.start:self.current] == 'int':
                self.add_token(TokenType.VTYPE)
            elif self.sample[self.start:self.current] == 'char':
                self.add_token(TokenType.VTYPE)
            elif self.sample[self.start:self.current] == 'Boolean':
                self.add_token(TokenType.VTYPE)
            elif self.sample[self.start:self.current] == 'String':
                self.add_token(TokenType.VTYPE)
            # 그외 -> ID
            else:
                self.add_token(TokenType.ID)

        # 소괄호
        elif self.comp == '(':
            self.next_comp()
            self.add_token(TokenType.LPAREN)

        elif self.comp == ')':
            self.next_comp()
            self.add_token(TokenType.RPAREN)

        # 중괄호
        elif self.comp == '{':
            self.next_comp()
            self.add_token(TokenType.LBLACE)
        elif self.comp == '}':
            self.next_comp()
            self.add_token(TokenType.RBLACE)

        # 대괄호
        elif self.comp == '[':
            self.next_comp()
            self.add_token(TokenType.LBLACKET)
        elif self.comp == ']':
            self.next_comp()
            self.add_token(TokenType.RBLANKET)

        # 세미콜론
        elif self.comp == ';':
            self.next_comp()
            self.add_token(TokenType.SEMI)

        # 콤마
        elif self.comp == ',':
            self.next_comp()
            self.add_token(TokenType.COMMA)

        # '='
        elif self.comp == '=':
            self.next_comp()
            self.add_token(TokenType.ASSIGN)

        # '+' / '-' / '*' / '/'
        elif self.comp == '+':
            self.next_comp()
            self.add_token(TokenType.OP)
        elif self.comp == '-':
            if (self.sample[self.current - 1] == '+') | (self.sample[self.current - 1] == '-') | \
                    (self.sample[self.current - 1] == '*') | (self.sample[self.current - 1] == '/'):
                self.next_comp()
                while is_digit(self.comp):
                    self.next_comp()
                self.add_token(TokenType.INTEGER)
            else:
                self.next_comp()
                self.add_token(TokenType.OP)
        elif self.comp == '*':
            self.next_comp()
            self.add_token(TokenType.OP)
        elif self.comp == '/':
            self.next_comp()
            self.add_token(TokenType.OP)

        # 비교연산자 '<' / '>' / '==' / '!=' / '<=' / '>='
        elif self.comp == '<':
            self.next_comp()
            self.add_token(TokenType.LT)
        elif self.comp == '>':
            self.next_comp()
            self.add_token(TokenType.GT)
        elif self.comp == '==':
            self.next_comp()
            self.add_token(TokenType.EQ)
        elif self.comp == '!=':
            self.next_comp()
            self.add_token(TokenType.NE)
        elif self.comp == '<=':
            self.next_comp()
            self.add_token(TokenType.LE)
        elif self.comp == '>=':
            self.next_comp()
            self.add_token(TokenType.GE)

        # 공백문자 무시
        elif (self.comp == ' ') | (self.comp == '\n') | (self.comp == '\t'):
            self.next_comp()

        # '' char
        elif self.comp == '\'':
            self.next_comp()
            while self.comp != '\'':
                self.next_comp()
            self.next_comp()
            self.add_token(TokenType.CHAR)

        # "" string
        elif self.comp == '\"':
            self.next_comp()
            while self.comp != '\"':
                self.next_comp()
            self.next_comp()
            self.add_token(TokenType.STRING)

    # next component
    def next_comp(self):
        self.current += 1
        self.comp = self.sample[self.current]

    # 리스트에 토큰 추가
    def add_token(self, t_type):
        Token_Value = Token(t_type.name, self.sample[self.start: self.current])
        self.token_list.append(Token_Value)


open_file = open("sample.txt", 'r')
result_file = open("result.csv", 'w')

input_text = open_file.readlines()
lex_sample = ''

# 분석할 text 전부 불러옴
for i in input_text:
    lex_sample += i

Compiler = Lexer(lex_sample)
Compiler.token_finder()
print("input message = {}".format(Compiler.sample))

# Tokenization 결과 csv 저장
for i in range(len(Compiler.token_list)):
    result_file.write(Compiler.token_list[i].type + ',' + Compiler.token_list[i].value + '\n')
