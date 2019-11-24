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

class Interpreter:
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
        if token.type == Tokens.INTEGER:
            self.eat(Tokens.INTEGER)
            return token.value
        elif token.type == Tokens.LPAREN:
            self.eat(Tokens.LPAREN)
            result = self.expr()
            self.eat(Tokens.RPAREN)
            return result
    
    def term(self):
        result = self.factor()
        while self.current_token.type in (Tokens.MUL, Tokens.DIV):
            token = self.current_token
            if token.type == Tokens.MUL:
                self.eat(Tokens.MUL)
                result = result * self.factor()
            elif token.type == Tokens.DIV:
                self.eat(Tokens.DIV)
                result = result / self.factor()
        return result
    
    def expr(self):
        result = self.term()
        while self.current_token.type in (Tokens.PLUS, Tokens.MINUS):
            token = self.current_token
            if token.type == Tokens.PLUS:
                self.eat(Tokens.PLUS)
                result = result + self.term()
            elif token.type == Tokens.MINUS:
                self.eat(Tokens.MINUS)
                result = result - self.term()
        return result

def main():
    while 1:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
