# Generado desde gramatica.g4 por ANTLR 4.13.1
# codificacion: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,14,56,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,4,
        0,14,8,0,11,0,12,0,15,1,0,1,0,1,1,1,1,3,1,22,8,1,1,2,1,2,1,2,1,2,
        1,2,1,3,1,3,1,3,5,3,32,8,3,10,3,12,3,35,9,3,1,4,3,4,38,8,4,1,4,1,
        4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,48,8,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,
        0,0,6,0,2,4,6,8,10,0,1,1,0,4,5,57,0,13,1,0,0,0,2,21,1,0,0,0,4,23,
        1,0,0,0,6,28,1,0,0,0,8,37,1,0,0,0,10,49,1,0,0,0,12,14,3,2,1,0,13,
        12,1,0,0,0,14,15,1,0,0,0,15,13,1,0,0,0,15,16,1,0,0,0,16,17,1,0,0,
        0,17,18,5,0,0,1,18,1,1,0,0,0,19,22,3,4,2,0,20,22,3,10,5,0,21,19,
        1,0,0,0,21,20,1,0,0,0,22,3,1,0,0,0,23,24,5,11,0,0,24,25,5,10,0,0,
        25,26,3,6,3,0,26,27,5,9,0,0,27,5,1,0,0,0,28,33,3,8,4,0,29,30,7,0,
        0,0,30,32,3,8,4,0,31,29,1,0,0,0,32,35,1,0,0,0,33,31,1,0,0,0,33,34,
        1,0,0,0,34,7,1,0,0,0,35,33,1,0,0,0,36,38,5,6,0,0,37,36,1,0,0,0,37,
        38,1,0,0,0,38,47,1,0,0,0,39,48,5,11,0,0,40,48,5,2,0,0,41,48,5,3,
        0,0,42,48,5,12,0,0,43,44,5,7,0,0,44,45,3,6,3,0,45,46,5,8,0,0,46,
        48,1,0,0,0,47,39,1,0,0,0,47,40,1,0,0,0,47,41,1,0,0,0,47,42,1,0,0,
        0,47,43,1,0,0,0,48,9,1,0,0,0,49,50,5,1,0,0,50,51,5,7,0,0,51,52,5,
        11,0,0,52,53,5,8,0,0,53,54,5,9,0,0,54,11,1,0,0,0,5,15,21,33,37,47
    ]

class gramaticaParser ( Parser ):

    grammarFileName = "gramatica.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'print'", "'TRUE'", "'FALSE'", "'AND'", 
                     "'OR'", "'NOT'", "'('", "')'", "';'", "'='" ]

    symbolicNames = [ "<INVALID>", "T_PRINT", "T_TRUE", "T_FALSE", "T_AND", 
                      "T_OR", "T_NOT", "T_LPAREN", "T_RPAREN", "T_SEMICOLON", 
                      "T_ASSIGN", "ID", "NUMBER", "WS", "COMMENT" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_assignment = 2
    RULE_boolExpr = 3
    RULE_boolTerm = 4
    RULE_printStmt = 5

    ruleNames =  [ "program", "statement", "assignment", "boolExpr", "boolTerm", 
                   "printStmt" ]

    EOF = Token.EOF
    T_PRINT=1
    T_TRUE=2
    T_FALSE=3
    T_AND=4
    T_OR=5
    T_NOT=6
    T_LPAREN=7
    T_RPAREN=8
    T_SEMICOLON=9
    T_ASSIGN=10
    ID=11
    NUMBER=12
    WS=13
    COMMENT=14

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(gramaticaParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gramaticaParser.StatementContext)
            else:
                return self.getTypedRuleContext(gramaticaParser.StatementContext,i)


        def getRuleIndex(self):
            return gramaticaParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = gramaticaParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Tipo de token
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 12
                self.statement()
                self.state = 15 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==11):
                    break

            self.state = 17
            self.match(gramaticaParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(gramaticaParser.AssignmentContext,0)


        def printStmt(self):
            return self.getTypedRuleContext(gramaticaParser.PrintStmtContext,0)


        def getRuleIndex(self):
            return gramaticaParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = gramaticaParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 21
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 19
                self.assignment()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 20
                self.printStmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(gramaticaParser.ID, 0)

        def T_ASSIGN(self):
            return self.getToken(gramaticaParser.T_ASSIGN, 0)

        def boolExpr(self):
            return self.getTypedRuleContext(gramaticaParser.BoolExprContext,0)


        def T_SEMICOLON(self):
            return self.getToken(gramaticaParser.T_SEMICOLON, 0)

        def getRuleIndex(self):
            return gramaticaParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = gramaticaParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self.match(gramaticaParser.ID)
            self.state = 24
            self.match(gramaticaParser.T_ASSIGN)
            self.state = 25
            self.boolExpr()
            self.state = 26
            self.match(gramaticaParser.T_SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoolExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def boolTerm(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gramaticaParser.BoolTermContext)
            else:
                return self.getTypedRuleContext(gramaticaParser.BoolTermContext,i)


        def T_AND(self, i:int=None):
            if i is None:
                return self.getTokens(gramaticaParser.T_AND)
            else:
                return self.getToken(gramaticaParser.T_AND, i)

        def T_OR(self, i:int=None):
            if i is None:
                return self.getTokens(gramaticaParser.T_OR)
            else:
                return self.getToken(gramaticaParser.T_OR, i)

        def getRuleIndex(self):
            return gramaticaParser.RULE_boolExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolExpr" ):
                listener.enterBoolExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolExpr" ):
                listener.exitBoolExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolExpr" ):
                return visitor.visitBoolExpr(self)
            else:
                return visitor.visitChildren(self)




    def boolExpr(self):

        localctx = gramaticaParser.BoolExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_boolExpr)
        self._la = 0 # Tipo de token
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self.boolTerm()
            self.state = 33
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==4 or _la==5:
                self.state = 29
                _la = self._input.LA(1)
                if not(_la==4 or _la==5):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 30
                self.boolTerm()
                self.state = 35
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoolTermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(gramaticaParser.ID, 0)

        def T_TRUE(self):
            return self.getToken(gramaticaParser.T_TRUE, 0)

        def T_FALSE(self):
            return self.getToken(gramaticaParser.T_FALSE, 0)

        def NUMBER(self):
            return self.getToken(gramaticaParser.NUMBER, 0)

        def T_LPAREN(self):
            return self.getToken(gramaticaParser.T_LPAREN, 0)

        def boolExpr(self):
            return self.getTypedRuleContext(gramaticaParser.BoolExprContext,0)


        def T_RPAREN(self):
            return self.getToken(gramaticaParser.T_RPAREN, 0)

        def T_NOT(self):
            return self.getToken(gramaticaParser.T_NOT, 0)

        def getRuleIndex(self):
            return gramaticaParser.RULE_boolTerm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolTerm" ):
                listener.enterBoolTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolTerm" ):
                listener.exitBoolTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolTerm" ):
                return visitor.visitBoolTerm(self)
            else:
                return visitor.visitChildren(self)




    def boolTerm(self):

        localctx = gramaticaParser.BoolTermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_boolTerm)
        self._la = 0 # Tipo de token
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 36
                self.match(gramaticaParser.T_NOT)


            self.state = 47
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.state = 39
                self.match(gramaticaParser.ID)
                pass
            elif token in [2]:
                self.state = 40
                self.match(gramaticaParser.T_TRUE)
                pass
            elif token in [3]:
                self.state = 41
                self.match(gramaticaParser.T_FALSE)
                pass
            elif token in [12]:
                self.state = 42
                self.match(gramaticaParser.NUMBER)
                pass
            elif token in [7]:
                self.state = 43
                self.match(gramaticaParser.T_LPAREN)
                self.state = 44
                self.boolExpr()
                self.state = 45
                self.match(gramaticaParser.T_RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_PRINT(self):
            return self.getToken(gramaticaParser.T_PRINT, 0)

        def T_LPAREN(self):
            return self.getToken(gramaticaParser.T_LPAREN, 0)

        def ID(self):
            return self.getToken(gramaticaParser.ID, 0)

        def T_RPAREN(self):
            return self.getToken(gramaticaParser.T_RPAREN, 0)

        def T_SEMICOLON(self):
            return self.getToken(gramaticaParser.T_SEMICOLON, 0)

        def getRuleIndex(self):
            return gramaticaParser.RULE_printStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintStmt" ):
                listener.enterPrintStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintStmt" ):
                listener.exitPrintStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStmt" ):
                return visitor.visitPrintStmt(self)
            else:
                return visitor.visitChildren(self)




    def printStmt(self):

        localctx = gramaticaParser.PrintStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_printStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.match(gramaticaParser.T_PRINT)
            self.state = 50
            self.match(gramaticaParser.T_LPAREN)
            self.state = 51
            self.match(gramaticaParser.ID)
            self.state = 52
            self.match(gramaticaParser.T_RPAREN)
            self.state = 53
            self.match(gramaticaParser.T_SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





