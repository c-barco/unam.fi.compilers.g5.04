from lark import Transformer, Token

class AST(Transformer):
    def program(self, items):
     
        return ("program", items)

    def var_declaration(self, items):
        nombre_tok = items[0]
        if len(items) == 1:

            return ("var_decl", nombre_tok.value, None)
        else:
            expr_node = items[-1]
            return ("var_decl", nombre_tok.value, expr_node)

    def assign(self, items):
        nombre_tok = items[0]
        op_tok     = items[1]
        expr_node  = items[2]
        return ("assign", nombre_tok.value, op_tok.value, expr_node)

    def expr_statement(self, items):
        return ("expr_stmt", items[0])

    def if_statement(self, items):
        cond      = items[0]
        then_stmt = items[1]
        else_part = items[2] if len(items) == 3 else None
        return ("if", cond, then_stmt, else_part)

    def block(self, items):
        return ("block", items)

    def logical_op(self, items):
        left, op_tok, right = items
        return ("logical", op_tok.value, left, right)

    def comparison_op(self, items):
        left, op_tok, right = items
        return ("compare", op_tok.value, left, right)

    def arithmetic_op(self, items):
        left, op_tok, right = items
        return ("arith", op_tok.value, left, right)

    def unary_op(self, items):
        op_tok = items[0]
        expr   = items[1]
        return ("unary", op_tok.value, expr)

    def number(self, tok):
        text = tok[0]
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
        name = items[0].value
        args = items[1:] if len(items) > 1 else []
        return ("call", name, args)

    def parentheses(self, items):
        return items[0]