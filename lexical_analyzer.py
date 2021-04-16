#!/usr/bin/python3


from enum import Enum
import sys


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

    # Identifier
    ID = 'identifier'

    # Special statements
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
    LBRACKET = '['
    RBRACKET = ']'
    COMMA = ','


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
        self.sample = sample + '\0'  # input text 에 NULL 삽입
        self.token_list = []  # Tokenized Token List
        self.start = 0  # 분석 시작 index
        self.current = 0  # 분석중 index
        self.sample_len = len(self.sample)  # input text 길이
        self.comp = ''  # input text 의 분석중인 component

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

            # 숫자갯수가 1자리 이상이면
            if (self.current - self.start) > 1:
                # 0으로 시작?
                if self.sample[self.start] == '0':
                    temp = self.current
                    self.current = self.start
                    # 0은 다 INTEGER 토큰화
                    while self.sample[self.current] == '0':
                        self.next_comp()
                        self.add_token(TokenType.INTEGER)
                        self.start = self.current
                    self.start = self.current
                    self.current = temp
                    self.add_token(TokenType.INTEGER)
                # 0 외의 나머지숫자로 시작?
                else:
                    self.add_token(TokenType.INTEGER)
            # 숫자갯수 1개
            else:
                self.add_token(TokenType.INTEGER)

            '''
            try:
                if (self.sample[self.start] == '0') & ((self.current - self.start) > 1):
                    raise Exception('Invalid Token')
                self.add_token(TokenType.INTEGER)
            except (ValueError, Exception):
                print('{}는 유효한 토큰이 아닙니다.'.format(self.sample[self.start:self.current]))
            '''

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
            elif self.sample[self.start:self.current] == 'true':
                self.add_token(TokenType.BOOLEAN)
            elif self.sample[self.start:self.current] == 'false':
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
            self.add_token(TokenType.LBRACKET)
        elif self.comp == ']':
            self.next_comp()
            self.add_token(TokenType.RBRACKET)

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
            # '-' 앞에 다른 operator -> '-'는 integer
            if (self.sample[self.current - 1] == '+') | (self.sample[self.current - 1] == '-') | \
                    (self.sample[self.current - 1] == '*') | (self.sample[self.current - 1] == '/'):
                self.next_comp()
                while is_digit(self.comp):
                    self.next_comp()
                self.add_token(TokenType.INTEGER)
            else:
                # '-' 뒤에 0임 -> 이후 00123 나오면 illegal, 0만 나오면 OK
                if self.sample[self.current + 1] == '0':
                    self.next_comp()
                    self.add_token(TokenType.OP)
                    while is_digit(self.comp):
                        self.next_comp()
                    try:
                        if (self.sample[self.start + 1] == '0') & (self.current - self.start - 1 > 1):
                            raise Exception('Invalid Token')
                        self.add_token(TokenType.INTEGER)
                    except (ValueError, Exception):
                        print('{}는 유효한 토큰이 아닙니다.'.format(self.sample[self.start + 1:self.current]))
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
            self.start += 1
            self.add_token(TokenType.CHAR)
            self.next_comp()

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


file_name = sys.argv[1]
open_file = open(file_name, 'r')
result_file = open("{}_output.txt".format(file_name), 'w')

input_text = open_file.readlines()
lex_sample = ''

# 분석할 text 전부 불러옴
for i in input_text:
    lex_sample += i

Compiler = Lexer(lex_sample)
Compiler.token_finder()
print("input message = {}".format(Compiler.sample))

# Tokenization 결과 txt 저장
for i in range(len(Compiler.token_list)):
    result_file.write('<' + Compiler.token_list[i].type + ',' + Compiler.token_list[i].value + '>' + '\n')
