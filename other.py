import pygame
import conf
import math

#RATOLÍ
class Mouse(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(conf.sprite_mouse)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        
    def update(self):
        self.rect.center = self.pos

#IMATGE ESTÀTICA
class Back(pygame.sprite.Sprite):
    def __init__(self, imatge, pos):
        super().__init__()
        self.image = pygame.image.load(imatge).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos

#BALA
class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos, rot):
        super().__init__()
        self.image = pygame.image.load(conf.sprite_bullet)
        self.angle = rot
        self.image = pygame.transform.rotate(self.image, rot*180/math.pi)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.vel = 8
        self.vx =  round(math.cos(rot)*self.vel)
        self.vy = -round(math.sin(rot)*self.vel)
        self.bolDed = False
        self.counter = 300
        self.c = 0
        
    def update(self):
        #Moviment
        pos = list(self.rect.center)
        pos[0] += self.vx
        pos[1] += self.vy
        self.rect.center = tuple(pos)

        if self.c >= self.counter:
            self.kill()
        self.c += 1

    def ded(self, time = 0):
        self.bolDed = True
        self.c = 0
        self.counter = time

#PROGRESS BAR
class ProgressBar(pygame.sprite.Sprite):

    def __init__(self, pos, amplada, alçada, color, color_fons):
        super().__init__()
        self.image = pygame.Surface((amplada, alçada))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.image.fill(color)
        self.percent = 100.0
        self.color1 = color
        self.color2 = color_fons

    def update(self):
        self.image.fill(self.color2)
        ple = (self.percent/100.0) * self.rect.width
        r = pygame.Rect((0,0), (ple, self.rect.height))
        self.image.fill(self.color1, r)

class Rectangle(pygame.sprite.Sprite):
    
    def __init__(self, pos, amplada, alçada, color):
        super().__init__()
        self.image = pygame.Surface((amplada, alçada))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.image.fill(color)
        self.color = color
        
    def update(self):
        self.image.fill(self.color)

class Blood(pygame.sprite.Sprite):
    def __init__(self, pos, angle, mtImatges, tipus, mida):
        super().__init__()
        self.tipus = tipus
        self.mtIm = mtImatges
        self.image = self.mtIm[self.tipus][0]
        self.angle = angle

        self.rect = self.image.get_rect()
        self.pos = (pos[0]+64*math.cos(angle), pos[1]-64*math.sin(angle))
        w, h = self.image.get_width(), self.image.get_height()
        self.novaMida = int(w*mida), int(h*mida  )      

        self.tFrame = 3
        self.cFrame = self.tFrame
        self.frame = 0
        
    def update(self):
        if self.frame < 2:
            self.cFrame -= 1
            if self.cFrame <= 0:
                self.frame += 1
                self.cFrame = self.tFrame
            self.image = self.mtIm[self.tipus][self.frame].convert_alpha()
            self.image = pygame.transform.scale(self.image, self.novaMida)
            self.image = pygame.transform.rotate(self.image, self.angle*180/math.pi)
            self.rect = self.image.get_rect()
            
            self.rect.center = self.pos
            

#Col·leccionable
class Interectuable(pygame.sprite.Sprite):

    def __init__(self, pos, mtIm, inter, preu = 0):
        super().__init__()
        self.estat = 0
        self.mtIm  = mtIm
        self.image = self.mtIm[0][self.estat]
        self.rect  = self.image.get_rect()
        self.rect.center = pos
        self.inter = inter
        self.preu = preu

    def update(self):
        if self.estat < 2:
            self.image = self.mtIm[0][self.estat]
        else:
            conf.inter[self.inter] = 1
            self.kill()

class Porta(pygame.sprite.Sprite):
    def __init__(self, lPos, ID):
        super().__init__()
        self.id = ID
        x,y,w,h = lPos[0].rect
        xMin, yMin = x, y
        xMax, yMax = x + w, y + h
        for i in lPos:
            x,y,w,h = i.rect
            if x < xMin:
                xMin = x
            if y < yMin:
                yMin = y
            if x + w > xMax:
                xMax = x + w
            if y +  h > yMax:
                yMax = y + h

        w,h = xMax-xMin, yMax-yMin
        eps = 2
        
        self.image = pygame.Surface((w + eps*2, h + 2*eps))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = xMin - eps, yMin  - eps

        #color
        alpha = 150
        color = (250,250,250)
        if ID == '!':
            color = (100,100,255)
        elif ID == '(':
            color = (255,150,150)
        elif ID == '/':
            color = (150,255,150)

        self.image.set_alpha(alpha)
        self.image.fill(color)
        


        
    
    
