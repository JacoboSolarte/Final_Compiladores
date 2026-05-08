from generated.gramaticaVisitor import gramaticaVisitor


class IRGenerator(gramaticaVisitor):
    def __init__(self):
        self.instructions = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, ast):
        self.visit(ast)
        return "\n".join(self.instructions)

    def visitAssignment(self, ctx):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.boolExpr())
        self.instructions.append(f"{var_name} = {value}")
        return var_name

    def visitPrintStmt(self, ctx):
        self.instructions.append(f"PRINT {ctx.ID().getText()}")
        return None

    def visitBoolExpr(self, ctx):
        result = self.visit(ctx.boolTerm(0))

        term_index = 1
        for i in range(1, ctx.getChildCount(), 2):
            operator = ctx.getChild(i).getText()
            right = self.visit(ctx.boolTerm(term_index))
            temp = self.new_temp()
            self.instructions.append(f"{temp} = {result} {operator} {right}")
            result = temp
            term_index += 1

        return result

    def visitBoolTerm(self, ctx):
        if ctx.ID():
            value = ctx.ID().getText()
        elif ctx.T_TRUE():
            value = "TRUE"
        elif ctx.T_FALSE():
            value = "FALSE"
        elif ctx.NUMBER():
            value = ctx.NUMBER().getText()
        else:
            value = self.visit(ctx.boolExpr())

        if ctx.T_NOT():
            temp = self.new_temp()
            self.instructions.append(f"{temp} = NOT {value}")
            return temp

        return value
