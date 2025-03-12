#Description: This file contains the code for the lexer 

from lark import Lark, Transformer

class Lexer(Transformer):
    def KEYWORD(self, token):
        return ("KEYWORD", token.value)

    def IDENTIFIER(self, token):
        return ("IDENTIFIER", token.value)

    def CONSTANT(self, token):
        return ("CONSTANT", token.value)

    def OPERATOR(self, token):
        return ("OPERATOR", token.value)

    def PUNCTUATION(self, token):
        return ("PUNCTUATION", token.value)

    def STRING_LITERAL(self, token):
        return ("STRING_LITERAL", token.value)

    def COMMENT(self, token):
        return ("COMMENT", token.value)

def tokenize(code):
    with open("grammar/grammar.lark", "r", encoding="utf-8") as file:
        grammar = file.read()

    parser = Lark(grammar, parser="lalr", lexer="basic", transformer=Lexer())
    return list(parser.lex(code))
