from enum import Enum


class Assoc(Enum):
    LEFT = 0
    RIGHT = 1


operators = {
    '+': (2, Assoc.LEFT),
    '-': (2, Assoc.LEFT),
    '*': (3, Assoc.LEFT),
    '/': (3, Assoc.LEFT),
    '^': (4, Assoc.RIGHT),
}

def stack_top():
    return stack[len(stack) - 1]

def get_prec(op):
    return operators[op][0]

def get_assoc(op):
    return operators[op][1]


#expression = input("Input your mathematical expression\n")
# test expression below --vvv--
expression = "-123^2^(2+4)/2/6*5(-8-3/4)"

print(expression)

tokens = []

i = 0
negative_first_char = False
subset_negative_char = False
while i < len(expression):
    if expression[i].isdigit():
        if len(tokens) > 0 and tokens[max(len(tokens) - 1, 0)] == ')':
            tokens.append('*')

        tmp = 0
        while i < len(expression) and expression[i].isdigit():
            tmp *= 10
            tmp += int(expression[i])
            i += 1

        if subset_negative_char:
            tokens.append(0 - tmp)
            subset_negative_char = False
        else:
            tokens.append(tmp)
        continue # through the number parsing while loop 'i' is already pointing at next character to pass
    elif expression[i] in operators:
        if i == 0:
            if expression[i] == '-':
                negative_first_char = True
                i += 1
                continue
            else:
                print("^--First character can't be a '{}'".format(expression[0]))
                exit(1)
        tokens.append(expression[i])
    elif expression[i] == '(':
        if isinstance(tokens[len(tokens) - 1], (float, int)):
            tokens.append('*')

        tokens.append(expression[i])

        if expression[i + 1] == '-':
            subset_negative_char = True
            # skip the '-' and go straight to number part
            i += 1

    elif expression[i] == ')':
        tokens.append(expression[i])
    else:
        print("Char '{}' is not part of any allowed functions or operators\nTry Again!".format(expression[i]))
        exit(1)


    i += 1

print(tokens)

stack = []
# rpn = Reverse Polish Notation
rpn = []

for token in tokens:
    if isinstance(token, (int, float)):
        rpn.append(token)
    elif token in operators:
        while len(stack) > 0 and stack_top() != '(' and (
                get_prec(stack_top()) > get_prec(token) or
                get_prec(stack_top()) == get_prec(token) and get_assoc(token) == Assoc.LEFT ):
            
            rpn.append(stack.pop(len(stack) - 1))
        stack.append(token)
    elif token == '(':
        stack.append(token)
    elif token == ')':
        while stack_top() != '(':
            rpn.append(stack.pop(len(stack) - 1))
        stack.pop(len(stack) - 1)
    else:
        break


rpn += reversed(stack)
stack.clear()


while len(rpn) > 1:
    i = 0
    while i <= len(rpn) - 3:
        a = rpn[i]
        b = rpn[i + 1]
        c = rpn[i + 2]

        if (isinstance(a, str) or isinstance(b, str)) and isinstance(c, str):
            i += 3
            continue
        elif isinstance(b, str):
            i += 2
            continue
        elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and isinstance(c, str):
            # collapsing 3 elements into 1
            for j in range(3):
                rpn.pop(i)

            if c == '+':
                rpn.insert(i, a + b)
            elif c == '-':
                rpn.insert(i, a - b)
            elif c == '*':
                rpn.insert(i, a * b)
            elif c == '/':
                rpn.insert(i, a / b)
            elif c == '^':
                rpn.insert(i, a ** b)
        i += 1

if negative_first_char:
    rpn[0] = 0 - rpn[0]

print("Result of calculation  : {}".format(rpn[0]))
py_calc = eval("-123**2**(2+4)/2/6*5*(-8-3/4)")
print("Python evaluated result: {}".format(py_calc))
print("Test succeded: {}".format(py_calc == rpn[0]))
