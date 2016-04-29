
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
    'EQ',
    'NEQ',
    'GT',
    'LT',
    'CMP'
] + list(reserved.values())

literals = ['(', ')', ',', ';', '+', '-', '*', '/', '=']


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


def p_stmt_if_noelse(p):
    """ stmt: IF exp THEN list """
    res = flowNode()
    res.ntype = 'FLOW_IF'
    res.cond = p[2]
    res.tl = p[4]
    p[0] = res

    
def p_stmt_if_else(p):
    """  stmt: IF exp THEN list ELSE list """
    res = flowNode()
    res.ntype = 'FLOW_IF'
    res.cond = p[2]
    res.tl = p[4]
    res.el = p[6]
    p[0] = res


def p_stmt_when(p):
    """ stmt: WHEN exp THEN list  """
    res = flowNode()
    res.ntype = 'FLOW_WHEN'
    res.cond = p[2]
    res.tl = p[4]
    p[0] = res
    

def p_stmt_exp(p):
    """    stmt : exp   """
    p[0] = p[1]

    
def p_list(p):
    """ list : 
             |stmt ';' list """
    res = binoNode()
    res.ntype = 'LIST'
    if len(p) == 4:
        res.l = p[1]
        res.r = p[3]
        p[0] = res        
    else:
        res.l, res.r = None, None
        p[0] = res


def p_biop_exp(p):
    """ exp: exp '+' exp 
           | exp '-' exp
           | exp '*' exp 
           | exp '/' exp  """
  
    res = binoNode()
    res.l = p[1]
    res.r = p[3]
    res.ntype = 'BIOP'
    res.value = p[2].value
    p[0] = res

    
def evalnode(node):
    pass


def p_assign_exp(p):
    """ exp: NAME '=' exp """
    p[0] = evalnode(p[3])
    symtab[p[1]] = p[0]


def p_cmp_exp(p):
    """ exp: exp CMP exp """                      
    res = binoNode()
    res.l = p[1]
    res.r = p[3]
    res.ntype = 'CMP'
    res.value = p[2].value
    p[0] = res

def p_square_exp(p):
    """ exp: ( exp ) """
    p[0] = p[2]
    

def p_uminus_exp(p):
    """ exp: '-' exp %prec UMINUS  """
    res = binoNode()
    res.value = - p[2].value
    res.ntype = 'NUMBER'
    p[0] = res

def p_ref_exp(p):
    """ exp: NAME """
    res = binoNode()
    res.value = lookup(p[1])
    p[0] = res

    
    
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

Pexp: exp CMP exp                  #binoNode  BIOP
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
