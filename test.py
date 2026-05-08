import sys
from antlr4 import *
from generated.gramaticaLexer import gramaticaLexer
from generated.gramaticaParser import gramaticaParser

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input.txt'
    
    try:
        input_stream = FileStream(input_file, encoding='utf-8')
        lexer = gramaticaLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = gramaticaParser(stream)
        tree = parser.program()
        
        print(f"Análisis léxico y sintáctico de '{input_file}' completado exitosamente.")
    except Exception as e:
        print(f"Error durante el test de lexer/parser: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
