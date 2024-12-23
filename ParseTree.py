import operator

class Node:
    def __init__(self, value):
        self.value = value
        self.leftchild = None
        self.rightchild = None
    
    def getRootVal(self):
        return self.value

    def getLeftChild(self):
        return self.leftchild
    
    def getRightChild(self):
        return self.rightchild
    
    def setLeftChild(self, leftchild):
        self.leftchild = leftchild
    
    def setRightChild(self, rightchild):
        self.rightchild = rightchild

def evaluate(parseTree):
    opers = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '^': operator.pow}
    leftC = parseTree.getLeftChild()
    rightC = parseTree.getRightChild()

    if leftC and rightC:
        fn = opers[parseTree.getRootVal()]
        return fn(float(evaluate(leftC)), float(evaluate(rightC)))
    elif isinstance(parseTree.value,Node):
        return evaluate(parseTree.value)
    else:
        root_val = parseTree.getRootVal()
        return float(root_val)

def parse_expression(tokens):
    if len(tokens) == 1:
        return Node(tokens[0])

    # make all () as subtrees and parsing them and return the root of the subtree
    while '(' in tokens:
        open_idx = tokens.index('(')
        close_idx = find_matching_parenthesis(tokens, open_idx)
        sub_tree = parse_expression(tokens[open_idx + 1:close_idx])
        tokens = tokens[:open_idx] + [sub_tree] + tokens[close_idx + 1:]

    
    op_idx = find_lowest_precedence_operator(tokens)
    
    root = Node(tokens[op_idx])
    root.setLeftChild(parse_expression(tokens[:op_idx]))
    root.setRightChild(parse_expression(tokens[op_idx + 1:]))

    return root

def find_matching_parenthesis(tokens, open_idx):
    stack = 1
    for i in range(open_idx + 1, len(tokens)):
        if tokens[i] == '(':
            stack += 1
        elif tokens[i] == ')':
            stack -= 1
        if stack == 0:
            return i
    raise ValueError("Mismatched parentheses")

def find_lowest_precedence_operator(tokens):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    lowest = float('inf')
    index = -1
    for i, token in enumerate(tokens):        # 1/3/2  example => will find the second / operator and return the index
        if isinstance(token, Node):
            continue
        if token in precedence and precedence[token] <= lowest:
            lowest = precedence[token]
            index = i
    return index


# Test cases ==========================================================================
expression1 = ' 1 / 3 / 2 '                         #  0.16666666666666666 aka 1/6
expression2 = '1 + ( 2 * 3 )'                       #  7
expression3 = '1 + 2 * ( 3 - 4 )'                   # -1
expression4 = '-1 - 2 - 3'                          # -6
expression5 = '-2 * 3 + 4'                          # -2
expression6 = '3 + ( 5 + 2 ) * 8'                   # 59
expression7 = '3 + 2 ^ 3'                           # 11
expression8 = '3 ^ ( 2 + 1 ) + ( 1 + 2 )'           # 30
expression9 =  '7 - 6 * 5 ^ 4 + 1 / 3 / 2'          # 3743.etc
expression10 = '2 * 3 + 5 * 4 - 9 / 6'              # 24.5

token1 = list(expression1.split())
token2 = list(expression2.split())
token3 = list(expression3.split())
token4 = list(expression4.split())
token5 = list(expression5.split())
token6 = list(expression6.split())
token7 = list(expression7.split())
token8 = list(expression8.split())
token9 = list(expression9.split())
token10 = list(expression10.split())

print("============================= TEST CASES ==============================")
test = parse_expression(token1)
print(evaluate(test))

test = parse_expression(token2)
print(evaluate(test))

test = parse_expression(token3)
print(evaluate(test))

test = parse_expression(token4)
print(evaluate(test))

test = parse_expression(token5)
print(evaluate(test))

test = parse_expression(token6)
print(evaluate(test))

test = parse_expression(token7)
print(evaluate(test))

test = parse_expression(token8)
print(evaluate(test))

test = parse_expression(token9)
print(evaluate(test))

test = parse_expression(token10)
print(evaluate(test))


