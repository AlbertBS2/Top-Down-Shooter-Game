import pygame
import math
import conf

class Animacio(pygame.sprite.Sprite):

    # Inicialitza els estats. Són nombres enters.
    IDLE, WALK = range(2)
    # Inicialitza les transicions
    VES_IDLE, VES_WALK = range(2)

    def __init__(self, matriu_imatges, pos):
        super().__init__()
        
        # Defineix l'estat inicial
        self.estat = self.IDLE
        self.llista_im = matriu_imatges
        self.count = 0
        self.nframes = len(self.llista_im[0])
        self.image = self.llista_im[self.estat][0] 
        self.rect = self.image.get_rect().move(pos)

        #Inputs mov
        self.up, self.down, self.left, self.right = 0,0,0,0
        self.vel = 3

        self.mousePos = pygame.mouse.get_pos()
        self.angle = 0

        #Disparar
        self.shoot = False
        self.canShoot = True
        self.tShoot = 3
        self.cShoot = 0

        #Atributs
        self.maxVida = 5
        self.vida   = self.maxVida
        self.damage = False
        self.tInv = 60    #Invencible durant un rato despres que et peguen
        self.cInv = 0

        self.reload = False
        self.maxBales   = 10
        self.totBales   = 100
        self.bales      = 10

        #Col·lisions
        self.parets = pygame.sprite.Group()
        self.portes = pygame.sprite.Group()
        self.portaID = ''
        self.w, self.h = self.image.get_width(), self.image.get_height()

        #Monedes
        self.diners = 0 #+1000

    def update(self):
        
        #Canvi de frame
        self.count = self.count + 1
        if self.count == self.nframes * 10:
            self.count = 0
        fila = self.estat
        columna = self.count // 10
        self.image = self.llista_im[fila][columna]

        #Rotació
        x, y   = self.rect.center
        mx, my = self.mousePos
        self.angle = -math.atan2(my-y, mx-x) #radiants
        self.image, self.rect = self.rot_centre(self.image, self.rect, self.angle * 180/math.pi)

        #Moviment
        vx, vy = self.right - self.left, self.down - self.up
        rx = x + vx * self.vel
        ry = y + vy * self.vel
       
        #Col·lisions amb parets
        bloc_col = pygame.sprite.spritecollide(self, self.parets, False)
        for bloque in bloc_col:
            dif = 0.7
            eps  = self.vel + 1 #pixels de diferencia
            
            pLeft,  pTop = x - self.w/2 * dif, y - self.h/2 * dif
            pRight, pBot = x + self.w/2 * dif, y + self.h/2 * dif

            oLeft,  oTop = bloque.rect.topleft
            oRight, oBot = bloque.rect.bottomright
            
            if abs(pLeft - oRight) < eps and vx < 0:
                if (pTop - oBot) * (pBot - oTop) < 0:
                    rx = oRight + self.w/2 * dif + 1
                
            if abs(pRight - oLeft) < eps and vx > 0:
                if (pTop - oBot) * (pBot - oTop) < 0:
                    rx = oLeft - self.w/2 * dif - 1
                
            if abs(pTop - oBot) < eps and vy < 0:
                if (pLeft - oRight) * (pRight - oLeft) < 0:
                    ry = oBot + self.h/2 * dif + 1
                
            if abs(pBot - oTop) < eps and vy > 0:
                if (pLeft - oRight) * (pRight - oLeft) < 0:
                    ry = oTop - self.h/2 * dif - 1

        #Col·lisió amb portes
        porta_col = pygame.sprite.spritecollide(self, self.portes, False)
        self.portaID = -1
        if len(porta_col) > 0:
            for i in range(len(conf.strPorta)):
                if conf.strPorta[i] == porta_col[0].id:
                    self.portaID = i        

        #Animació               
        if rx != x or ry != y:
            self.canvia_estat(self.VES_WALK)
        else:
            self.canvia_estat(self.VES_IDLE)

        self.rect.center = (rx,ry)

        #Recargar
        if self.reload:
            self.reload = False
            if self.bales < self.maxBales and self.totBales > 0:
                self.bales    += 1
                self.totBales -= 1
        
        #Disparar
        if self.cShoot > 0:
            self.cShoot -= 1
            self.canShoot = False
        else:
            self.canShoot = True

        if self.bales > 0:
            if self.shoot:
                self.shoot = False
                self.bales -= 1
                self.cShoot = self.tShoot
        else:
            self.canShoot = False

        #Damage
        #prevIm = self.image
        if self.damage:
            self.damage = False
            if self.cInv == 0:
                self.vida -= 1
                self.cInv = self.tInv
                
        if self.cInv > 0:
            self.cInv -= 1
            #self.image = None
        #else:
            #self.image = prevIm
        
    def canvia_estat(self, transicio=None):

        estat_anterior = self.estat
        if transicio == self.VES_WALK:
            self.estat = self.WALK
        elif transicio == self.VES_IDLE:
            self.estat = self.IDLE
        else:
            raise ValueError('Transició {} desconeguda'.format(transicio))
        if self.estat != estat_anterior:
            self.count = 0

    def rot_centre(self, image, rect, angle):
        #ROTACIÓ en el centre de la imatge
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
