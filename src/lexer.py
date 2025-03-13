#Description: This file contains the code for the lexer 

from lark import Lark, logger
import logging


def tokenize(code):
    logger.setLevel(logging.WARN)
    
    with open("grammar/grammar.lark", "r", encoding="utf-8") as file:
        grammar = file.read()

    parser = Lark(grammar, lexer="basic")
    return list(parser.lex(code))


