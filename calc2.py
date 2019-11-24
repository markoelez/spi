class Tokens:
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    EOF = 'EOF'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAREN = '('
    RPAREN = ')'
    OP_LIST = (PLUS, MINUS, MUL, DIV)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.type, repr(self.value))

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(Tokens.INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(Tokens.PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(Tokens.MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(Tokens.MUL, '*')
            if self.current_char == '/':
                self.advance()
                return Token(Tokens.DIV, '/')
            if self.current_char == '(':
                self.advance()
                return Token(Tokens.LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(Tokens.RPAREN, ')')
            self.error()
        return Token(Tokens.EOF, None)

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        self.token = op

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = op
        self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        token = self.current_token
        if token.type == Tokens.PLUS:
            self.eat(Tokens.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == Tokens.MINUS:
            self.eat(Tokens.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == Tokens.INTEGER:
            self.eat(Tokens.INTEGER)
            return Num(token)
        elif token.type == Tokens.LPAREN:
            self.eat(Tokens.LPAREN)
            node = self.expr()
            self.eat(Tokens.RPAREN)
            return node
    
    def term(self):
        node = self.factor()
        while self.current_token.type in (Tokens.MUL, Tokens.DIV):
            token = self.current_token
            if token.type == Tokens.MUL:
                self.eat(Tokens.MUL)
            elif token.type == Tokens.DIV:
                self.eat(Tokens.DIV)
            node = BinOp(node, token, self.factor())
        return node
    
    def expr(self):
        node = self.term()
        while self.current_token.type in (Tokens.PLUS, Tokens.MINUS):
            token = self.current_token
            if token.type == Tokens.PLUS:
                self.eat(Tokens.PLUS)
            elif token.type == Tokens.MINUS:
                self.eat(Tokens.MINUS)
            node = BinOp(node, token, self.term())
        return node

    def parse(self):
        return self.expr()

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == Tokens.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == Tokens.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == Tokens.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == Tokens.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == Tokens.PLUS:
            return +self.visit(node.expr)
        elif op == Tokens.MINUS:
            return - self.visit(node.expr)
    
    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    while 1:
        try:
            text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)

if __name__ == '__main__':
    main()
