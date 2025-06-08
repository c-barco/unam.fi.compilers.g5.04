class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # nombre -> tipo (por ahora solo verifica existencia)
        self.errors = []

    def analyze(self, ast):
        for stmt in ast:
            self.visit(stmt)
        return self.errors

    def visit(self, node):
        if not isinstance(node, tuple) or len(node) != 2:
            self.errors.append(f"Error: nodo inválido {node}")
            return

        nodetype, children = node

        if nodetype == "var_decl":
            self.visit_var_decl(children)
        elif nodetype == "assign":
            self.visit_assign(children)
        elif nodetype == "expr_stmt" or nodetype == "expr_statement":
            self.visit(children[0])
        elif nodetype == "if":
            self.visit_if(children)
        elif nodetype == "block":
            for stmt in children:
                self.visit(stmt)
        elif nodetype in ("arith", "logical", "compare"):
            self.visit(children[0])
            self.visit(children[1])
        elif nodetype == "unary":
            self.visit(children[1])
        elif nodetype == "var":
            varname = children
            if varname not in self.symbol_table:
                self.errors.append(f"Error: variable '{varname}' no declarada.")
        elif nodetype == "call":
            for arg in children[1:] if len(children) > 1 else []:
                self.visit(arg)
        elif nodetype in ("const", "string", "char"):
            pass  # Literales, no necesitan validación
        else:
            self.errors.append(f"Error: nodo no reconocido '{nodetype}'")

    def visit_var_decl(self, children):
        name = children[0]
        value = children[1] if len(children) > 1 else None

        if name in self.symbol_table:
            self.errors.append(f"Error: variable '{name}' ya declarada.")
        else:
            self.symbol_table[name] = "any"
            if value:
                self.visit(value)

    def visit_assign(self, children):
        name = children[0]
        value = children[1]
        if name not in self.symbol_table:
            self.errors.append(f"Error: variable '{name}' no declarada antes de asignar.")
        self.visit(value)

    def visit_if(self, children):
        cond = children[0]
        then_stmt = children[1]
        else_stmt = children[2] if len(children) > 2 else None

        self.visit(cond)
        self.visit(then_stmt)
        if else_stmt:
            self.visit(else_stmt)
