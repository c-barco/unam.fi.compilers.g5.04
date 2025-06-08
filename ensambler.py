from llvmlite import ir, binding
from lark import Token

class LLVMTransformer:
    def __init__(self):
        self.module = ir.Module(name="module")
        self.builder = None
        self.func = None
        self.variables = {}
        self.int32 = ir.IntType(32)

    def transform(self, ast):
        # Crear función main
        func_type = ir.FunctionType(ir.VoidType(), [])
        self.func = ir.Function(self.module, func_type, name="main")
        block = self.func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        # El AST es: ('program', [lista de statements])
        for statement in ast[1]:
            if statement[0] == 'var_decl':
                self.handle_var_decl(statement[1])
            elif statement[0] == 'assign':
                self.handle_assign(statement[1])
            elif statement[0] == 'if':
                self.handle_if(statement[1])
            else:
                raise NotImplementedError(f"Statement {statement[0]} no implementado")

        self.builder.ret_void()
        return self.module

    def handle_var_decl(self, parts):
        identifier = None
        value_node = None
        for part in parts:
            if hasattr(part, 'type') and part.type == 'IDENTIFIER':
                identifier = part.value
            if isinstance(part, tuple) and part[0] == 'const':
                value_node = part
        if identifier is None:
            raise ValueError("Declaración sin identificador")
        if value_node is None:
            raise ValueError("Declaración sin valor asignado")

        ptr = self.builder.alloca(self.int32, name=identifier)
        const_val = ir.Constant(self.int32, value_node[1])
        self.builder.store(const_val, ptr)
        self.variables[identifier] = ptr

    def handle_assign(self, parts):
        var_name = None
        expr_node = None
        for part in parts:
            if hasattr(part, 'type') and part.type == 'IDENTIFIER':
                var_name = part.value
            elif isinstance(part, tuple):
                expr_node = part
        if var_name is None or expr_node is None:
            raise ValueError("Asignación mal formada")

        val = self.eval_expr(expr_node)
        ptr = self.variables.get(var_name)
        if ptr is None:
            raise ValueError(f"Variable no declarada: {var_name}")
        self.builder.store(val, ptr)

    def handle_if(self, parts):
        # Esperamos: [Token('LPAR', '('), compare_node, Token('RPAR', ')'), then_block, else_block?]
        # Encontrar nodo compare y bloques
        compare_node = None
        then_block = None
        else_block = None
        for part in parts:
            if isinstance(part, tuple) and part[0] == 'compare':
                compare_node = part
            elif isinstance(part, tuple) and part[0] == 'block':
                if then_block is None:
                    then_block = part
                else:
                    else_block = part

        if compare_node is None or then_block is None:
            raise ValueError("If mal formado")

        cond_val = self.eval_compare(compare_node)

        func = self.func
        then_bb = func.append_basic_block(name="then")
        else_bb = func.append_basic_block(name="else") if else_block else None
        merge_bb = func.append_basic_block(name="merge")

        if else_bb:
            self.builder.cbranch(cond_val, then_bb, else_bb)
        else:
            self.builder.cbranch(cond_val, then_bb, merge_bb)

        # THEN
        self.builder.position_at_start(then_bb)
        self.handle_block(then_block[1])
        self.builder.branch(merge_bb)

        # ELSE
        if else_bb:
            self.builder.position_at_start(else_bb)
            self.handle_block(else_block[1])
            self.builder.branch(merge_bb)

        self.builder.position_at_start(merge_bb)

    def handle_block(self, statements):
        for stmt in statements:
            if isinstance(stmt, tuple) and stmt[0] == 'assign':
                self.handle_assign(stmt[1])
            # Puedes añadir más casos si hay más tipos de statements en bloques

    def eval_compare(self, compare_node):
        # compare_node: ('compare', [left, op_token, right])
        left = compare_node[1][0]
        op_token = compare_node[1][1]
        right = compare_node[1][2]

        left_val = self.eval_expr(left)
        right_val = self.eval_expr(right)

        op_map = {
            '>': '>',
            '<': '<',
            '>=': '>=',
            '<=': '<=',
            '==': '==',
            '!=': '!='
        }
        op_str = op_token.value
        if op_str not in op_map:
            raise ValueError(f"Operador de comparación no soportado: {op_str}")

        return self.builder.icmp_signed(op_str, left_val, right_val, name="cmptmp")

    def eval_expr(self, expr):
        # expr puede ser ('const', val), ('var', name), ('arith', [left, op, right])
        if isinstance(expr, tuple):
            tag = expr[0]
            if tag == 'const':
                return ir.Constant(self.int32, expr[1])
            elif tag == 'var':
                var_name = expr[1]
                ptr = self.variables.get(var_name)
                if ptr is None:
                    raise ValueError(f"Variable no declarada: {var_name}")
                return self.builder.load(ptr, name=var_name+"_val")
            elif tag == 'arith':
                left = expr[1][0]
                op_token = expr[1][1]
                right = expr[1][2]

                left_val = self.eval_expr(left)
                right_val = self.eval_expr(right)
                op = op_token.value
                if op == '+':
                    return self.builder.add(left_val, right_val, name="addtmp")
                elif op == '-':
                    return self.builder.sub(left_val, right_val, name="subtmp")
                elif op == '*':
                    return self.builder.mul(left_val, right_val, name="multmp")
                elif op == '/':
                    return self.builder.sdiv(left_val, right_val, name="divtmp")
                else:
                    raise ValueError(f"Operador aritmético no soportado: {op}")
            else:
                raise ValueError(f"Expresión no soportada: {tag}")
        elif isinstance(expr, Token):
            if expr.type == 'IDENTIFIER':
                ptr = self.variables.get(expr.value)
                if ptr is None:
                    raise ValueError(f"Variable no declarada: {expr.value}")
                return self.builder.load(ptr, name=expr.value+"_val")
            else:
                # Podría ser constante numérica como token NUMERO (depende de gramática)
                try:
                    val = int(expr.value)
                    return ir.Constant(self.int32, val)
                except:
                    raise ValueError(f"Token no soportado en expresión: {expr}")
        else:
            raise ValueError(f"Tipo de expresión no reconocido: {expr}")



# -------------- Uso ------------------

# AST de ejemplo (simplificado, el que enviaste)
example_ast = (
    'program',
    [
        ('var_decl', [Token('IDENTIFIER', 'x'), Token('ASSIGN_OP', '='), ('const', 10), Token('SEMI', ';')]),
        ('if', [
            Token('LPAR', '('),
            ('compare', [('var', 'x'), Token('COMPARISON_OP', '>'), ('const', 5)]),
            Token('RPAR', ')'),
            ('block', [
                Token('LBRACE', '{'),
                ('assign', [Token('IDENTIFIER', 'x'), Token('ASSIGN_OP', '='), ('arith', [('var', 'x'), Token('ARITH_OP', '-'), ('const', 1)]), Token('SEMI', ';')]),
                Token('RBRACE', '}'),
            ]),
            ('block', [Token('LBRACE', '{'), Token('RBRACE', '}')])
        ])
    ]
)

# Para que esto funcione, necesitas tener los objetos Token de Lark importados y definidos
from lark import Token

transformer = LLVMTransformer()
llvm_module = transformer.transform(example_ast)

print(str(llvm_module))