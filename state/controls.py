#Mòduls
import pygame
from pygame.locals import *
from pgu import engine
import conf
import other

class Controls(engine.State): # ---------------------- CONTROLS ---------------------- #
    
    def init(self):
        self.image = pygame.image.load("imag/controls.png").convert_alpha()
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
        minX, minY, fntSize, maxX = 20, 30, 50, 300
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

        #Pintar-ho tot
        screen.fill(conf.color_fons)
        screen.blit(self.image, (0,0))
        screen.blit(img, (minX, minY + fntSize))
        
        #self.grpCursor.draw(screen)
        pygame.display.flip()

    def event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and self.colorList == 1:
                return self.game.change_state('MENU')
        if event.type == KEYDOWN:
            if event.key == pygame.K_p or event.key == K_ESCAPE:
                return self.game.change_state('MENU')
