/*
 * Lexer Rules
 */

 lexer grammar CharmsLexer;

 PLUS         : '+' ;
 MINUS        : '-' ;
 TIMES        : '*' ;
 DIVIDE       : '/' ;
 ASSIGN	      : '=' ;
 EQUAL        : '==' ;
 NOTEQUAL     : '!=' ;
 LESSTHAN     : '<' ;
 GREATERTHAN  : '>' ;
 AND_SYMBOL	  : '&&' ;
 OR_SYMBOL	   : '||' ;
 LPARENTHESES : '(' ;
 RPARENTHESES : ')' ;
 LCURLY       : '{' ;
 RCURLY       : '}' ;
 SEMICOLON    : ';' ;
 COMMA	       : ',' ;
 INT          : 'int' ;
 VOID         : 'void' ;
 BOOL         : 'bool' ;
 CHAR         : 'char' ;
 IF           : 'if' ;
 ELSE         : 'else' ;
 WHILE        : 'while' ;
 PRINT        : 'print' ;
 READ         : 'read' ;
 RETURN       : 'return' ;
 FUNCTION     : 'function' ;
 CTE_BOOL     : 'True' | 'False' ;
 ID           : [a-zA-Z]+ ;
 CTE_INT      : [0-9][0-9]* ;
 CTE_STRING   : [A-Za-z]+ ;
 WHITESPACE   : [ \t\r\n]+ -> skip ;
