from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def main():
    while 1:
        try:
            text = input('spi::> ')
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
