#Description: this file contains the functions for the user
#provides context for them

import sys

VERSION = "1.0.0"

def print_version():
    print(f"Lexer versión {VERSION}")
    sys.exit(0)

def print_help():
    help_text = """\
Este programa es un analizador léxico que divide el código fuente en tokens.

Uso:
  python lex.py [-f <archivo>] [-o <archivo_salida>]...

Opciones:
  -f <archivo>    Analiza el código fuente desde un archivo.
  -o <archivo>    Guarda la salida en un archivo en lugar de imprimirla.
  -v, --version   Muestra la versión del lexer.
  --help          Muestra este mensaje de ayuda.

Si no se proporciona un archivo, el programa pedirá entrada manual."""
    print(help_text)
    sys.exit(0)
    
def print_version():
    print(f"Version {VERSION}")
    sys.exit(0)

def output_to_file(tokens, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for token in tokens:
                f.write(f"{token.type}: {token.value}\n")
            f.write(f"Num tokens: {len(tokens)} \n")
        print(f"Salida guardada en {filename}")
        f.close()
    except Exception as e:
        print(f"Error al escribir en el archivo {filename}: {e}")
        sys.exit(1)
        
      
      
      
      
      