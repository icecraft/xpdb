
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'then': 'THEN',
    'when': 'WHEN',
    'define': 'DEFINE',
    'print': 'PRINT'
    }


# List of token names.   This is always required
tokens = [
    'NUMBER',
    'NAME',
    'EOL',
    'LT',
    'GT',
    'EQ',
    'NEQ',
    'CMP'
] + list(reserved.values())

literals = ['+', '-', '/', '*', '(', ')', ',', '=', ';']


def t_GT(t):
    r'\>'
    t.type = 'CMP'
    return t


def t_LT(t):
    r'\<'
    t.type = 'CMP'
    return t


def t_EQ(t):
    r'=='
    t.type = 'CMP'
    return t


def t_NEQ(t):
    r'!='
    t.type = 'CMP'
    return t


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_EOF(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

data = '''
define a( arg1, arg2 )
   b = 2
   b != 3
end
'''

# Give the lexer some input
lexer.input(data)


precedence = (
    ('nonassoc', 'CMP'),
    ('right', '='),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('nonassoc', 'UMINUS'),
    )

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print (tok)


class Node(object):
    value = None
    ntype = None

    
class flowNode(Node):
    cond = None  # condition
    tl = None  # then branch
    el = None  # else branch

    
class binoNode(Node):
    ''' =, -, *, /, <, >, != , == 
stmt; list 的表示'''
    l = None  # left
    r = None  # right

    
class funcNode(Node):
    name = None
    args = None
    body = None
    
symtab = {}

"""
# bison rules

stmt: IF exp THEN list             #flowNode  FLOW
   | IF exp THEN list ELSE list    #flowNode 
   | WHEN exp THEN list            #flowNode 
   | exp                           #binoNode  NODE
;

list: /* nothing */ 
   | stmt ';' list                #binoNode  LIST
   ;

exp: exp CMP exp                  #binoNode  BIOP
   | exp '+' exp                  #binoNode  BIOP
   | exp '-' exp                  #binoNode  BIOP
   | exp '*' exp                  #binoNode  BIOP
   | exp '/' exp                  #binoNode  BIOP
   | '(' exp ')'                  #Node      NODE  
   | '-' exp %prec UMINUS 
   | NUMBER                       #Node     NUMBER
   | NAME                         #Node     NAME 
   | NAME '=' exp                 #binoNode NAME 
   | NAME '(' explist ')'         #binoNode FUNC_CALL
;

explist: exp
 | exp ',' explist               #binoNode ARGS
;
symlist: NAME                    #binoNode SYMBOLS
 | NAME ',' symlist              #binoNode SYMBOLS
;

calclist: /* nothing */
  | calclist stmt EOL {
    if(debug) dumpast($2, 0);
     printf("= %4.4g\n> ", eval($2));
     treefree($2);
    }
  | calclist DEFINE NAME '(' symlist ')' '=' list EOL  #funcNode

  | calclist error EOL { yyerrok; printf("> "); }
 ;

"""
