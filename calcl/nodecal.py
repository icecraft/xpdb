from node import funcNode

symtab = {}


def define(name, args, body):
    func = funcNode()
    func.args = args
    func.body = body
    symtab[name.value] = func
    

def user_call(p):
    ddict = {}
    
    def save_dict(p):
        if p.l and p.l.value in symtab:
            ddict[p.l.value] = symtab[p.l.value]
        save_dict(p.r)       
        
    def restore_dict():
        symtab.update(ddict)

    save_dict(p)
    return evalnode(p)
    restore_dict()
    
        
def evalnode(p):
    if not p:
        return
    elif p.ntype == 'FLOW':
        if p.value == 'IF':
            if evalnode(p.cond):
                evalnode(p.tl)
            elif p.el:
                evalnode(p.el)
        else:
            while evalnode(p.cond):
                evalnode(p.tl)
    elif p.ntype == 'LIST':
        evalnode(p.l)
        evalnode(p.r)
    elif p.ntype == 'BIOP':
        if p.value == '+':
            return evalnode(p.l) + evalnode(p.r)
        elif p.value == '*':
            return evalnode(p.l) * evalnode(p.r)
        elif p.value == '-':
            return evalnode(p.l) - evalnode(p.r)
        elif p.value == '/':
            return evalnode(p.l) / evalnode(p.r)
            
    elif p.ntype == 'ASSIGN':
        symtab[p.l.value] = evalnode(p.r)
        
    elif p.ntype == 'CMP':
        if p.value == '>':
            return evalnode(p.l) > evalnode(p.r)
        elif p.value == '<':
            return evalnode(p.l) < evalnode(p.r)
        elif p.value == '==':
            return evalnode(p.l) == evalnode(p.r)
        elif p.value == '!=':
            return evalnode(p.l) != evalnode(p.r)
        else:
            raise ValueError
        
    elif p.ntype == 'NUMBER':
        return p.value
    
    elif p.ntype == 'NAME':
        return symtab.get(p.value, 0)
    
    elif p.ntype == 'CALL':
        return user_call(p)



    
