grammar gramatica;

// Lenguaje de expresiones logicas complejas
program : statement+ EOF ;

statement : assignment | printStmt ;

assignment : ID T_ASSIGN boolExpr T_SEMICOLON ;

boolExpr : boolTerm ((T_AND | T_OR) boolTerm)* ; 

boolTerm : T_NOT? (ID | T_TRUE | T_FALSE | NUMBER | T_LPAREN boolExpr T_RPAREN) ;

printStmt : T_PRINT T_LPAREN ID T_RPAREN T_SEMICOLON ;

// Tokens
T_PRINT : 'print' ;
T_TRUE : 'TRUE' ;
T_FALSE : 'FALSE' ;
T_AND : 'AND' ;
T_OR : 'OR' ;
T_NOT : 'NOT' ;

T_LPAREN : '(' ;
T_RPAREN : ')' ;
T_SEMICOLON : ';' ;
T_ASSIGN : '=' ;

ID : [a-zA-Z_][a-zA-Z0-9_]* ;
NUMBER : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;
COMMENT : '//' ~[\r\n]* -> skip ;
