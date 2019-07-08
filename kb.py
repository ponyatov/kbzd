# knowledge database

import os,sys

## ######################################### Marvin Minsky extended frame model

class Frame:
    
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.val  = V
        self.slot = {}
        self.nest = []
        self.immed = False
        
    def __repr__(self):
        return self.dump()
    def dump(self,depth=0,prefix='',voc=True):
        tree = self._pad(depth) + self.head(prefix)
        if not depth: Frame._dumped = []
        if self in Frame._dumped: return tree + ' _/'
        else: Frame._dumped.append(self)
        if voc:
            for i in self.slot:
                tree += self.slot[i].dump(depth+1,prefix=i+' = ')
        for j in self.nest:
            tree += j.dump(depth+1)
        return tree
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix,self.type,self._val(),id(self))
    def _pad(self,depth):
        return '\n' + ' '*4 * depth
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
    def __init__(self,V):
        Active.__init__(self, V)
        self.compile = []
    def __setitem__(self,key,F):
        if callable(F): self[key] = Cmd(F) ; return self
        else: return Active.__setitem__(self,key,F)
    def __lshift__(self,F):
        if callable(F): return self << Cmd(F)
        else: return Active.__lshift__(self, F)

class Cmd(Active):
    def __init__(self,F,I=False):
        Active.__init__(self, F.__name__)
        self.immed = I
        self.fn = F
    def eval(self,vm):
        self.fn(vm)
        
class Seq(Active,Vector): pass

## ######################################################################## I/O

class IO(Frame): pass

class Dir(IO): pass
class File(IO): pass

## #################################################################### network

class Net(IO): pass
class Url(Net): pass
class Web(Net): pass
class Ip(Net): pass
class Port(Net): pass

## ################################################################ documenting

class Doc(Frame): pass
class Font(Doc): pass
class Color(Doc): pass

## ############################################################ metaprogramming

class Meta(Frame): pass

class Module(Meta): pass
        
## ##################################################### global virtual machine

vm = VM('kb')

## ###################################################################### debug

def BYE(vm): sys.exit(0)
vm << BYE

def Q(vm): print(vm.dump(voc=False))
vm['?'] = Cmd(Q,I=True)

def QQ(vm): print(vm.dump(voc=True)) ; BYE(vm)
vm['??'] = Cmd(QQ,I=True)

### ########################################################## stack operations

def DOT(vm): vm.dropall()
vm['.'] = DOT

## ######################################################## frame manipulations

def EQ(vm): addr = vm.pop() ; vm[addr.val] = vm.pop()
vm['='] = EQ

## ######################################################################## I/O

## ############################################################ metaprogramming

def MODULE(vm): vm // Module(vm.pop().val)
vm << MODULE

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
    try: vm // vm[token.val] ; return True
    except KeyError: vm // vm[token.val.upper()] ; return True
    return False

def EVAL(vm):
    vm.pop().eval(vm)
    
def INTERPRET(vm):
    lexer.input(vm.pop().val)
    while True:
        if not WORD(vm): break;
        if isinstance(vm.top(),Symbol):
            if not FIND(vm): raise SyntaxError(vm)
        if not vm.compile or vm.top().immed:
            EVAL(vm)
        else:
            COMPILE(vm)
            
## ################################################################### compiler

def COMPILE(vm): vm.compile[-1] // vm.pop()

def REC(vm): vm.compile[-1] // vm.compile[-1]
vm['REC'] = Cmd(REC,I=True)
        
def LQ(vm): vm.compile.append(Vector(''))
vm['['] = Cmd(LQ,I=True)

def RQ(vm):
    item = vm.compile.pop()
    if vm.compile: vm.compile[-1] // item
    else: vm // item
vm[']'] = Cmd(RQ,I=True)

def LC(vm): vm.compile.append(Seq(''))
vm['{'] = Cmd(LC,I=True)

def RC(vm): RQ(vm)
vm['}'] = Cmd(RC,I=True)

## #################################################################### network

def URL(vm): vm // Url(vm.pop().val)
vm['URL'] = URL

def WEB(vm):
    web = Web(vm.val) ; vm['WEB'] = web
    web['IP'] = Ip('127.0.0.1') ; web['PORT'] = Port(8888)
    css = web['CSS'] = File('dark.css')
    css['font'] = Font('monospace')
    css['font']['size'] = String('3mm')
    css['background'] = Color('black')
    css['color'] = Color('lightgreen')
    
    import flask,flask_wtf,wtforms
    
    web.app = flask.Flask(vm.val)
    web.app.config['SECRET_KEY'] = os.urandom(32)
    
    class CLI(flask_wtf.FlaskForm):
        pad = wtforms.TextAreaField('pad',
                                    render_kw={'rows':5,'autofocus':'true'},
                                    default='# metaL/kb')
        go  = wtforms.SubmitField('go')
    
    @web.app.route('/',methods=['GET','POST'])
    def index():
        form = CLI()
        if form.validate_on_submit():
            vm // String(form.pad.data) ; INTERPRET(vm)
        return flask.render_template('index.html',vm=vm,web=web,form=form)
    
    @web.app.route('/css.css')
    def css():
        return flask.Response(
            flask.render_template('css.css',vm=vm,web=web),
            mimetype='text/css')
        
    @web.app.route('/<path:path>')
    def path(path):
        return flask.render_template('dump.html',vm=vm[path],web=web)
    
    web.app.run(
        host=web['IP'].val,port=web['PORT'].val,debug=True,extra_files='kb.ini')
     
vm['WEB'] = WEB

## ################################################################ system init

if __name__ == '__main__':
    vm // String(open('kb.ini').read()) ; INTERPRET(vm) ; QQ(vm)
