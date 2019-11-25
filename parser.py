from tokens import Token, Tokens
from nodes import Num, UnaryOp, BinOp, Compound, Var, Assign, NoOp


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
        else:
            node = self.variable()
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
    
    def program(self):
        node = self.compound_statement()
        self.eat(Tokens.DOT)
        return node

    def compound_statement(self):
        self.eat(Tokens.BEGIN)
        nodes = self.statement_list()
        self.eat(Tokens.END)
        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.type == Tokens.SEMI:
            self.eat(Tokens.SEMI)
            results.append(self.statement())
        if self.current_token.type == Tokens.ID:
            self.error()
        return results

    def statement(self):
        if self.current_token.type == Tokens.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == Tokens.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(Tokens.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(Tokens.ID)
        return node

    def empty(self):
        return NoOp()

    def parse(self):
        node = self.program()
        if self.current_token.type != Tokens.EOF:
            self.error()
        return node