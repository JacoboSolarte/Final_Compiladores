# Generado desde gramatica.g4 por ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .gramaticaParser import gramaticaParser
else:
    from gramaticaParser import gramaticaParser

# Esta clase define un listener completo para un arbol de analisis producido por gramaticaParser.
class gramaticaListener(ParseTreeListener):

    # Entrar a un arbol de analisis producido por gramaticaParser#program.
    def enterProgram(self, ctx:gramaticaParser.ProgramContext):
        pass

    # Salir de un arbol de analisis producido por gramaticaParser#program.
    def exitProgram(self, ctx:gramaticaParser.ProgramContext):
        pass


    # Entrar a un arbol de analisis producido por gramaticaParser#statement.
    def enterStatement(self, ctx:gramaticaParser.StatementContext):
        pass

    # Salir de un arbol de analisis producido por gramaticaParser#statement.
    def exitStatement(self, ctx:gramaticaParser.StatementContext):
        pass


    # Entrar a un arbol de analisis producido por gramaticaParser#assignment.
    def enterAssignment(self, ctx:gramaticaParser.AssignmentContext):
        pass

    # Salir de un arbol de analisis producido por gramaticaParser#assignment.
    def exitAssignment(self, ctx:gramaticaParser.AssignmentContext):
        pass


    # Entrar a un arbol de analisis producido por gramaticaParser#boolExpr.
    def enterBoolExpr(self, ctx:gramaticaParser.BoolExprContext):
        pass

    # Salir de un arbol de analisis producido por gramaticaParser#boolExpr.
    def exitBoolExpr(self, ctx:gramaticaParser.BoolExprContext):
        pass


    # Entrar a un arbol de analisis producido por gramaticaParser#boolTerm.
    def enterBoolTerm(self, ctx:gramaticaParser.BoolTermContext):
        pass

    # Salir de un arbol de analisis producido por gramaticaParser#boolTerm.
    def exitBoolTerm(self, ctx:gramaticaParser.BoolTermContext):
        pass


    # Entrar a un arbol de analisis producido por gramaticaParser#printStmt.
    def enterPrintStmt(self, ctx:gramaticaParser.PrintStmtContext):
        pass

    # Salir de un arbol de analisis producido por gramaticaParser#printStmt.
    def exitPrintStmt(self, ctx:gramaticaParser.PrintStmtContext):
        pass



del gramaticaParser
