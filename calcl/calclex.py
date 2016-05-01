#!/usr/bin/env python
from node import flowNode, binoNode, funcNode
from nodecal import evalnode, define


precedence = (
    ('nonassoc', 'CMP'),
    ('right', '='),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('nonassoc', 'UMINUS'),
    )

##############################################


def p_stmt_if_noelse(p):
    """ stmt: IF exp THEN list """
    res = flowNode('FLOW', 'IF')
    res.cond = p[2]
    res.tl = p[4]
    p[0] = res

    
def p_stmt_if_else(p):
    """  stmt: IF exp THEN list ELSE list """
    res = flowNode('FLOW', 'IF')
    res.cond = p[2]
    res.tl = p[4]
    res.el = p[6]
    p[0] = res


def p_stmt_when(p):
    """ stmt: WHEN exp THEN list  """
    res = flowNode('FLOW', 'WHEN')
    res.cond = p[2]
    res.tl = p[4]
    p[0] = res
    

def p_stmt_exp(p):
    """    stmt : exp   """
    p[0] = p[1]

    
def p_list(p):
    """ list : 
             |stmt ';' list """
    res = binoNode('LIST')
    if len(p) == 4:
        res.l = p[1]
        res.r = p[3]
        p[0] = res        
    else:
        p[0] = []


def p_biop_exp(p):
    """ exp: exp '+' exp 
           | exp '-' exp
           | exp '*' exp 
           | exp '/' exp  """
  
    res = binoNode('BIOP', p[2].value)
    res.l = p[1]
    res.r = p[3]
    res.ntype = 'BIOP'
    res.value = p[2].value
    p[0] = res

    
def p_assign_exp(p):
    """ exp: NAME '=' exp """
    res = binoNode('ASSIGN')
    res.l = p[1]
    res.r = p[3]  
    p[0] = res

    
def p_cmp_exp(p):
    """ exp: exp CMP exp """                      
    res = binoNode('CMP')
    res.value = p[2].value    
    res.l = p[1]
    res.r = p[3]
    p[0] = res

    
def p_square_exp(p):
    """ exp: ( exp ) """
    p[0] = p[2]
    

def p_uminus_exp(p):
    """ exp: '-' exp %prec UMINUS  """
    res = binoNode('NUMBER')
    res.value = - p[2].value
    p[0] = res

    
def p_ref_exp(p):
    """ exp: NAME """
    res = binoNode('NAME')
    res.value = p[1].value
    p[0] = res


def p_number_exp(p):
    """exp: NUMBER"""
    res = binoNode('NUMBER')
    res.value = p[1].value
    p[0] = res 

    
def p_funccall_exp(p):
    """exp: NAME '(' explist ')' """
    res = funcNode()
    res.name = p[1]
    res.args = p[3]

    
def p_exp_explist(p):
    """explist: exp """
    p[0] = p[1]

    
def p_explist_explist(p):
    """explist: exp ',' explist  """
    res = binoNode('ARGS')
    res.l = p[1]
    res.r = p[3]
    p[0] = res


def p_sym_symlist(p):
    """symlist: NAME ',' symlist """
    res = binoNode('SYMBOLS')
    res.l = p[1]
    res.r = p[3]
    p[0] = res

    
def p_name_symlist(p):
    """symlist: NAME """
    res = binoNode('SYMBOLS')
    res.l = p[1]
    p[0] = res


def p_calclist_list(p):
    """ calclist: 
                | calclist stmt EOL 
                | calclist DEFINE NAME '(' symlist ')' '=' list EOL  
                | calclist error EOL """
    if len(p) == 4:
        print evalnode(p[2])
    elif len(p) == 10:    
        define(p[3], p[5], p[8])

        
def p_error_calclist(p):
    """calclist: calclist error EOL """
    print '>'

