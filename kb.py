# knowledge database

import os,sys

class Frame:
    
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.val  = V
        self.slot = {}
        self.nest = []
        
    def __repr__(self):
        return self.dump()
    def dump(self,depth=0,prefix=''):
        tree = self._pad(depth) + self.head(prefix)
        return tree
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix,self.type,self._val(),id(self))
    def _pad(self,depth):
        return '\n' + '\t' * depth
    def _val(self):
        return str(self.val)
    
    def __getitem__(self,key):
        return self.slot[key]
    def __setitem__(self,key,that):
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        self.slot[that.val] = that ; return self
    def __floordiv__(self,that):
        return self.push(that)
    
    def push(self,that):
        self.nest.append(that) ; return self
    def pop(self):
        return self.nest.pop()

class Primitive(Frame): pass

class Symbol(Primitive): pass

class String(Primitive): pass

class Active(Frame): pass

class VM(Active):
    def __setitem__(self,key,F):
        if callable(F): self[key] = Cmd(F) ; return self
        else: return Active.__setitem__(self,key,F)
    def __lshift__(self,F):
        if callable(F): return self << Cmd(F)
        else: return Active.__lshift__(self, F)

class Cmd(Active): pass
    
import ply.lex as lex

tokens = ['symbol']

t_ignore = ' \t\r\n'
t_ignore_comment = '[\#].*'

def t_symbol(t):
    r'[`]|[^ \t\r\n\#]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

vm = VM('kb')

def BYE(vm=vm): sys.exit(0)
vm << BYE

def QQ(vm=vm): print(vm) ; BYE(vm)
vm['??'] = QQ
    
def INTERPRET(vm=vm):
    lexer.input(vm.pop().val)
    while True:
        token = lexer.token()
        if not token: break
        print( token )

if __name__ == '__main__':
    vm // String(open('kb.ini').read()) ; INTERPRET() ; QQ()
