#Mòduls
import pygame
from pygame.locals import *
from pgu import engine
import conf


class Final(engine.State): # ---------------------- GAME OVER ---------------------- #

    def init(self):
        self.image = pygame.image.load("imag/final.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (960, 630))
        self.colors = ((150,150,150),(250,250,250))
        self.colorList = [0,0]
        self.selected = -1
        self.state = ['JUGANT','MENU']
        self.surface = pygame.surface

        #Cursor
        #self.grpCursor = pygame.sprite.Group()
        #self.cursor = other.Mouse((0,0))
        #self.grpCursor.add(self.cursor)

    def paint(self,screen):
        s = pygame.Surface((screen.get_width(), screen.get_height()))  # the size of your rect
        s.set_alpha(100)                # alpha level
        s.fill((0,0,0))           # this fills the entire surface
        
        screen.blit(s, (0,0))    # (0,0) are the top-left coordinates
        
        w, h = self.image.get_width(), self.image.get_height()
        screen.blit(self.image,(0,0))#, (screen.get_width()/2 - w/2,screen.get_height()/3 - h/2))
        self.update(screen)
         
    def update(self, screen):
        #variables temporals
        minX, minY, fntSize, maxX = 30, 530, 50, 300
        mx,my = pygame.mouse.get_pos()
        font = pygame.font.SysFont(None, fntSize)

        #Cursor
        #self.cursor.pos = (mx,my)
        #self.cursor.update()
       
        #Selecció
        for i in range(2):
            posY = minY + fntSize*i
            if mx > minX and mx < maxX and  my > posY and my < posY + fntSize - 2:
                self.selected = i
                break
            else:
                self.selected = -1

        self.colorList = [0,0]
        if self.selected != -1:
            self.colorList[self.selected] = 1

        #Crear llista
        img = [font.render('Reintentar', True, self.colors[self.colorList[0]]),
            font.render('Pantalla inicial', True, self.colors[self.colorList[1]])]

        #Pintar-ho tot
        #screen.fill(conf.color_fons)
        screen.fill((20,20,20), (0, screen.get_height()*4/5, screen.get_width(), screen.get_height()))
        #screen.fill((20,20,20), (0, screen.get_height()*4/5, screen.get_width(), screen.get_height()))
        #screen.blit(self.image, (0,0))
        
        for i in range(2):
            screen.blit(img[i], (minX, minY + fntSize*i))
            
        #self.grpCursor.draw(screen)
        pygame.display.flip()

    def event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and self.selected != -1:
                return self.game.change_state(self.state[self.selected])   
