from generated.gramaticaVisitor import gramaticaVisitor


class PythonGenerator(gramaticaVisitor):
    def __init__(self):
        self.code = []

    def generate(self, ast):
        self.visit(ast)
        return "\n".join(self.code)

    def visitAssignment(self, ctx):
        var_name = ctx.ID().getText()
        expression = self.visit(ctx.boolExpr())
        self.code.append(f"{var_name} = {expression}")
        return None

    def visitPrintStmt(self, ctx):
        self.code.append(f"print({ctx.ID().getText()})")
        return None

    def visitBoolExpr(self, ctx):
        result = self.visit(ctx.boolTerm(0))

        term_index = 1
        for i in range(1, ctx.getChildCount(), 2):
            operator = ctx.getChild(i).getText()
            python_operator = "and" if operator == "AND" else "or"
            right = self.visit(ctx.boolTerm(term_index))
            result = f"({result} {python_operator} {right})"
            term_index += 1

        return result

    def visitBoolTerm(self, ctx):
        if ctx.ID():
            value = ctx.ID().getText()
        elif ctx.T_TRUE():
            value = "True"
        elif ctx.T_FALSE():
            value = "False"
        elif ctx.NUMBER():
            value = ctx.NUMBER().getText()
        else:
            value = f"({self.visit(ctx.boolExpr())})"

        if ctx.T_NOT():
            return f"(not {value})"

        return value
