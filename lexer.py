from tokens import Token, Tokens


RESERVED_KEYWORDS = {
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
}

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

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]
    
    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result, Token(Tokens.ID, result))
        return token
    
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
            if self.current_char.isalpha():
                return self._id()
            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(Tokens.ASSIGN, ':=')
            if self.current_char == ';':
                self.advance()
                return Token(Tokens.SEMI, ';');
            if self.current_char == '.':
                self.advance()
                return Token(Tokens.DOT, '.')
            self.error()
        return Token(Tokens.EOF, None)