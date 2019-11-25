import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def main():
    text = open(sys.argv[1], 'r').read()
    
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)

if __name__ == '__main__':
    main()
