
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'then': 'THEN',
    'when': 'WHEN',
    'define': 'DEFINE',
    'end': 'END',
    'eq': 'EQ',
    'neq': 'NEQ',
    'print': 'PRINT'
    }

# List of token names.   This is always required
tokens = [
    'NUMBER',
    'NAME'
] + list(reserved.values())

literals = ['+', '-', '/', '*', '(', ')', '<', '>', '=']


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

data = '''
define a(arg1, arg2)
   b = 2
   b < 3
end
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
