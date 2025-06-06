from lark import Lark, exceptions
from reader import AST

if __name__ == "__main__":
    # Leer gramática desde un archivo
    with open("grammar.lark", "r") as f:
        grammar = f.read()

    # Generar analizador
    parser = Lark(grammar, parser="lalr", propagate_positions=True, transformer=AST())

    # Código de prueba
    source_code = """
    var x = 10;
    if (x > 5) {
        x = x - 1;
    } else {
        print("no es mayor");
    }
    x = x + 1;
    """

    # Analizar el código fuente
    try:
        ast = parser.parse(source_code)
        print("AST resultante:")
        print(ast)


    except exceptions.UnexpectedCharacters as e:
        print("Error léxico:", e)
    except exceptions.UnexpectedInput as e:
        print("Error sintáctico:", e)
