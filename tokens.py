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

    BEGIN = 'BEGIN'
    END = 'END'
    ID = 'ID'
    DOT = 'DOT'
    ASSIGN = 'ASSIGN'
    SEMI = 'SEMI'
    

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.type, repr(self.value))

    def __repr__(self):
        return self.__str__()