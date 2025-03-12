#Description: This file contains the code for the lexer 

from lark import Lark



def tokenize(code):
    with open("grammar/grammar.lark", "r", encoding="utf-8") as file:
        grammar = file.read()

    parser = Lark(grammar, parser="lalr", lexer="basic")
    return list(parser.lex(code))


