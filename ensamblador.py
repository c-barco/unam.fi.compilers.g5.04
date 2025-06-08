from lark import Lark, Transformer, Tree, Token

# ------------ CARGA DE LA GRAMÁTICA ------------
with open("grammar.lark", "r") as f:
    grammar = f.read()

parser = Lark(grammar, parser="lalr")


# ------------ GENERADOR DE CÓDIGO X86 ------------
class ensamblador(Transformer):
    def __init__(self):
        self.code = []
        self.vars = set()
        self.label_count = 0

    def unique_label(self, base):
        self.label_count += 1
        return f"{base}_{self.label_count}"

    def program(self, items):
        for item in items:
            if isinstance(item, Tree):
                self.transform(item)
        return ""

    def var_declaration(self, items):
        name = str(items[0])
        self.vars.add(name)
        if len(items) == 2:
            self.visit_expr(items[1])
            self.code.append(f"mov [{name}], eax")
        return ""

    def assign(self, items):
        name = str(items[0])
        self.visit_expr(items[1])
        self.code.append(f"mov [{name}], eax")
        return ""

    def expr_statement(self, items):
        self.visit_expr(items[0])
        return ""

    def block(self, items):
        for stmt in items:
            if isinstance(stmt, Tree):
                self.transform(stmt)
        return ""

    def if_statement(self, items):
        condition = items[0]
        then_stmt = items[1]
        else_stmt = items[2] if len(items) > 2 else None

        else_label = self.unique_label("else")
        end_label = self.unique_label("endif")

        self.visit_expr(condition)
        self.code.append("cmp eax, 0")
        if else_stmt:
            self.code.append(f"je {else_label}")
        else:
            self.code.append(f"je {end_label}")

        if isinstance(then_stmt, Tree):
            self.transform(then_stmt)

        if else_stmt:
            self.code.append(f"jmp {end_label}")
            self.code.append(f"{else_label}:")
            if isinstance(else_stmt, Tree):
                self.transform(else_stmt)

        self.code.append(f"{end_label}:")
        return ""


    def arithmetic_op(self, items):
        left, op, right = items
        self.visit_expr(left)
        self.code.append("push eax")
        self.visit_expr(right)
        self.code.append("mov ebx, eax")
        self.code.append("pop eax")

        op_map = {'+': 'add', '-': 'sub', '*': 'imul', '/': 'idiv'}
        op_instr = op_map[str(op)]

        if op_instr == 'idiv':
            self.code.append("cdq")
            self.code.append("idiv ebx")
        else:
            self.code.append(f"{op_instr} eax, ebx")
        return ""

    def comparison_op(self, items):
        left, op, right = items
        self.visit_expr(left)
        self.code.append("push eax")
        self.visit_expr(right)
        self.code.append("mov ebx, eax")
        self.code.append("pop eax")
        self.code.append("cmp eax, ebx")

        true_label = self.unique_label("true")
        end_label = self.unique_label("endcmp")

        jmp_map = {
            '==': 'je', '!=': 'jne',
            '<': 'jl', '<=': 'jle',
            '>': 'jg', '>=': 'jge'
        }

        self.code.append(f"{jmp_map[str(op)]} {true_label}")
        self.code.append("mov eax, 0")
        self.code.append(f"jmp {end_label}")
        self.code.append(f"{true_label}:")
        self.code.append("mov eax, 1")
        self.code.append(f"{end_label}:")
        return ""

    def unary_op(self, items):
        op = str(items[0])
        self.visit_expr(items[1])
        if op == '-':
            self.code.append("neg eax")
        elif op == '!':
            false_label = self.unique_label("false")
            end_label = self.unique_label("endnot")
            self.code.append("cmp eax, 0")
            self.code.append(f"je {false_label}")
            self.code.append("mov eax, 0")
            self.code.append(f"jmp {end_label}")
            self.code.append(f"{false_label}:")
            self.code.append("mov eax, 1")
            self.code.append(f"{end_label}:")
        return ""

    def parentheses(self, items):
        self.visit_expr(items[0])
        return ""

    def number(self, items):
        value = str(items[0])
        self.code.append(f"mov eax, {value}")
        return ""

    def variable(self, items):
        name = str(items[0])
        self.code.append(f"mov eax, [{name}]")
        return ""

    def visit_expr(self, expr):
        if isinstance(expr, Tree):
            getattr(self, expr.data)(expr.children)
        elif isinstance(expr, Token):
            if expr.type == "NUMBER":
                self.number([expr])
            elif expr.type == "IDENTIFIER":
                self.variable([expr])
     


    def get_output(self):
        header = [f"{v} dd 0" for v in self.vars]
        return (
            "section .data\n"
            + "\n".join(header)
            + "\n\nsection .text\n"
            + "global _start\n_start:\n"
            + "\n".join(self.code)
            + "\nmov eax, 1\nmov ebx, 0\nint 0x80"
        )


# ------------ DEMO DE USO ------------
code = """
var x = 5;
var y = 10;
if (x < y) {
    x = x + 1;
    x = x + 2;
} else {
    x = x - 1;
    x = x - 2;
}
"""

ast = parser.parse(code)
gen = ensamblador()
gen.transform(ast)
print(gen.get_output())
