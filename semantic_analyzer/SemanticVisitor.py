from generated.gramaticaVisitor import gramaticaVisitor
from .SymbolTable import SymbolTable


class SemanticVisitor(gramaticaVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visitAssignment(self, ctx):
        var_name = ctx.ID().getText()
        expr_type = self.visit(ctx.boolExpr())
        if expr_type != "bool":
            raise Exception(f"Semantic Error: Variable '{var_name}' must be boolean.")
        self.symbol_table.declare(var_name, "bool")
        return "bool"

    def visitPrintStmt(self, ctx):
        var_name = ctx.ID().getText()
        if not self.symbol_table.exists(var_name):
            raise Exception(f"Semantic Error: Variable '{var_name}' not defined.")
        if self.symbol_table.get_type(var_name) != "bool":
            raise Exception(f"Semantic Error: Variable '{var_name}' is not boolean.")
        return None

    def visitBoolExpr(self, ctx):
        for term in ctx.boolTerm():
            term_type = self.visit(term)
            if term_type != "bool":
                raise Exception("Semantic Error: Logical expressions only accept boolean values.")
        return "bool"

    def visitBoolTerm(self, ctx):
        if ctx.NUMBER():
            raise Exception("Semantic Error: Numeric values are not boolean.")

        if ctx.ID():
            var_name = ctx.ID().getText()
            if not self.symbol_table.exists(var_name):
                raise Exception(f"Semantic Error: Variable '{var_name}' not defined.")
            if self.symbol_table.get_type(var_name) != "bool":
                raise Exception(f"Semantic Error: Variable '{var_name}' is not boolean.")
            return "bool"

        if ctx.boolExpr():
            return self.visit(ctx.boolExpr())

        return "bool"
