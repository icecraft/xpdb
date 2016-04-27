
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

    
"""
# bison rules

stmt: IF exp THEN list            
   | IF exp THEN list ELSE list  
   | WHEN exp THEN list           
   | exp
;

list: /* nothing */ { $$ = NULL; }
   | stmt ';' list  {XX}                    }
   ;

exp: exp CMP exp          { $$ = newcmp($2, $1, $3); }
   | exp '+' exp          { $$ = newast('+', $1,$3); }
   | exp '-' exp          { $$ = newast('-', $1,$3);}
   | exp '*' exp          { $$ = newast('*', $1,$3); }
   | exp '/' exp          { $$ = newast('/', $1,$3); }
   | '(' exp ')'          { $$ = $2; }
   | '-' exp %prec UMINUS { $$ = newast('M', $2, NULL); }
   | NUMBER               { $$ = newnum($1); }
   | NAME                 { $$ = newref($1); }
   | NAME '=' exp         { $$ = newasgn($1, $3); }
   | NAME '(' explist ')' { $$ = newcall($1, $3); }
;

explist: exp
 | exp ',' explist  { $$ = newast('L', $1, $3); }
;
symlist: NAME       { $$ = newsymlist($1, NULL); }
 | NAME ',' symlist { $$ = newsymlist($1, $3); }
;

calclist: /* nothing */
  | calclist stmt EOL {
    if(debug) dumpast($2, 0);
     printf("= %4.4g\n> ", eval($2));
     treefree($2);
    }
  | calclist LET NAME '(' symlist ')' '=' list EOL {
                       dodef($3, $5, $8);
                       printf("Defined %s\n> ", $3->name); }

  | calclist error EOL { yyerrok; printf("> "); }
 ;

"""
