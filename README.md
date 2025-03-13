# unam.fi.compilers.g5.04
Lexical Analyzer for the programming language C developed in Python

# Requisitos
El proyecto utiliza lark, para su instalación usar
```
pip install lark --upgrade
```
# Funcionamiento
El programa puede leer entradas directamente desde la terminal o desde un archivo.

```
  python lex.py [-f <archivo>] [-o <archivo_salida>]...

Opciones:
  -f <archivo>    Analiza el código fuente desde un archivo.
  -o <archivo>    Guarda la salida en un archivo en lugar de imprimirla.
  -v, --version   Muestra la versión del lexer.
  --help          Muestra este mensaje de ayuda.

Si no se proporciona un archivo, el programa pedirá entrada manual.
```

