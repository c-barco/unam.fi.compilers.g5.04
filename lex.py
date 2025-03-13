#Description: this file contains the main code for the program

import sys
import argparse
from src.lexer import tokenize
from src.user import print_version, print_help, output_to_file
from src.reader import read_from_file, read_from_terminal

def main():
    parser = argparse.ArgumentParser(description="Lexer para lenguaje C", add_help=False)
    
    parser.add_argument("-f", "--file", help="Especifica el archivo de entrada")
    parser.add_argument("-o", "--output", help="Redirige la salida a un archivo")
    parser.add_argument("-v", "--version", action="store_true", help="Muestra la versión del lexer")
    parser.add_argument("--help", action="store_true", help="Muestra la ayuda del lexer")

    
    args = parser.parse_args()

    if args.help:
        print_help()

    if args.version:
        print_version()

    if args.file:
        
        try:
            filename = args.file
            code = read_from_file(filename)
        except FileNotFoundError:
            print("Error: Se esperaba un nombre de archivo después de '-f'.")
            sys.exit(1)
    else:
        code = read_from_terminal()

    tokens = tokenize(code)
    
    if args.output:
            output_to_file(tokens, args.output)

    else:
        print("\nTokens encontrados:")
        for token in tokens:
            print(f"{token.type}: {token.value}")
        
        print()
        print(f"Num tokens: {len(tokens)}")
        print()

  
    

if __name__ == "__main__":
    main()

