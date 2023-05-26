import pygame
import math
import networkx as nx
import random as rd

class Enemic(pygame.sprite.Sprite):

    # Inicialitza els estats. Són nombres enters.
    IDLE, WALK, ATAC = range(3)
    # Inicialitza les transicions
    VES_IDLE, VES_WALK, VES_ATAC = range(3)

    def __init__(self, matriu_imatges, pos, tipus=0):
        super().__init__()
        
        # Defineix l'estat inicial
        self.estat = self.WALK
        self.llista_im = matriu_imatges
        self.count = 0
        self.nframes = len(self.llista_im[0])
        self.image = self.llista_im[self.estat][0] 

        #Mode 0(pathfinding), 1(seguint jugador)
        self.mode = 'path'

        #Inputs mov
        self.playerPos = (0,0)
        self.atac = False
        self.tAtac = 100
        self.cAtac = 0
        self.angle = 0

        #bales
        self.grpBullet = []

        #Atributs
        self.damage = False
        self.tipus = tipus
        self.grpEnemy = []

        #Col·lisions i pathfinding
        self.parets = pygame.sprite.Group()
        self.w, self.h = self.image.get_width(), self.image.get_height()

        #self.graf = nx.Graph()
        self.lPath = []
        self.nextStep = (0,0)
        self.actPunt = ['y',20000]


        '''
        0 -> zombie pochito  (0,1)   -> vel = 1; vida = 2;
        1 -> zombie millorat (2,3,4) -> vel = 1,5  ; vida = 3;
        2 -> zombie tanque   (2,4)   -> vel = 1; vida = 8;
        3 -> zombie ràpid    (3,4)   -> vel = 2  ; vida = 1;
        '''
        self.cVel = 0 #velocitat = vel/(tVel+1)
        if  tipus == 0:#pocho
            self.vida = 3
            self.vel  = 3 #1.5
            self.tVel = 1
            self.mida = 1
            
        elif tipus == 1:#millorat
            self.vida = 5
            self.vel  = 2 #2
            self.tVel = 0
            self.mida = 1

        elif tipus == 2:#ràpid
            self.vida = 3
            self.vel  = 5 #2.5
            self.tVel = 1
            self.mida = 0.8
            
        elif tipus == 3:#tanque
            self.vida = 11
            self.vel  = 1 #.5
            self.tVel = 1
            self.mida = 1.3

        #Moviment random
        self.cRand = 0
        self.tRand = 60/self.vel

        #Raycast
        self.cRay = 0
        self.tRay = 100
        self.bolRay = False

        #Mida nova i posició
        self.w, self.h = int(self.w * self.mida) , int(self.h * self.mida)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rect = self.image.get_rect().move(pos)
        
        self.angleBala = 0        

    def paint(self):
        x, y   = self.rect.center
        self.act_punt(x,y)

    def update(self):

        #Variables
        x, y   = self.rect.center
        px, py = self.playerPos
        sx, sy = self.nextStep

        if self.mode == 'path':
            ax,ay = sx,sy
        elif self.mode == 'player':
            ax,ay = px,py

        #Velocitat
        mult = 1
        if self.tVel != 0:   #Velocitat entre 0 i 1
            if self.cVel <= 0:
                self.cVel  = self.tVel
                mult = 1
            else:
                self.cVel -= 1
                mult = 0
        
        #Canvi de frame
        self.count = self.count + 1
        if self.count == self.nframes * 10:
            self.count = 0
        fila = self.estat
        columna = self.count // 10
        self.image = self.llista_im[fila][columna]
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
                    
        #Col·lisió amb bales
        lista_impactos_balas = pygame.sprite.spritecollide(self, self.grpBullet, False)
        for bala in lista_impactos_balas:
            bx, by = bala.rect.center
            radi = 36*self.mida
            
            if self.mag(bx-x, by-y) < radi and not bala.bolDed:
                self.damage = True
                self.angleBala = bala.angle
                bala.ded(1)

        #Rotació
        imRot = -math.atan2(ay-y, ax-x)
        self.angle  = -math.atan2(ay-y, ax-x)  #radiants 
        self.image, self.rect = self.rot_centre(self.image, self.rect, imRot* 180/math.pi)

        #Moviment
        eps = .1
        epsR = 60
        
        if self.cRand <= 0:
            self.vRandom = rd.randint(0, 100)*rd.randint(-1,1)
            self.cRand = self.tRand
            
            if abs(self.vRandom)>epsR:
                self.vRandom = math.copysign(1,self.vRandom)
            else:
                self.vRandom = 0
        self.cRand -= 1
        
        if abs(math.cos(self.angle)) > eps:
            vx = math.copysign(1,(ax-x))
        else:
            vx = self.vRandom

        if abs(math.sin(self.angle)) > eps:
            vy = math.copysign(1,(ay-y))
        else:
            vy = self.vRandom

        epsD = 40 * self.mida + 15 / self.mida
        if self.mag(px-x, py-y) < epsD and self.mode == 'player':
            self.canvia_estat(self.VES_ATAC)
            vx = 0
            vy = 0
       
        #Col·lisió amb parets
        rx = x + vx * self.vel * mult
        ry = y + vy * self.vel * mult
        
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.parets, False)
        for bloque in lista_impactos_bloques:
            dif = .7
            eps  = self.vel * mult + 1 #pixels de diferencia
            
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

        #Animació
        if (vx != 0 or vy != 0):
            #Si està atacant acaba de fer-ho
            if self.estat == self.ATAC:
                if self.count == 0:
                    self.canvia_estat(self.VES_WALK)
                else:
                    vx,vy = 0,0
            else:
                self.canvia_estat(self.VES_WALK)
        #else:
            #self.canvia_estat(self.VES_IDLE)

        #Moviment final
        self.rect.center = (rx,ry)
        
        #Atacar
        if self.atac:
            self.atac = False

        #Damage
        if self.damage:
            self.damage = False
            self.vida -= 1

        #Pathfinding
        eps2 = 5
        self.act_punt(x,y)

        if self.actPunt[1] < eps2:
            if self.actPunt[0] in self.lPath and len(self.lPath) > 1:
                self.lPath.remove(self.actPunt[0])
                self.nextStep = self.graf.nodes[self.lPath[0]]['pos']

        if len(self.lPath) == 0:
            self.canvia_estat(self.VES_IDLE)

        #Raycast
        if self.cRay <= 0:
            self.cRay = self.tRay
            self.rayCastPlayer()
            self.mode = 'player'
            if self.bolRay:
                self.mode = 'path'
                self.canvia_path(self.lPath[-1])
                
        self.cRay -= 1
        
            
    def canvia_estat(self, transicio=None):

        estat_anterior = self.estat
        if transicio == self.VES_WALK:
            self.estat = self.WALK
        elif transicio == self.VES_IDLE:
            self.estat = self.IDLE
        elif transicio == self.VES_ATAC:
            self.estat = self.ATAC
        else:
            raise ValueError('Transició {} desconeguda'.format(transicio))
        if self.estat != estat_anterior:
            self.count = 0

    def rot_centre(self, image, rect, angle):
        #ROTACIÓ en el centre de la imatge
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

    def mag(self, vx, vy):
        return (vx**2 + vy**2)**(1/2)

    def canvia_path(self, objectiu):
        pAct = nx.shortest_path(self.graf, self.actPunt[0], objectiu)
        
        if len(self.lPath) > 0:
            pSeg = nx.shortest_path(self.graf, self.lPath[0], objectiu)
            if len(pAct) < len(pSeg):
                self.lPath = pAct
            else:
                self.lPath = pSeg 
        else:
            self.lPath = pAct
            
        self.nextStep = self.graf.nodes[self.lPath[0]]['pos']

    def act_punt(self,x,y):
        ptx, pty = self.graf.nodes[self.actPunt[0]]['pos']
        self.actPunt[1] = self.mag(ptx-x, pty-y)
        
        for punt in self.graf.nodes:
            ptx, pty = self.graf.nodes[punt]['pos']
            d = self.mag(ptx-x, pty-y)
            
            if d < self.actPunt[1]:
                self.actPunt = [punt,d]

    def rayCastPlayer(self):
        #Raycast
        x, y   = self.rect.center
        px, py = self.playerPos
        
        dx,dy = px-x, py-y
        
        inicial = 0
        actual = inicial
        final = self.mag(dx, dy)
        pas = 32

        self.bolRay = False
        
        while(self.mag(actual*pas* dx/final, actual*pas* dy/final) < final and not self.bolRay):  
            rayX,rayY = x + actual*pas* dx/final, y + actual*pas* dy/final
            
            for bloque in self.parets:
                oLeft,  oTop = bloque.rect.topleft
                oRight, oBot = bloque.rect.bottomright

                if rayX >= oLeft and rayX <= oRight and rayY >= oTop and rayY <= oBot:
                    self.bolRay = True
                    
            actual += 1
