# knowledge database

import os,sys

## ######################################### Marvin Minsky extended frame model

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
        for i in self.slot:
            tree += self.slot[i].dump(depth+1,prefix=i+' = ')
        for j in self.nest:
            tree += j.dump(depth+1)
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
    def top(self):
        return self.nest[-1]
    def dropall(self):
        self.nest = [] ; return self
    
    def eval(self,vm):
        vm // self
        
## ##################################################### primitive/scalar types

class Primitive(Frame): pass

class Symbol(Primitive): pass

class String(Primitive): pass

class Number(Primitive):
    def __init__(self,V):
        Primitive.__init__(self,float(V))

class Integer(Number):
    def __init__(self,V):
        Primitive.__init__(self,int(V))

class Hex(Integer):
    def __init__(self,V):
        Primitive.__init__(self,int(V[2:],0x10))
    def _val(self):
        return hex(self.val)

class Bin(Integer):
    def __init__(self,V):
        Primitive.__init__(self,int(V[2:],0x02))
    def _val(self):
        return bin(self.val)

## ############################################################ data containers

class Container(Frame): pass

class Vector(Container): pass

class Stack(Container): pass

class Dict(Container): pass

class Queue(Container): pass

## #################################### active (executable/evaluatable) objects

class Active(Frame): pass

class VM(Active):
    def __setitem__(self,key,F):
        if callable(F): self[key] = Cmd(F) ; return self
        else: return Active.__setitem__(self,key,F)
    def __lshift__(self,F):
        if callable(F): return self << Cmd(F)
        else: return Active.__lshift__(self, F)

class Cmd(Active):
    def __init__(self,F):
        Active.__init__(self, F.__name__)
        self.fn = F
    def eval(self,vm):
        self.fn(vm)
        
## ##################################################### global virtual machine

vm = VM('kb')

## ###################################################################### debug

def BYE(vm): sys.exit(0)
vm << BYE

def Q(vm): print(vm)
vm['?'] = Q

def QQ(vm): Q(vm) ; BYE(vm)
vm['??'] = QQ

### ########################################################## stack operations

def DOT(vm): vm.dropall()
vm['.'] = DOT

## ######################################################## frame manipulations

def EQ(vm): addr = vm.pop() ; vm[addr.val] = vm.pop()
vm['='] = EQ

## ############################################ PLY-powered parser (lexer only)
    
import ply.lex as lex

tokens = ['symbol','string','number','integer','hex','bin']

t_ignore = ' \t\r\n'
t_ignore_comment = r'[#\\].*'

states = (('str','exclusive'),)
t_str_ignore = ''
def t_str(t):
    r'\''
    t.lexer.push_state('str') ; t.lexer.string = ''
def t_str_str(t):
    r'\''
    t.lexer.pop_state() ; return String(t.lexer.string)
def t_str_char(t):
    r'.'
    t.lexer.string += t.value

def t_hex(t):
    r'0x[0-9a-fA-F]+'
    return Hex(t.value)
def t_bin(t):
    r'0b[01]+'
    return Bin(t.value)

def t_number_exp(t):
    r'[+\-]?[0-9]+[eE][+\-]?[0-9]+'
    return Number(t.value)
def t_number_dot(t):
    r'[+\-]?[0-9]*\.[0-9]+'
    return Number(t.value)
    
def t_integer(t):
    r'[+\-]?[0-9]+'
    return Integer(t.value)

def t_symbol(t):
    r'[`]|[^ \t\r\n\#\\]+'
    return Symbol(t.value)

def t_ANY_error(t): raise SyntaxError(t)

lexer = lex.lex()

## ################################################################ interpreter

def QUOTE(vm): WORD(vm)
vm['`'] = QUOTE

def WORD(vm):
    token = lexer.token()
    if token: vm // token ; return True
    return False

def FIND(vm):
    token = vm.pop()
    vm // vm[token.val] ; return True
    return False

def EVAL(vm):
    vm.pop().eval(vm)
    
def INTERPRET(vm):
    lexer.input(vm.pop().val)
    while True:
        if not WORD(vm): break;
        if isinstance(vm.top(),Symbol):
            if not FIND(vm): raise SyntaxError(vm)
        EVAL(vm)
        
## ################################################################ system init

if __name__ == '__main__':
    vm // String(open('kb.ini').read()) ; INTERPRET(vm) ; QQ(vm)
