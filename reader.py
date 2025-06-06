from lark import Transformer, Token

class AST(Transformer):
    def program(self, items): 
        return ("program", items)

    def var_declaration(self, items):
        return ("var_decl", items)
        

    def assign(self, items):
        return ("assign", items)

    def expr_statement(self, items):
        return ("expr_stmt", items)

    def if_statement(self, items):
        
        return ("if", items)

    def block(self, items):
        return ("block", items)

    def logical_op(self, items):

        return ("logical", items)

    def comparison_op(self, items):
        return ("compare", items)

    def arithmetic_op(self, items):
        return ("arith", items)

    def unary_op(self, items):
        return ("unary", items)

    def number(self, tok):
        text = tok[0].value
        if "." in text:
            return ("const", float(text))
        else:
            return ("const", int(text))

    def string(self, tok):
        s = tok[0][1:-1]
        return ("string", s)

    def char(self, tok):
        c = tok[0][1:-1]
        return ("char", c)

    def variable(self, tok):
        return ("var", tok[0].value)

    def func_call(self, items):

        return ("call", items)

    def parentheses(self, items):
        return items[0]