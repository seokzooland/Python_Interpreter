#!/usr/bin/python3

import slr
import sys
import stack

file_name = sys.argv[1]
open_file = open(file_name, 'r')
result_file = open("{}_result.txt".format(file_name), 'w')

input_text = open_file.readlines()
input_buffer = []
parser_stack = stack.Stack()

# 기존 lexical analyzer 결과(과제1)에서 토큰 이름 변경(과제2)
for i in input_text:
    tok = i.split()

    if tok[0] == 'INTEGER':
        tok[0] = 'NUM'
    elif tok[0] == 'CHAR':
        tok[0] = 'CHARACTER'
    elif tok[0] == 'BOOLEAN':
        tok[0] = 'BOOLSTR'
    elif tok[0] == 'STRING':
        tok[0] = 'LITERAL'
    elif tok[1] == '+':
        tok[0] = 'ADDSUB'
    elif tok[1] == '-':
        tok[0] = 'ADDSUB'
    elif tok[1] == '*':
        tok[0] = 'MULTDIV'
    elif tok[1] == '/':
        tok[0] = 'MULTDIV'
    elif tok[0] == 'LT':
        tok[0] = 'COMP'
    elif tok[0] == 'GT':
        tok[0] = 'COMP'
    elif tok[0] == 'EQ':
        tok[0] = 'COMP'
    elif tok[0] == 'NE':
        tok[0] = 'COMP'
    elif tok[0] == 'LE':
        tok[0] = 'COMP'
    elif tok[0] == 'GE':
        tok[0] = 'COMP'

    input_buffer.append(tok[0].lower())

# End Marker 추가
input_buffer.append('$')
# input buffer 0 추가
buffer_index = 0
parser_stack.push(0)

while 1:
    token = input_buffer[buffer_index]

    try:
        # SLR 테이블에서의 결과가 SHIFT 이면?
        if slr.ACTION[int(parser_stack.peek()), token][0] == 's':
            # 스택에서 하나 불러옴(peek) = stage
            temp = parser_stack.peek()
            # 토큰 스택에 넣음
            parser_stack.push(token)
            # (stage, token)의 ACTION 테이블 결과의 다음 stage 번호를 스택에 넣음
            parser_stack.push(slr.ACTION[int(temp), token][1:])
            buffer_index += 1

        # SLR 테이블에서의 결과가 REDUCE 이면?
        elif slr.ACTION[int(parser_stack.peek()), token][0] == 'r':
            # Reduce RULE number 를 가져옴.
            rule = slr.ACTION[int(parser_stack.peek()), token][1:]
            # Reduce Rule 의 첫번째를 불러옴
            rule_first = slr.GRAMMAR[int(rule)][0]
            # 어떤 식을 Reduce Rule로 바꿀지 Rule 내용을 받아옴
            reduce_rule = slr.GRAMMAR[int(rule)][1]

            if len(reduce_rule) != 0:
                for i in range(len(reduce_rule)):
                    # Rule 내의 변환 갯수*2만큼 pop
                    parser_stack.pop()
                    parser_stack.pop()
            # 어디로 GOTO할지 스택에서 불러옴
            goto_1 = int(parser_stack.peek())
            parser_stack.push(rule_first)
            # 뺀 거 reduce한 결과물을 다시 넣음
            parser_stack.push(slr.GOTO[goto_1, rule_first])

        # 잘 만들어진 문법 이라면, acc 파일 입력
        elif slr.ACTION[int(parser_stack.peek()), token] == 'acc':
            result_file.write('acc')
            break

    # 테이블에 없을 시 어디서 오류가 났는지 알려줌.
    except:
        result_file.write('reject\n')
        result_file.write('(' + parser_stack.peek() + ',' + token + ') 은 table에 없습니다.\n')
        break
