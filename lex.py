#Description: this file contains the main code for the program

import sys
from src.reader import read_from_file, read_from_terminal
from src.lexer import tokenize
import src.user as user



def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            user.print_help()
            return
        elif sys.argv[1] == "-f":
            if len(sys.argv) < 3:
                print("Error: Se esperaba un nombre de archivo después de '-f'.")
                return
            filename = sys.argv[2]
            code = read_from_file(filename)
        else:
            print("Error: Opción no reconocida. Usa '--help' para ver las opciones.")
            return
    else:
        code = read_from_terminal()

    tokens = tokenize(code)

    print("\nTokens encontrados:")
    for token in tokens:
        print(f"{token.type}: {token.value}")
    
    print()
    print(f"Num tokens: {len(tokens)}")
    print()

if __name__ == "__main__":
    main()
