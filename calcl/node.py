# -*- coding: utf-8 -*-
# numbers


class Node(object):
    def __init__(self, ntype, value=None):
        self.ntype = ntype
        self.value = value

    
class flowNode(Node):
    cond = None  # condition
    tl = None  # then branch
    el = None  # else branch

    
class binoNode(Node):
    """ =, -, *, /, <, >, != , == 
stmt; list 的表示 """
    l = None  # left
    r = None  # right

    
class funcNode(Node):
    def __init__(self):
        super(funcNode, self).__init__('CALL')
    name = None    
    args = None
    body = None
