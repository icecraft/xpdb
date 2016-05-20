# -*- coding: utf-8 -*-
from copy import copy as _copy
import ast as _ast
import sys
import os.path
import logging
import inspect

__all__ = ["watchPointerList", "noWatchPoint", "getFinishLine",
           "colorStr", "logFile", "logWrapClass", "logWrapfunc"]

# init logger 
logger = logging.getLogger('xpdb.utils.log')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('xpdb.utils.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def log_init():
    inited = [False]

    def _log_init():
        pass
    
    def func():
        if inited[0]:
            return
        else:
            inited[0] = True
            _log_init()
    return func


def logWrapfunc(func, logger=logger):
    def wrap(*args, **kwargs):
        logger.info('enter %s', repr(func))
        result = func(*args, **kwargs)
        logger.info('exit %s', repr(func))
        return result
    return wrap


class logWrapClass(object):
    def __init__(self, obj):
        self.attr = "a custom function attribute"
        self.obj = obj
        self.logger = logger 
        self._instance = None

    def set_loger(self, logger):
        self.logger = logger
        
    def __call__(self, *args, **kwargs):
        self._instance = self.obj(*args, **kwargs)
        return self
        
    def __getattr__(self, attr):
        attr_1 = getattr(self._instance, attr)
        if inspect.ismethod(attr_1):
            # 如果是方法 (包括 类方法)
            return logWrapfunc(attr_1, self.logger)
        else:
            return attr_1
        
    
"""    
@logWrapClass
class B(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def ad1(self, x):
        return  x+1
"""
            

def noWatchPoint():
    return watchPointerList.noWatchPoint


class watchPointerList(object):
    """ step watch """
    _watchPList = []
    _argList = None

    @classmethod
    def reset(cls):
        cls._watchPList = []
          
    @classmethod
    def showWatchPoint(cls):
        if noWatchPoint():
            sys.stdout.write("do not set any WatchPoints now!")
            return 
        for di in cls._watchPList:
            sys.stdout.wirte("watchPoints: %s[%s] = %s"
                             % (di[0], di[1], di[2]))
          
    @classmethod
    def noWatchPoint(cls):
        return len(cls._watchPList) == 0
      
    @classmethod
    def _getId(cls, astT):
        for i in _ast.walk(astT):
            if hasattr(i, 'id'):
                return i.id
        sys.stdout.write("Error! can not get NameId")
        return "error"

    @classmethod
    def removeWatchPoint(cls, arg):
        """ if the name of watchPonter A, B are same, will remove on randomly!
        """
        for di in cls._watchPList:
            if di[-1] == arg:
                cls._watchPList.remove(di)
                sys.stdout.write("watch Point %s removed succ!" % arg)
                if cls.noWatchPoint:
                    sys.stdout.write("no watch points NOW !")
                    return
                else:
                    sys.stdout.write("failed to remove watch Point %s"
                                     % arg)
                   
    @classmethod
    def findChangedPoint(cls, frame):
        retV = False
        for di in cls._watchPList:
            try:
                f, value, eexp, id_f = di[0], di[2], di[3], di[4]
                    
                newValue = eval(eexp, f) if id_f != id(frame) \
                               else eval(eexp, frame.f_locals, frame.f_globals)
                if newValue != value:
                    sys.stdout.write('WatchPoint %s: Old Value = %s, New Value = %s'
                                     % (eexp, value, newValue))
                    sys.stdout.write('\n')
                    di[2] = newValue
                    retV = True
            except KeyError, TypeError:
                cls._watchPList.remove(di)
        return retV
      
    @classmethod
    def addWatchPoint(cls, f, arg):
        """ watch the name of point in nearest namespace,
for example: if namespace A, B both have var a, the watch pointer may attach to A.a or B.a"""
        try:
            _value = eval(arg, f.f_locals, f.f_globals)
            astT = _ast.parse(arg)
            _id = cls._getId(astT)
            sys.stdout.write("%s %s" % (repr(_value), repr(_id)))
            if _id == 'error':
                raise NoThisVarError
              
            while f:
                if f.f_locals.has_key(_id) or f.f_globals.has_key(_id):
                    wd = f.f_locals if f.f_locals.has_key(_id) else f.f_globals
                    cls._watchPList.append([_copy(wd) , _id, _value, arg, id(f)])
                    sys.stdout.write("Succ to Add Watch Point")
                    sys.stdout.write('\n')
                    wd = None
                    return 
                f = f.f_back
                      
                raise NotFoundError            
        except Exception as e:
            sys.stdout.write("Failed to Add Watch Point for %s"
                             % repr(e))
            sys.stdout.write('\n')

            
class NoThisVarError(Exception):
    def __str__(self):
        return "NoThisVarError: can not find this variable"

    
class NotFoundError(Exception):
    def __str__(self):
        return "NotFoundError: ATTENTION :my func can not find this var, but eval can! "

    
class getFinishLine(_ast.NodeVisitor):
    """ to support xpdb command finish"""
    def lookupmodule(self, filename):
        """Helper function for break/clear parsing -- may be overridden.

        lookupmodule() translates (possibly incomplete) file or module name
        into an absolute file name.
        """
        if os.path.isabs(filename) and os.path.exists(filename):
            return filename
        f = os.path.join(sys.path[0], filename)
        if os.path.exists(f):
            return f
        root, ext = os.path.splitext(filename)
        if ext == '':
            filename = filename + '.py'
        if os.path.isabs(filename):
            return filename
        for dirname in sys.path:
            while os.path.islink(dirname):
                dirname = os.readlink(dirname)
            fullname = os.path.join(dirname, filename)
            if os.path.exists(fullname):
                return fullname
        return None

    def __init__(self, frame): 
        self.findFuncStart = False
        self.co_funcn = frame.f_code.co_name
        self.co_filename = frame.f_code.co_filename
        self.abs_filename = self.lookupmodule(self.co_filename)
        self.co_lineno = frame.f_lineno
        self.max_co_lineno = self.co_lineno
        self.min_co_lineno = -1
        self.frame = frame
        try:
            with open(self.abs_filename) as f:
                contents = f.read()
            self.astObj = _ast.parse(contents, filename=self.abs_filename)    
        except:
            pass

        self.visit(self.astObj)

    def locate_scope(self, node):
        tnode = None
        for body in node.body:
            if (body.__class__.__name__ in "While_For_FunctionDef") and \
               body.lineno < self.co_lineno:
                    tnode = body
        if tnode:
            return [tnode] + self.locate_scope(tnode)
        else:
            return [None]

    def getStart_EndLine(self):
            return [self.min_co_lineno, self.max_co_lineno, self.frame]        

    def visit_FunctionDef(self, node):
        if node.name == self.co_funcn:
            scope = [node]
            scope.extend(self.locate_scope(node))
            scope.pop()
            for i in _ast.walk(scope[-1]):
                if hasattr(i, 'lineno'):
                    self.max_co_lineno = max(i.lineno, self.max_co_lineno)
                    if self.min_co_lineno == -1:
                        self.min_co_lineno = i.lineno
                    self.min_co_lineno = min(self.min_co_lineno, i.lineno)
        for body in node.body:
            self.visit(body)


class colorStr(object):
    @classmethod
    def redStr(cls, s):
        return "%s[31;2m%s%s[0m"%(chr(27), s, chr(27))

    @classmethod
    def greenStr(cls, s):
        return "%s[32;2m%s%s[0m"%(chr(27), s, chr(27))

    
class logFile(object):
    log_fd = None
    save_stdout = None
        
    @classmethod
    def dup(cls, arg):
            
        if cls.log_fd: cls.log_fd.close()
        if not cls.save_stdout: cls.save_stdout = sys.stdout
            
        cls.log_fd = open(arg, 'w+')
        sys.stdout = cls
        return cls

    @classmethod    
    def close(cls):
        if cls.log_fd:
            cls.log_fd.close()
            cls.log_fd = None
        if cls.save_stdout:
            sys.stdout = cls.save_stdout
            cls.save_stdout = None

    @classmethod        
    def write(cls, value):
        if cls.log_fd:
            cls.log_fd.write(value)
            cls.log_fd.flush()
        cls.save_stdout.write(value)

        
