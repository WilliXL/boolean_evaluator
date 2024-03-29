# Made by William (wxl) for 15-110
# Please DM me on Slack or email me if you find any bugs and I can fix them right away

# modeled after this super helpful gist: https://gist.github.com/leehsueh/1290686/36b0baa053072c377ac7fc801d53200d17039674

# Usage instructions:
# just run python3 booleanEvaluator.py
# the only argument right now is -e or --expression
# with the boolean expression

# the support operations are: AND, OR, XOR
# please use these exact spellings
# also please put parentheses around everything including the top level

# only TWO INPUT gates supported

# Also any singleton variables MUST be on the most right-hand side of the expression
# ie. (X AND Y) XOR Z OR X will work
# but X OR (X AND Y) will NOT work
# so please write something like the above in this form: (X AND Y) OR X

# Also also two variable inputs have to be X and Y. X and Z, or Y and Z combinations will NOT work

import re
import argparse

class InputTypes:
    # just hardcode these, whatever
    inputs3 = [
        {'X':0,'Y':0,'Z':0},
        {'X':0,'Y':0,'Z':1},
        {'X':0,'Y':1,'Z':0},
        {'X':0,'Y':1,'Z':1},
        {'X':1,'Y':0,'Z':0},
        {'X':1,'Y':0,'Z':1},
        {'X':1,'Y':1,'Z':0},
        {'X':1,'Y':1,'Z':1}
    ]

    inputs2 = [
        {'X':0,'Y':0},
        {'X':0,'Y':1},
        {'X':1,'Y':0},
        {'X':1,'Y':1}
    ]

class TokenTypes:
    CONST, INPUT, AND, OR, XOR, NOT, LP, RP = range(8)

class ASTNode:
    tokenType = None
    val       = None
    left      = None
    right     = None

    def __init__(self, token):
        self.tokenType = token

    def printVal(self):
        print(self.val)

class Tokenizer:
    expression = None
    tokens     = None
    tokenTypes = None

    i = 0

    def __init__(self, expression):
        self.expression = expression

    def next(self):
        self.i += 1
        return self.tokens[self.i-1]

    def peek(self):
        return self.tokens[self.i-1]

    def hasNext(self):
        return self.i < len(self.tokens)

    def nextTokenType(self):
        return self.tokenTypes[self.i]

    def nextTokenIsOperator(self):
        if (self.tokenTypes[self.i] == TokenTypes.AND or
            self.tokenTypes[self.i] == TokenTypes.OR  or
            self.tokenTypes[self.i] == TokenTypes.XOR):
            return True
        else:
            return False

    def tokenize(self):
        self.expression = self.expression.replace("NOT", "1 XOR")
        regEx = re.compile(r'(\bAND\b|\bOR\b|\bXOR\b|\bNOT\b|\(|\))')
        self.tokens = regEx.split(self.expression)
        self.tokens = [t.strip() for t in self.tokens if t.strip() != '']
        print(self.tokens)

        self.tokenTypes = []
        for t in self.tokens:
            if t == 'AND':
                self.tokenTypes.append(TokenTypes.AND)
            elif t == 'OR':
                self.tokenTypes.append(TokenTypes.OR)
            elif t == 'XOR':
                self.tokenTypes.append(TokenTypes.XOR)
            elif t == 'NOT':
                self.tokenTypes.append(TokenTypes.NOT)
            elif t == '(':
                self.tokenTypes.append(TokenTypes.LP)
            elif t == ')':
                self.tokenTypes.append(TokenTypes.RP)
            elif t == 'X' or t == 'Y' or t == 'Z':
                self.tokenTypes.append(TokenTypes.INPUT)
            elif t == '1': # only used for NOT case
                self.tokenTypes.append(TokenTypes.CONST)
            else: # if used properly, should never get to this case...
                self.tokenTypes.append(None) # SOMETHING'S WRONGGGG

class Parser:
    tokenizer = None
    root      = None

    def __init__(self, expression):
        self.tokenizer = Tokenizer(expression)
        self.tokenizer.tokenize()

    def parse(self):
        self.root = self.parseExpression()
        return self.root

    def parseExpression(self):
        leftTerm = self.parseXorTerm()
        while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenTypes.XOR:
            self.tokenizer.next()
            rightTerm = self.parseNotTerm()
            root = ASTNode(TokenTypes.XOR)
            root.left = leftTerm
            root.right = rightTerm
            leftTerm = root
        return leftTerm

    def parseXorTerm(self):
        leftTerm = self.parseAndTerm()
        while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenTypes.OR:
            self.tokenizer.next()
            rightTerm = self.parseAndTerm()
            root = ASTNode(TokenTypes.OR)
            root.left = leftTerm
            root.right = rightTerm
            leftTerm = root
        return leftTerm

    def parseAndTerm(self):
        leftTerm = self.parseNested()
        while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenTypes.AND:
            self.tokenizer.next()
            rightTerm = self.parseNested()
            root = ASTNode(TokenTypes.AND)
            root.left = leftTerm
            root.right = rightTerm
            leftTerm = root
        return leftTerm

    def parseNested(self):
        if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenTypes.LP:
            self.tokenizer.next()
            expression = self.parseExpression()
            if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenTypes.RP:
                self.tokenizer.next()
                return expression
            else:
                raise Exception("Closing ) expected, but got " + self.tokenizer.next())

        terminal1 = self.parseTerminal()
        if self.tokenizer.hasNext() and self.tokenizer.nextTokenIsOperator():
            condition = ASTNode(self.tokenizer.nextTokenType())
            self.tokenizer.next()
            terminal2 = self.parseTerminal()
            condition.left = terminal1
            condition.right = terminal2
            return condition
        else:
            condition = ASTNode(TokenTypes.INPUT)
            condition.val = self.tokenizer.peek()
            return condition

    def parseTerminal(self):
        if self.tokenizer.hasNext():
            tokenType = self.tokenizer.nextTokenType()
            if tokenType == TokenTypes.INPUT:
                n = ASTNode(tokenType)
                n.val = self.tokenizer.next()
                return n
            elif tokenType == TokenTypes.CONST: # only used in the NOT case
                n = ASTNode(tokenType)
                n.val = int(self.tokenizer.next())
                return n
            else:
                raise Exception(self.tokenizer.next())
        else:
            raise Exception('NUM, STR, or VAR expected, but got ' + self.tokenizer.next())

def XOR(x, y):
    if (x > 1 or y > 1 or x < 0 or y < 0):
        raise Exception('XOR is expecting binary inputs')
    if x == y:
        return 0
    else:
        return 1

class Evaluator:
    parser = None
    args   = None
    root   = None

    def __init__(self, args):
        self.args = args
        self.parser = Parser(args.expression)

    def evaluateExpression(self, numInputs):
        self.root = self.parser.parse()
        if numInputs == 2:
            inputDicts = InputTypes.inputs2
            print("X  Y  OUT")
        else:
            inputDicts = InputTypes.inputs3
            print("X  Y  Z  OUT")
        for inputDict in inputDicts:
            if numInputs == 2:
                line = "{}  {}  {}".format(inputDict['X'], inputDict['Y'],
                                           self.evaluateRecursive(self.root, inputDict))
                print(line)
            else:
                line = "{}  {}  {}  {}".format(inputDict['X'], inputDict['Y'], inputDict['Z'],
                                               self.evaluateRecursive(self.root, inputDict))
                print(line)

    def evaluateRecursive(self, ASTNode, inputDict):
        # base case, at a leaf
        # import pdb; pdb.set_trace()
        if ASTNode.tokenType == TokenTypes.INPUT:
            return inputDict.get(ASTNode.val)
        if ASTNode.tokenType == TokenTypes.CONST:
            return ASTNode.val

        # recursive case, evaluate subtrees
        else:
            left = self.evaluateRecursive(ASTNode.left, inputDict)
            right = self.evaluateRecursive(ASTNode.right, inputDict)

            if ASTNode.tokenType == TokenTypes.AND:
                return left and right
            elif ASTNode.tokenType == TokenTypes.OR:
                return left or right
            elif ASTNode.tokenType == TokenTypes.NOT:
                return 1 if right.val == 0 else 0
            elif ASTNode.tokenType == TokenTypes.XOR:
                return XOR(left,right)
            else:
                raise Exception('Unexpected token' + str(ASTNode.tokenType))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expression', '-e', metavar='e', type=str, help="Boolean Expression in the format as described in README")
    args = parser.parse_args()

    evaluator = Evaluator(args)
    if 'Z' in args.expression:
        print("Evaluating 3 inputs")
        evaluator.evaluateExpression(3)
    else:
        print("Evaluating 2 inputs")
        evaluator.evaluateExpression(2)

main()
