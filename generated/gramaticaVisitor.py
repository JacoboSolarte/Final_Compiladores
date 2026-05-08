# Generado desde gramatica.g4 por ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .gramaticaParser import gramaticaParser
else:
    from gramaticaParser import gramaticaParser

# Esta clase define un visitor generico completo para un arbol de analisis producido por gramaticaParser.

class gramaticaVisitor(ParseTreeVisitor):

    # Visitar un arbol de analisis producido por gramaticaParser#program.
    def visitProgram(self, ctx:gramaticaParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visitar un arbol de analisis producido por gramaticaParser#statement.
    def visitStatement(self, ctx:gramaticaParser.StatementContext):
        return self.visitChildren(ctx)


    # Visitar un arbol de analisis producido por gramaticaParser#assignment.
    def visitAssignment(self, ctx:gramaticaParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visitar un arbol de analisis producido por gramaticaParser#boolExpr.
    def visitBoolExpr(self, ctx:gramaticaParser.BoolExprContext):
        return self.visitChildren(ctx)


    # Visitar un arbol de analisis producido por gramaticaParser#boolTerm.
    def visitBoolTerm(self, ctx:gramaticaParser.BoolTermContext):
        return self.visitChildren(ctx)


    # Visitar un arbol de analisis producido por gramaticaParser#printStmt.
    def visitPrintStmt(self, ctx:gramaticaParser.PrintStmtContext):
        return self.visitChildren(ctx)



del gramaticaParser
