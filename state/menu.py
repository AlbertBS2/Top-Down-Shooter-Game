#Mòduls
import pygame
from pygame.locals import *
from pgu import engine
import conf
import other

class Menu(engine.State): # ---------------------- MENU PRINCIPAL ---------------------- #
    
    def init(self):
        self.image = pygame.image.load("imag/menu.png").convert_alpha()
        self.colors = ((10,10,10),(255,255,255))
        self.colorList = [0,0,0]
        self.selected = -1
        self.state = ['JUGANT', 'CONTROLS', 'QUIT']

        #Cursor
        #self.grpCursor = pygame.sprite.Group()
        #self.cursor = other.Mouse((0,0))
        #self.grpCursor.add(self.cursor)
         
    def update(self, screen):
        #variables temporals
        minX, minY, fntSize, maxX = 30, 400, 50, 200
        mx,my = pygame.mouse.get_pos()
        font = pygame.font.SysFont(None, fntSize)
        fnt2 = pygame.font.SysFont(None, fntSize-20)

        #Cursor
        #self.cursor.pos = (mx,my)
        #self.cursor.update()
       
        #Selecció
        for i in range(3):
            posY = minY + fntSize*i
            if mx > minX and mx < maxX and  my > posY and my < posY + fntSize - 2:
                self.selected = i
                break
            else:
                self.selected = -1

        self.colorList = [0,0,0]
        if self.selected != -1:
            self.colorList[self.selected] = 1

        #Crear llista
        img = [font.render('Jugar', True, self.colors[self.colorList[0]]),
            font.render('Controls', True, self.colors[self.colorList[1]]),
            font.render('Sortir', True, self.colors[self.colorList[2]])]

        #Finals
        filer = open('state/static.txt','r')
        static = filer.readline()
        colWin = []
        for i in static:
            colWin.append(self.colors[int(i)])
        filer.close()

        txtWin = [fnt2.render("CAPITALISTA", True, colWin[0]),
                  fnt2.render("CLAUER", True, colWin[1]),
                  fnt2.render("CANVI D'OPINIO", True, colWin[2])]

        #Pintar-ho tot
        screen.fill(conf.color_fons)
        screen.blit(self.image, (0,0))
        for i in range(3):
            screen.blit(txtWin[i], (minX + 200*i - 25*i**2, 580))
            screen.blit(img[i], (minX, minY + fntSize*i))

        #Accent a la ó
        screen.blit(fnt2.render('´', True, colWin[2]), (480, 575)) 

        
        #self.grpCursor.draw(screen)
        pygame.display.flip()

    def event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and self.selected != -1:
                return self.game.change_state(self.state[self.selected])
