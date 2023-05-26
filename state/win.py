#Mòduls
import pygame
from pygame.locals import *
from pgu import engine
import conf


class Win(engine.State): # ---------------------- YOU WIN ---------------------- #

    def init(self):
        self.image = pygame.image.load("imag/win.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (960, 630))
        self.colors = ((10,10,10),(255,255,255))
        self.colorList = 0

        #Cursor
        #self.grpCursor = pygame.sprite.Group()
        #self.cursor = other.Mouse((0,0))
        #self.grpCursor.add(self.cursor)
        
    '''def paint(self, screen):
        screen.fill(conf.color_fons)
        screen.blit(self.image, (0,0))
        self.update(screen)'''
         
    def update(self, screen):
        #variables temporals
        minX, minY, fntSize, maxX = 100, 430, 50, 350
        mx,my = pygame.mouse.get_pos()
        font = pygame.font.SysFont(None, fntSize)

        #Cursor
        #self.cursor.pos = (mx,my)
        #self.cursor.update()

        #Selecció
        posY = minY + fntSize
        if mx > minX and mx < maxX and  my > posY and my < posY + fntSize - 2:
            self.colorList = 1
        else:
            self.colorList = 0

        #Crear llista
        img = font.render('Pantalla inicial', True, self.colors[self.colorList])

        #Desbloquejar finals
        filer = open('state/static.txt','r')
        static = filer.readline()
        filer.close()

        if conf.bolPorta[-2]:
            winText = font.render('Has completat el final CLAUER', True, (255,255,255))
            static = static[0] + '1' + static[2]
            
        elif conf.inter[-1]:
            winText = font.render("Has completat el final CANVI D'OPINIÓ", True, (255,255,255))
            static = static[:2] + '1'
            
        else:
            winText = font.render('Has completat el final CAPITALISTA', True, (255,255,255))
            static = '1' + static[1:]

        filew = open('state/static.txt','w')
        filew.write(static)
        filew.close()

        #Pintar-ho tot
        screen.fill(conf.color_fons)
        screen.blit(self.image, (0,0))
        screen.blit(winText, (minX, minY))
        screen.blit(img, (minX, minY + fntSize))
        
        #self.grpCursor.draw(screen)
        pygame.display.flip()

    def event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and self.colorList == 1:
                return self.game.change_state('MENU')
