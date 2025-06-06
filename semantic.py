class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # nombre -> tipo (por ahora sólo verificamos existencia)
        self.errors = []

    def analyze(self, ast):
        for stmt in ast:
            self.visit(stmt)
        return self.errors

    def visit(self, node):
        nodetype = node[0]
        if nodetype == "var_decl":
            self.visit_var_decl(node)
        elif nodetype == "assign":
            self.visit_assign(node)
        elif nodetype == "expr_statement":
            self.visit(node[1])  # es una expresión
        elif nodetype == "if_statement":
            self.visit_if(node)
        elif nodetype == "block":
            for stmt in node[1]:
                self.visit(stmt)
        elif nodetype in ("arithmetic_op", "logical_op", "comparison_op"):
            self.visit(node[2])
            self.visit(node[3])
        elif nodetype == "unary_op":
            self.visit(node[2])
        elif nodetype == "variable":
            varname = node[1]
            if varname not in self.symbol_table:
                self.errors.append(f"Error: variable '{varname}' no declarada.")
        elif nodetype == "func_call":
            for arg in node[3] or []:
                self.visit(arg)
        elif nodetype in ("number", "string", "char"):
            pass  # literales, no necesitan verificación
        else:
            self.errors.append(f"Error: nodo no reconocido '{nodetype}'")

    def visit_var_decl(self, node):
        _, name, value = node
        if name in self.symbol_table:
            self.errors.append(f"Error: variable '{name}' ya declarada.")
        else:
            self.symbol_table[name] = "any"  # por ahora no usamos tipos fuertes
            if value:
                self.visit(value)

    def visit_assign(self, node):
        _, name, value = node
        if name not in self.symbol_table:
            self.errors.append(f"Error: variable '{name}' no declarada antes de asignar.")
        self.visit(value)

    def visit_if(self, node):
        _, cond, then_stmt, else_stmt = node
        self.visit(cond)
        self.visit(then_stmt)
        if else_stmt:
            self.visit(else_stmt)