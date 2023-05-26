# Variables globals amb valors per configurar el joc

# Amplada i alçada de la pantalla
mides_pantalla = 960, 630

# Nombre màxim d'imatges per segon (fps)
fps = 60

# Color de fons de la pantalla
color_fons = 70, 70, 70

#Sprite sheet player
sprite_sheet_player = "imag/player.png"
mides_sprite_sheet_player = 2, 4
posicio_player = 0, 0

sprite_sheet_enemy = "imag/enemy.png"
mides_sprite_sheet_enemy = 3, 4

sprite_sheet_blood = "imag/blood.png"
mides_sprite_sheet_blood = 3, 3

sprite_mouse  = 'imag/cursor.png'
sprite_map    = 'imag/mapa.png'
sprite_bullet = 'imag/bullet.png'
sprite_ref    = 'imag/referencia.png'
sprite_tramp  = 'imag/trampilla.png'

bullet_icon = 'imag/bullet_icon.png'
vida_icon = 'imag/vida_icon.png'

inter_vida = 'imag/botiquin.png'
inter_mun  = 'imag/municio.png'
inter_clau = ['imag/clau1.png',
              'imag/clau2.png',
              'imag/clau3.png']

music    = 'music/music.mp3'
snd_shot = 'music/pistol_shot.wav'
snd_no_shot = 'music/empty_shot.wav'
snd_open = 'music/key.wav'
snd_lock = 'music/stomp.wav'
snd_pick = 'music/pick_up.wav'
snd_hit  = 'music/hit.wav'
snd_dead = 'music/dead.wav'

'''

0 - Res
1 - Paret
3 - Trampilla
a,b,c... Path
!"·$%... Portes

'''

mp=['111111111111111111111111111111111111111111',
    '103000100030000000000000000000000010000001',
    '100000"000g000000i0000000k00000000%0000001',
    '100f00"000000000000000000000000n00%0q00001',
    '100000"000000000000000000000000000%0000001',
    '100000111···11111$$$1100010001000010000001',
    '100000100000001000000100010001000010000031',
    '1000001000H0001000j0010l010m01000010000001',
    '100e0010000000100000010001000100o0100r0001',
    '100000100000001000000100313001000310000001',
    '1000001000h0001000300100010001000011111111',
    '100000100000001111111111111111&&&&10000001',
    '10d0001000300010000000000100300000100x0031',
    '1000001111111113000000003100000p0010000001',
    '1000001000000010000z0000000000000010000001',
    '10000010000000100000000s00t00000001///1111',
    '100000!00000001000000000000000000000000001',
    '100c00!0b000a310y000000001000000000000000)',
    '100000!00000001000000000010000v00000w0000)',
    '103000100000001030000003010030000000030001',
    '111111111111111111((((11111111111111111111']

nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
         'o', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

edges = [('a','b'),('b','c'),('c','d'),('d','e'),('e','f'),('f','g'),('g','H'),
         ('g','i'),('i','j'),('i','k'),('k','l'),('k','m'),('k','n'),('n','q'),
         ('q','r'),('n','o'),('o','p'),('p','t'),('p','v'),('v','t'),('v','w'),
         ('w','x'),('t','s'),('t','z'),('z','s'),('z','y'),('y','s'),('H','h')]

inter     = [0,0,0,0,0] #+1 vida / +50 bales / clau 1 / clau 2 / clau 3 
bolPorta  = [0,0,0,0,0,0,0,0,0]

preuPorta = ['i3',50,80,80,250,150,'i2','i4',700]
strPorta  = '!"·$%&/()'

b = 48
pSpawn0 =       [(73,81),(73,490),(95,893)]
pSpawn  = {'!': [(577, 881)],
           '"': [(403,126),(1554,411),(1107,434),(1290,417),(1082,118)],
           '·': [(411,496)],
           '$': [(817,382)],
           '%': [(1842,264)],
           '&': [(1867,840),(1311,881),(1295,605),(1107,878),(764,877),(758,604)],
           '/': [(1902,565)]}


