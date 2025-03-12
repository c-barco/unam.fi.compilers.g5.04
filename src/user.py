#Description: this file contains the functions for the user
#provides context for them

def print_help():
    # Ayuda para el usuario
    help_text = """\
Este programa es un analizador léxico que divide el código fuente en tokens.


Uso: python lex.py [-f <archivo>] [--help]

Opciones:
  -f <archivo>    Analiza el código fuente desde un archivo.
  --help          Muestra este mensaje de ayuda.

Si no se proporciona un archivo, el programa pedirá entrada manual."""
    print(help_text)