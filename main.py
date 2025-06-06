from lark import Lark, exceptions
from reader import AST
from semantic import SemanticAnalyzer

if __name__ == "__main__":
    # Leer gramática desde un archivo
    with open("grammar.lark", "r") as f:
        grammar = f.read()

    # Generar analizador
    parser = Lark(grammar, parser="lalr", transformer=AST(), keep_all_tokens=True)

    # Código de prueba
    source_code = """
    
    var x = 10;
    if (x > 5) {
        x = x - 1;
    } else {
    
    }
    
    """
    semantic = SemanticAnalyzer()

    # Analizar el código fuente
    try:
        ast = parser.parse(source_code)
        print("AST resultante:")
        print(ast)
        '''errors = semantic.analyze(ast)
        print()
        print()
        print(errors)'''
        

    
    except exceptions.UnexpectedCharacters as e:
        print("Error léxico:", e)
    except exceptions.UnexpectedInput as e:
        print("Error sintáctico:", e)
