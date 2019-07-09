# -*- coding: utf-8 -*-

from kb import *

## ##################################################### homoiconic game system

class Game(Frame): pass

def GAME(vm):
    vm['GAME'] = Game(vm.val)
    
    vm['GAME']['pygame'] = pyModule('pygame')
    pygame = vm['GAME']['pygame'].module
    
    window = pygame.display.set_mode((640,480))
    pygame.display.set_caption(vm.head())
    
    screen = pygame.Surface((640,480))
    
    while True:
        window.blit(screen,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                BYE(vm)
    
vm << GAME

## ################################################################ system init

if __name__ == '__main__':
    vm // String(open('game.ini').read()) ; INTERPRET(vm) ; QQ(vm)
