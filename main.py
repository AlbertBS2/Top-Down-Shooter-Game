# Pygame
import pygame
from pygame.locals import *

# PGU
from pgu import engine

#Networkx
import networkx as nx

#Random
from random import randint as rdInt

# Mòduls propis
import conf
from sprite_sheets import *

import player
import enemy
from other import *
from camera import *

#Estats del joc
from state.pause    import Pause
from state.final    import Final
from state.controls import Controls
from state.menu     import Menu
from state.win      import Win


# Classe joc
class Joc(engine.Game):

    # Initialize screen, pygame modules, clock... and states.
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(conf.mides_pantalla, SWSURFACE)
        self.crono = pygame.time.Clock()
        self._init_state_machine()
        pygame.font.init()
        pygame.display.set_caption('NOM PROVISIONAL')#Títol
        pygame.display.set_icon(pygame.image.load(conf.sprite_mouse))

        #pygame.mixer.pre_init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(20)
        pygame.mixer.music.load(conf.music)
        pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.
        #pygame.mouse.set_visible(False)  # hide the cursor

    # Creates and stores all states as attributes
    def _init_state_machine(self):
        self.jugant     = Jugant(self)
        self.pause      = Pause(self)
        self.menu       = Menu(self)
        self.quit_state = engine.Quit(self)
        self.final      = Final(self)
        self.win        = Win(self)
        self.controls   = Controls(self)

    # Calls the main loop with the initial state.
    def run(self): 
        super().run(self.menu, self.screen)   #jugant --> menu

    # Tick is called once per frame. It shoud control de timing.
    def tick(self):
        self.crono.tick(conf.fps)   # Limits the maximum FPS
        #print(self.crono.get_fps())

    def change_state(self, transition=None):
        pygame.mouse.set_visible(True) #ensenya cursor
        #print(transition)
        
        if self.state is self.menu:
            if transition == 'JUGANT':  #Reiniciar joc
                pygame.mouse.set_visible(False)  # hide the cursor
                self.rePortes()
                new_state = self.jugant
                new_state.init()
                
            elif transition == 'CONTROLS':
                new_state = self.controls
                
            elif transition == 'QUIT':
                new_state = self.quit_state
                
            else:
                print("error: no s'ha trobat una transició a: " + transition)

        if self.state is self.pause:    #Continuar joc
            if transition == 'JUGANT':
                pygame.mouse.set_visible(False)  # hide the cursor
                new_state = self.jugant
                
            elif transition == 'MENU':
                new_state = self.menu

        if self.state is self.jugant:
            if transition == 'PAUSE':
                new_state = self.pause
                
            elif transition == 'FINAL':
                new_state = self.final

            elif transition == 'WIN':
                new_state = self.win

        if self.state is self.final or self.state is self.win:
            if transition == 'JUGANT':  #Reiniciar joc
                pygame.mouse.set_visible(False)  # hide the cursor
                self.rePortes()
                new_state = self.jugant
                new_state.init()
                
            elif transition == 'MENU':
                new_state = self.menu
                
        if self.state is self.controls: #Tornar al menu
            new_state = self.menu
            
        return new_state

    def rePortes(self):
        #Reiniciar portes i interectuables
        for i in range(len(conf.inter)):
            if conf.inter[i] != 0:
                conf.inter[i] = 0

        for i in range(len(conf.bolPorta)):
            if conf.bolPorta[i] != 0:
                conf.bolPorta[i] = 0
        
class Jugant(engine.State): # ---------------------- JUGANT ---------------------- #

    #Inici
    def init(self):
    #PLAYER
        sprPlayer       = pygame.image.load(conf.sprite_sheet_player)
        self.grpPlayer  = pygame.sprite.Group() # grup de Sprites
        mtPlayer        = crea_matriu_imatges(sprPlayer, *conf.mides_sprite_sheet_player)
        self.player     = player.Animacio(mtPlayer, (100,300))#conf.posicio_player)
        self.grpPlayer.add(self.player)

    #BALES
        self.grpBullet  = pygame.sprite.Group() # grup de Sprites

    #PARETS
        self.grpWall = pygame.sprite.Group() # grup de Sprites
        self.grpBG   = pygame.sprite.Group()

        #Crear mapa i camins per l'enemic
        mapa = conf.mp
        bw, bh = 48,48
        self.maxMapa = ((len(mapa[0])-1) * bw, (len(mapa)-1) * bh)

        self.graf = nx.Graph()
        self.prevPunt = 'z'
        #self.graf.add_nodes_from(conf.nodes)

        self.dPortes = {}
        
        for y in range(len(mapa)):
            for x in range(len(mapa[0])):
                if mapa[y][x] == '1':
                    bloc = Back(conf.sprite_ref, (x * bw, y * bh))
                    self.grpWall.add(bloc)

                elif mapa[y][x] == '3':
                    trap = Back(conf.sprite_tramp, (x * bw, y * bh))
                    self.grpBG.add(trap)                    

                elif mapa[y][x].isalpha():  #Posició de cada punt del graf
                    self.graf.add_node(mapa[y][x], pos = (x * bw, y * bh))

                elif not mapa[y][x].isalnum():
                    bloc = Back(conf.sprite_ref, (x * bw, y * bh))
                    self.grpWall.add(bloc)
                    
                    if mapa[y][x] in self.dPortes:
                        self.dPortes[mapa[y][x]].append(bloc)
                    else:
                        self.dPortes[mapa[y][x]] = [bloc]       

        self.graf.add_edges_from(conf.edges) #Unió de punts

        #import matplotlib.pyplot as plt
        #nx.draw_networkx(self.graf)
        #plt.show()
        
    #PORTES
        self.grpPorta = pygame.sprite.Group() # grup de Sprites
        
        for i in self.dPortes:
            l = self.dPortes[i]
            porta = Porta(l,i)

            self.dPortes[i].append(porta)
            self.grpPorta.add(porta)

    #INTERACTUABLES (portes, pistola, curació, claus, munició)
        self.grpInter = pygame.sprite.Group() # grup de Sprites

        pMun  = [(398,515), (790,437), (1735,600), (766,861)]
        pVida = [(1297,450), (1852,363), (1819,885)]
        pClau = [(1765,363), (1864,600), (577, 881)]
        for i in pMun:
            sprMunicio = pygame.image.load(conf.inter_mun)
            mtMunicio  = crea_matriu_imatges(sprMunicio, 1, 2)
            self.grpInter.add(Interectuable(i, mtMunicio, 0))
            
        for i in pVida:
            sprVida = pygame.image.load(conf.inter_vida)
            mtVida  = crea_matriu_imatges(sprVida, 1, 2)
            self.grpInter.add(Interectuable(i, mtVida, 1))

        for i in range(len(pClau)):
            sprClau = pygame.image.load(conf.inter_clau[i])
            mtClau  = crea_matriu_imatges(sprClau, 1, 2)
            self.grpInter.add(Interectuable(pClau[i], mtClau, i + 2))

        self.bolInter = False
        self.intPreu  = 0
            

    #GUI
        self.grpGui  = pygame.sprite.Group()
        self.pbVida  = ProgressBar((24, 14),170, 18,(200, 70, 70), (50, 50, 50))
        self.pbBales = ProgressBar((24, 48),170, 18,(70, 70, 200), (50, 50, 50))

        barra_n1     = Rectangle((22, 12),174, 22,(0, 0, 0))
        barra_n2     = Rectangle((22, 46),174, 22,(0, 0, 0))
        self.cursor  = Mouse((0,0))
        vida_icon    = Back(conf.vida_icon, (21, 23))
        bullet_icon  = Back(conf.bullet_icon, (21, 57))

        self.grpGui.add(barra_n1)
        self.grpGui.add(barra_n2)
        self.grpGui.add(self.pbVida)
        self.grpGui.add(self.pbBales)
        self.grpGui.add(self.cursor)
        self.grpGui.add(vida_icon)
        self.grpGui.add(bullet_icon)

    #ENEMICS
        self.grpEnemy = pygame.sprite.Group() # grup de Sprites
        self.pSpawn = conf.pSpawn0

        self.cSpawn = 500 #+10000000
        self.tSpawn = 300

    #BLOOD
        self.grpBlood = pygame.sprite.Group() # grup de Sprites

    #ALTRES
        #Camera
        w,h = conf.mides_pantalla
        self.camera = [0,0,w,h]

        #Efectes de so
        self.sndShot  = pygame.mixer.Sound(conf.snd_shot)
        self.sndFShot = pygame.mixer.Sound(conf.snd_no_shot)
        self.sndOpen  = pygame.mixer.Sound(conf.snd_open)
        self.sndLock  = pygame.mixer.Sound(conf.snd_lock)
        self.sndPick  = pygame.mixer.Sound(conf.snd_pick)
        self.sndHit   = pygame.mixer.Sound(conf.snd_hit)
        self.sndDead  = pygame.mixer.Sound(conf.snd_dead)

        #Parets player i enemics
        self.player.parets = self.grpWall
        self.player.portes = self.grpPorta

        #Alertes
        self.cAlerta = 0
        self.tAlerta = 180
        self.sAlerta =  ''

    def paint(self,screen): #un cop cada cop que torna al estat
        #Reiniciar controls
        self.player.up    = 0
        self.player.down  = 0
        self.player.right = 0
        self.player.left  = 0
        self.player.mousePos = pygame.mouse.get_pos()
        
        self.update(screen)

    def event(self,event):
        #Declarar diferents inputs
        if event.type == KEYDOWN or event.type == KEYUP:
            up    = event.key == pygame.K_w or event.key == pygame.K_UP
            down  = event.key == pygame.K_s or event.key == pygame.K_DOWN
            right = event.key == pygame.K_d or event.key == pygame.K_RIGHT
            left  = event.key == pygame.K_a or event.key == pygame.K_LEFT

        #Moviment
        if event.type == KEYDOWN:
            if up:
                self.player.up    = 1
            if down:
                self.player.down  = 1
            if right:
                self.player.right = 1
            if left:
                self.player.left  = 1

            #Pause
            if event.key == pygame.K_p or event.key == K_ESCAPE:
                return self.game.change_state('PAUSE')

            #interactuables
            if event.key == K_SPACE:
                for inter in self.grpInter:
                    if self.player.diners >= inter.preu and inter.estat == 1:
                        inter.estat = 2
                        self.player.diners -= inter.preu
                        self.tocaSo(self.sndPick)


                ID = self.player.portaID
                if ID != -1: #Obrir portes amb diners o claus
                    if isinstance(conf.preuPorta[ID],int):
                        if self.player.diners >= conf.preuPorta[ID]:
                            conf.bolPorta[ID] = 1
                            self.player.diners -= conf.preuPorta[ID]
                            self.tocaSo(self.sndOpen)
                            
                        else:
                            self.cAlerta = self.tAlerta
                            self.sAlerta =  'Em falten diners'
                            self.tocaSo(self.sndLock)
                    else:
                        clau = int(conf.preuPorta[ID][-1])
                        if conf.inter[clau] == 1:
                            conf.bolPorta[ID] = 1
                            self.tocaSo(self.sndOpen)

                        else:
                            self.cAlerta = self.tAlerta
                            self.sAlerta =  'Em falta la clau'
                            self.tocaSo(self.sndLock)
            
        if event.type == KEYUP:
            if up:
                self.player.up    = 0
            if down:
                self.player.down  = 0
            if right:
                self.player.right = 0
            if left:
                self.player.left  = 0

        #Disparar i recaregar
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.player.canShoot:
                    self.spawnBullet(self.player.rect.center, self.player.angle)
                    self.player.shoot = True
                    self.tocaSo(self.sndShot)
                    
                elif self.player.bales == 0:
                    self.tocaSo(self.sndFShot)

            elif event.button == 4 or event.button == 5:
                self.player.reload = True 
    
    def loop(self):
        #Indicador de vida
        self.pbVida.percent  = 100*self.player.vida/self.player.maxVida
        self.pbBales.percent = 100*self.player.bales/self.player.maxBales
        
        #Donar pos player als enemics i mirar si estan atacant
        posPlayer = self.player.rect.center
        actPunt = ['a',20000]

        for punt in self.graf.nodes:
            ptx, pty = self.graf.nodes[punt]['pos']
            plx, ply = posPlayer
            dx, dy = ptx-plx, pty-ply
            d = (dx**2 + dy**2)**(1/2)
            
            if d < actPunt[1]:
                actPunt = [punt,d] 
        
        for enem in self.grpEnemy:
            enem.playerPos = posPlayer
            enem.grpBullet = self.grpBullet
            
            if enem.estat == enem.ATAC and enem.count == 0: #ATAC ENEMIC
                self.player.damage = True

            if enem.vida <= 0:#Guanyar punts quan mates un enemic
                self.player.diners += 10 + 5*enem.tipus
                self.spawnBlood(enem.rect.center, enem.angleBala)
                self.tocaSo(self.sndDead)
                enem.kill()

            if actPunt[0] != self.prevPunt:
                enem.canvia_path(actPunt[0])

        if actPunt[0] != self.prevPunt:
            self.prevPunt = actPunt[0]

        if self.player.damage and self.player.cInv == 0:
            self.tocaSo(self.sndHit)                

        #Posició del mouse
            #en la camera
        mousePos = pygame.mouse.get_pos()
        self.cursor.pos = mousePos

            #en el world
        mousePos = (mousePos[0] + self.camera[0], mousePos[1] + self.camera[1])
        self.player.mousePos = mousePos

        #update dels sprites (crida la funcio que defineix cada sprite)
        self.grpWall.update()
        self.grpBG.update()
        self.grpPlayer.update()
        self.grpEnemy.update()
        self.grpGui.update()
        self.grpInter.update()
        self.grpBullet.update()
        self.grpBlood.update()

        #Moviment de la càmera
        '''si t'apropes a uns límits de la pantalla la càmera es mourà per
        mantenir al player visible'''
        epsx, epsy = 450, 300
        vel = self.player.vel
        
        wrldLim    = [(0,0),self.maxMapa]#[(0,0),(3*conf.mides_pantalla[0],1.5*conf.mides_pantalla[1])]
        camLim    = [(epsx,epsy),(self.camera[2]-epsx,self.camera[3]-epsy)]
        
        camPlayer = (posPlayer[0] - self.camera[0], posPlayer[1] - self.camera[1])
        wrldCam   = [(self.camera[0],self.camera[1]),
                      (self.camera[0] + self.camera[2], self.camera[1] + self.camera[3])]

        if   wrldCam[0][0] > wrldLim[0][0] and camPlayer[0] < camLim[0][0]:#esquerra
            self.camera[0] -= vel
        elif wrldCam[1][0] < wrldLim[1][0] and camPlayer[0] > camLim[1][0]:#dreta
            self.camera[0] += vel

        if   wrldCam[0][1] > wrldLim[0][1] and camPlayer[1] < camLim[0][1]:#dalt
            self.camera[1] -= vel
        elif wrldCam[1][1] < wrldLim[1][1] and camPlayer[1] > camLim[1][1]:#baix
            self.camera[1] += vel

        #SPAWN ENEMY
        self.tSpawn = 300
            
        nEnemics,mEnemics = len(self.grpEnemy), 40
        nPortes, mPortes  = 9 - len(self.grpPorta), -20
        nDiners, mDiners  = self.player.diners, -1/2
        nClaus, mClaus    = 0, -30
        for i in conf.inter[2:]:
            if i:
                nClaus += 1
 
        self.cSpawn -= 1
        sumatori = nEnemics * mEnemics + nPortes * mPortes + nDiners * mDiners + nClaus * mClaus
        tSpawnFinal = self.tSpawn + int(sumatori)
        
        if self.cSpawn <= 0 :
            posibleSpawn = []

            #Tipus de zombie en funcio del tamps d'espera
            if tSpawnFinal > 220:
                zombie = 0
            elif tSpawnFinal > 150:
                zombie = 1
            else:
                zombie = rdInt(1,3)

            #Spawn a un lloc on no es vegi amb la camera
            for pos in self.pSpawn:
                cx1, cy1 = wrldCam[0]
                cx2, cy2 = wrldCam[1]
                x, y     = pos
                r = 70
                if x + r < cx1 or y  + r < cy1 or x - r > cx2 or y - r > cy2:
                    posibleSpawn.append(pos)

            #Spawn final
            if len(posibleSpawn) > 0:                
                self.cSpawn = tSpawnFinal
                spawn = posibleSpawn[rdInt(0,len(posibleSpawn) - 1)]
                self.spawnEnemy(spawn,zombie)

        #INTERACTUABLES
        self.bolInter = False
        self.intPreu = 0
        
        
        posPlayer = self.player.rect.center
        for inter in self.grpInter:
            posI = inter.rect.center
            dx, dy = posPlayer[0]-posI[0], posPlayer[1]-posI[1]
            d = (dx**2 + dy**2)**(1/2)

            epsD = 50
            if d < epsD:
                inter.estat = 1
                self.bolInter = True
                self.bolPreu = inter.preu
            else:
                inter.estat = 0

        interSum = [100, 1]
        
        if conf.inter[0] > 0:#munició
            self.player.totBales += interSum[0]*conf.inter[0]
            conf.inter[0] = 0
            
        if conf.inter[1] > 0:#vida
            if self.player.maxVida - self.player.vida > interSum[1]*conf.inter[1]:
                self.player.vida += interSum[1]*conf.inter[1]
            else:
                self.player.vida = self.player.maxVida
            conf.inter[1] = 0
            
        #Portes
        for i in range(len(conf.bolPorta)):
            if conf.bolPorta[i] == 1:
                self.obrirPorta(conf.strPorta[i])
                conf.bolPorta[i] = 2 #oberta
                
                #Parets al player
                self.player.parets = self.grpWall
                self.player.portes = self.grpPorta

                #Enemics específics de portes
                if conf.strPorta[i] == '"':
                    self.spawnEnemy((1290,417),2)

                if conf.strPorta[i] == '&':
                    self.spawnEnemy((764,877), 3)
                    self.spawnEnemy((95,893) , 3)

        ID = self.player.portaID
        if ID != -1: 
            self.bolInter = True
            if isinstance(conf.preuPorta[ID],int):
                self.intPreu = conf.preuPorta[self.player.portaID]
        
                
    def update(self, screen):
        screen.fill(conf.color_fons)

        #Transformació world -> view + visualització
        grpList = [self.grpBlood, self.grpBG, self.grpWall, self.grpPorta,
                   self.grpEnemy, self.grpInter, self.grpBullet, self.grpPlayer]
        for grup in grpList:
            world_to_view(self.camera,grup)
            grup.draw(screen)

        #Destransformar view -> world
        for grup in grpList:
            view_to_world(self.camera,grup)

        #GUI (grup de sprites)
        self.grpGui.draw(screen)

        #GUI (lletres)       
        BLANC = (255,255,255)
        RED   = (255,100,100)
        NEGRE = (0,0,0)
        font = pygame.font.SysFont(None, 30)
        txt = [font.render(str(self.player.vida) + ' / ' + str(self.player.maxVida),True,BLANC),
            font.render(str(self.player.bales) + ' / ' + str(self.player.totBales),True,BLANC),
            font.render('$ ' + str(self.player.diners),True,NEGRE),
            font.render('$ ' + str(self.player.diners),True,BLANC)]
            #font.render(str(self.player.mousePos),True,NEGRE)]
        
        for i in (0,1):
            screen.blit(txt[i], (50, 14 + 34*i))

        #Monedes
        txtX,txtY = 230,14
        screen.blit(txt[2], (txtX, txtY + 2))
        screen.blit(txt[3], (txtX, txtY))

        #Intercatuar
        txtB = []
        txtN = []
        if self.bolInter:
            txtB.append(font.render('- espai -  per interectuar',True,BLANC))
            txtN.append(font.render('- espai -  per interectuar',True,NEGRE))
            if self.intPreu > 0:
                txtB.append(font.render('Preu: ' + str(self.intPreu),True,BLANC))
                txtN.append(font.render('Preu: ' + str(self.intPreu),True,NEGRE))
                
        for i in range(len(txtN)):
            screen.blit(txtN[i], (3*txtX, txtY + 34*i + 2))
            screen.blit(txtB[i], (3*txtX, txtY + 34*i))

        #Alertes
        tAlerta = [font.render(self.sAlerta,True,NEGRE), font.render(self.sAlerta,True,RED)]
        if self.cAlerta > 0:
            screen.blit(tAlerta[0], (txtX + 80, txtY + 2))
            screen.blit(tAlerta[1], (txtX + 80, txtY))
            self.cAlerta -= 1
            
        #Flip
        pygame.display.flip()

        #GAME OVER
        if self.player.vida <= 0:
            self.pbVida.percent = 0
            self.grpGui.update()
            self.grpGui.draw(screen)
            for i in (0,1):
                screen.blit(txt[i], (50, 15 + 35*i))
            pygame.display.flip()
            return self.game.change_state('FINAL')

        #YOU WIN
        if sum(conf.bolPorta[-2:]): #si alguna de les dos últimes portes està oberta
            return self.game.change_state('WIN')        

    def spawnEnemy(self, pos, tipo = 0):
        sprEnemy = pygame.image.load(conf.sprite_sheet_enemy)
        mtEnemy  = crea_matriu_imatges(sprEnemy, *conf.mides_sprite_sheet_enemy)
        objEnemy = enemy.Enemic(mtEnemy, pos, tipo)

        self.grpEnemy.add(objEnemy)
        objEnemy.parets = self.grpWall
        objEnemy.graf = self.graf
        objEnemy.act_punt(pos[0], pos[1])
        objEnemy.canvia_path(self.prevPunt)

    def spawnBullet(self, pos, angle):
        self.grpBullet.add(Bullet(pos, angle))

    def playSound(self, sound, chanel):
        pygame.mixer.Channel(chanel).play(sound)

    def obrirPorta(self, clauPorta):
        if clauPorta in conf.pSpawn:
            self.pSpawn =  self.pSpawn + conf.pSpawn[clauPorta]
        
        for porta in self.dPortes:
            for bloc in self.dPortes[porta]:
                if porta == clauPorta:
                    bloc.kill()
                    
    def spawnBlood(self, pos, angle):
        tipus    = rdInt(0,2)
        mida     = rdInt(8,12)/10
        sprBlood = pygame.image.load(conf.sprite_sheet_blood)
        mtBlood  = crea_matriu_imatges(sprBlood, *conf.mides_sprite_sheet_blood)
        
        objBlood = Blood(pos, angle, mtBlood, tipus, mida)
        self.grpBlood.add(objBlood)

    def tocaSo(self, snd):
        for i in range(8):
            if not pygame.mixer.Channel(i).get_busy():
                pygame.mixer.Channel(i).play(snd)
                break

# Programa principal
def main():
    global game
    game = Joc()
    game.run()
    

if __name__ == '__main__':
     main()
pygame.quit()
