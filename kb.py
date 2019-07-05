# knowledge database
from ply.lex import lex

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

class Primitive(Frame): pass

class Symbol(Primitive): pass
    
import ply.lex as lex

tokens = ['symbol']

t_ignore = ' \t\r\n'

def t_symbol(t):
    r'[^ \t\r\n]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()
    
def INTERPRET(src):
    lexer.input(src)
    while True:
        token = lexer.token()
        if not token: break
        print( token )

if __name__ == '__main__':
    INTERPRET(open('kb.ini').read())
