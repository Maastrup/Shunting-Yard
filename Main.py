import Operator

outputQueue = []
operatorStack = []


def highest_index(array):
    return array[len(array) - 1]


def push_to_queue(index, array):
    outputQueue.append(array.pop(index))


def stack_to_queue(index):
    outputQueue.append(operatorStack.pop(index))


inputString = input("Enter your calculation: ")

for char in inputString:
    if char.isdecimal():
        tempNum = ""
        tempNum += char
    # first value is the boolean
    elif Operator.is_operator(char)[0]:
        # second value contains which operator
        op = Operator.is_operator(char)[1]
        opFromStack = highest_index(operatorStack)

        while ((opFromStack.prec > op.prec or
               opFromStack.prec == op.prec and
               opFromStack.assoc == Operator.Assoc.Left) and
               opFromStack.char != '('):
            # the length - 1 is the current highest-index value
            stack_to_queue(highest_index(operatorStack))
        operatorStack.append(op)

    elif char == '(':
        operatorStack.append('(')
    elif char == ')':
        # stuff in parentheses must be calculated first
        while highest_index(operatorStack) != '(':
            stack_to_queue(highest_index(operatorStack))
        operatorStack.remove('(')

    if inputString.endswith(char):
        while len(operatorStack) != 0:
            stack_to_queue(highest_index(operatorStack))