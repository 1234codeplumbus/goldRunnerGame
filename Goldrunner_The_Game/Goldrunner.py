#--------------
#v.1.2
#--------------
import pygame, sys
import random
import time
import webbrowser
from pygame.locals import *
pygame.init()
#variables --------------------------------------------------------
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 470
WINDOW_HEIGHT = 700
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#start game with 
score=0
scoreM=0
scoreH=0

count_shoot=0
count_main=0
reloadTime=20
ammoBAR=0
MAXammo=50
ammo=MAXammo

MAXMine_ammo=3
Mine_ammo=MAXMine_ammo
MAXhealth=100
EnemiesNUM=0
spawnRate=100
count_enemy=spawnRate
count_msg=0
length_msg=0


count_R=0
MENU = True# 
PLAY = False#
END_SCREEN =False#
PAUSE = False#
SETTINGS=False
HOW_TO_PLAY =False
gameMode=1
enemy_made=0
canUseMine=False
#------------------------------
mute=False
volume=0.2

Player={
"X": (470 - 50) / 2, 
"Y": WINDOW_HEIGHT-150,
"Width": 60,
"Height": 60,
"health":MAXhealth,
"speed":4,
"weapon":1,
"gunSpeed":1
}

pistol={
"speed":6,
"damage":2
}
ak={
    "speed":10,
    "damage":1
}

allMine={
    "damage":0.4
}

#load image 
enemy1=pygame.image.load('img\enemy1.png')
enemy2=pygame.image.load('img\enemy2.png')
enemy3=pygame.image.load('img\enemy3.png')
#scale image 
enemy1_scale=pygame.transform.scale(enemy1,(60,60))
enemy2_scale=pygame.transform.scale(enemy2,(60,60))
enemy3_scale=pygame.transform.scale(enemy3,(60,60))

Enemies={
    "speed":7,
    "health":[1,2,3],
    "skin":{0:enemy1_scale,
            1:enemy2_scale,
            2:enemy3_scale}
}

# /image
BACKGROUND=pygame.image.load('img\menu.png')
gameBG=pygame.image.load('img\gameBG.png')
gameBG1=pygame.image.load('img\gameBG1.png')
gameBG2=pygame.image.load('img\gameBG2.png')
gameBG3=pygame.image.load('img\gameBG3.png')
howBG=pygame.image.load('img\how.png')
dieBG= pygame.image.load('img\dieBG.png')
settingsBG= pygame.image.load('img\settingBG.png')

ammologo= pygame.image.load('img/ammologo.png')
HPlogo= pygame.image.load('img\HPlogo.png')
mc= pygame.image.load('img\mc.png')
mcW= pygame.image.load('img\mcW.png')

#the game icon
Icon = pygame.image.load('img\icon.png')

BACKGROUND_scale=pygame.transform.scale(BACKGROUND,(WINDOW_WIDTH,WINDOW_HEIGHT))
gameBG_scale=pygame.transform.scale(gameBG,(WINDOW_WIDTH,WINDOW_HEIGHT))
gameBG1_scale=pygame.transform.scale(gameBG1,(WINDOW_WIDTH,WINDOW_HEIGHT))
gameBG2_scale=pygame.transform.scale(gameBG2,(WINDOW_WIDTH,WINDOW_HEIGHT))
gameBG3_scale=pygame.transform.scale(gameBG3,(WINDOW_WIDTH,WINDOW_HEIGHT))
howBG_scale=pygame.transform.scale(howBG,(WINDOW_WIDTH,WINDOW_HEIGHT))
dieBG_scale=pygame.transform.scale(dieBG,(WINDOW_WIDTH,WINDOW_HEIGHT))
settingsBG_scale=pygame.transform.scale(settingsBG,(WINDOW_WIDTH,WINDOW_HEIGHT))

backon=0
bg=[gameBG_scale,gameBG1_scale,gameBG2_scale,gameBG3_scale]
#logo image
HPlogo_scale=pygame.transform.scale(HPlogo,(20,20))
ammologo_scale=pygame.transform.scale(ammologo,(20,20))
#2 images for player(walk and stand)
mc_scale=pygame.transform.scale(mc,(Player["Width"],Player["Height"]))
mcW_scale = pygame.transform.scale(mcW,(Player["Width"],Player["Height"]))

Rimg=pygame.transform.flip(mcW_scale,True,False)#make a fliped version of the walk image to swap to 
MC=[mcW_scale,Rimg,mc_scale]

step=0  #keep track of
walk=0  #goes up whn the player walkes
#Colours
BLACK = (0, 0, 0)
DARK_BLUE = (37, 57, 112)
WHITE =(255,255,255)
BLUE = (105, 145, 255)
GREY=(217,217,217,255)
GREEN=(106,168,79,255)
#load sound
click=pygame.mixer.Sound('sound\click.mp3')
click.set_volume(volume)
die=pygame.mixer.Sound('sound\die.wav')
die.set_volume(volume)
select=pygame.mixer.Sound('sound\select.wav')
select.set_volume(volume)
# main music
bgmusic=pygame.mixer.music.load('sound\BGmusic.mp3')


#read file 
def readfile():
    datafile = open("highScores.txt", 'r') # r means read
    line = datafile.readline()
    readScore=line.strip()
    scores = readScore.split(',')#returns the contese of the file into a array called "scoreArray" 
    datafile.close()
    return scores
# Save data to a file Standard Algorithm

#store the contese of the file into a array called "scoreArray"
scoreArray=readfile()
def writeTofile(score) : 
    datafile=open("highScores.txt", 'w') # w means append write over
    #write over a specific score depending on the game mode 
    if gameMode==0: 
        scoreArray[0]= score
    if gameMode==1:
        scoreArray[1]=score
    if gameMode==2:
        scoreArray[2]=score
    datafile.write(f"{scoreArray[0]},{scoreArray[1]},{scoreArray[2]}")#add it into the file 
    datafile.close()
#------------

Clicked=False# this makes sure that when you click it counts as one click  
#function that adds buttons that can be clicked to change a veriable 
def settings_buttons(posX,posY,var,min,max,change_amount):
    global Clicked
    global gameMode
    #settings options
    for event in pygame.event.get() :   
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
    fontObj = pygame.font.Font(None, 75)
    mouse = pygame.mouse.get_pos()
    Difficulty_point_r = pygame.Rect((WINDOW_WIDTH/2)+posX-25+60,WINDOW_HEIGHT/2-posY-5, 60,50)
    Difficulty_point_l = pygame.Rect((WINDOW_WIDTH/2)+posX-25,WINDOW_HEIGHT/2-posY-5, 60,50)

    shadow=pygame.Rect((WINDOW_WIDTH/2)+posX-25,WINDOW_HEIGHT/2-posY, 120,53)

    Difficulty_TXT_r = fontObj.render('>', True, BLACK, None)
    Difficulty_TXT_r_pos = Difficulty_TXT_r.get_rect(center=((WINDOW_WIDTH/2)+posX+70,WINDOW_HEIGHT/2-posY+15))

    Difficulty_TXT_l = fontObj.render('<', True, BLACK, None)
    Difficulty_TXT_l_pos = Difficulty_TXT_l.get_rect(center=((WINDOW_WIDTH/2)+posX,WINDOW_HEIGHT/2-posY+15))
    
    if Difficulty_point_r.collidepoint(mouse):
        #right btn
        Difficulty_point_r = pygame.Rect((WINDOW_WIDTH/2)+posX-25+60,WINDOW_HEIGHT/2-posY, 60,50)
        Difficulty_TXT_r_pos = Difficulty_TXT_r.get_rect(center=((WINDOW_WIDTH/2)+posX+70,WINDOW_HEIGHT/2-posY+23))
        
        if pygame.mouse.get_pressed()[0] == 1 and Clicked==False:
            var+=change_amount
            if mute==False:
                select.play()
            Clicked = True

    if Difficulty_point_l.collidepoint(mouse):
        #left btn
        Difficulty_TXT_l_pos = Difficulty_TXT_l.get_rect(center=((WINDOW_WIDTH/2)+posX,WINDOW_HEIGHT/2-posY+23))
        Difficulty_point_l = pygame.Rect((WINDOW_WIDTH/2)+posX-25,WINDOW_HEIGHT/2-posY, 60,50)

        if pygame.mouse.get_pressed()[0] == 1 and Clicked==False:
            var-=change_amount
            if mute==False:
                select.play()
            Clicked = True

    if pygame.mouse.get_pressed()[0] == 0:
        Clicked = False
    
    #setting a range 
    if(var>max):
        var=max
    #
    if(var<min):
        var=min
    #render buttons on screen 
    pygame.draw.rect(WINDOW, GREY, shadow)
    pygame.draw.rect(WINDOW, WHITE, Difficulty_point_r)
    pygame.draw.rect(WINDOW, WHITE, Difficulty_point_l)
    WINDOW.blit(Difficulty_TXT_l,Difficulty_TXT_l_pos)
    WINDOW.blit(Difficulty_TXT_r,Difficulty_TXT_r_pos)
    return var
#-------------------------------------------------------------------------

#Main code--------------------------------------------------------

all_sprites_list = pygame.sprite.Group()#add all sprites into a list to display in the same time
bullet_list = pygame.sprite.Group()
Badguy_list = pygame.sprite.Group()
mine_list = pygame.sprite.Group()
ak_list=pygame.sprite.Group()
blood_list=pygame.sprite.Group()

bul= pygame.transform.scale(pygame.image.load('img/shoot.png'),(7,15))#bullet image

class P_Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([5, 15])
        self.image.fill([245, 241, 144])
        self.image = bul#bullet image
        self.rect = self.image.get_rect()
    def update(self):
        #Move the bullet.
        self.rect.y -= pistol["speed"]
        
            
class ak_Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bul#bullet image
        self.rect = self.image.get_rect()
    def update(self):
        #Move the bullet.
        self.rect.y -= ak["speed"]
        
            
class mines(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        mineImg= pygame.transform.scale(pygame.image.load('img/mine.png'),(30,15))

        self.image = mineImg
        self.timer=0
        self.rect = self.image.get_rect()
    def update(self):
        if MENU ==True:
            self.kill()
        #removes self after some time
        self.timer+=1
        if self.timer>1000:
            self.kill()



class Enemy(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        #make a random enemys
        rand=random.randint(0,2)
        self.HP=Enemies["health"][rand]
        self.hit = pygame.Surface([50, 50])
        self.Limg = Enemies["skin"][rand]

        self.Rimg = pygame.transform.flip(Enemies["skin"][rand],True,False)
        self.flip=0
        self.image=self.Limg
        self.rect = self.image.get_rect()
        self.speed=Enemies["speed"]

    def update(self):
        global score
        global hit
        #colide player
        playerHitBox=pygame.Rect(Player["X"] ,Player["Y"],Player["Width"],Player["Height"])#make a hitbox for player to detect collision  

        if (self.rect.colliderect(playerHitBox) or self.rect.y>WINDOW_HEIGHT-120):
            damage(self.HP+6)  # the more hp the more damage
            self.kill()

        #move forward in a blocky motion
        self.speed+=1
        
        if self.speed ==1:
            self.rect.y += 13#  adds to y evry time 
            self.flip+=1        #flips to make the enemy look like its walking

        if self.speed>=Enemies["speed"]:# reset to loop the code above 
            self.speed=0
        #image alternates 
        if self.flip%2==0:
            self.image=self.Rimg
        else:
            self.image=self.Limg
        #getting damged  

        for bullet_p in bullet_list:
            if self.rect.colliderect(bullet_p.rect):
                #self.image = atkImg
                #remove bullet
                bullet_list.remove(bullet_p)
                all_sprites_list.remove(bullet_p)
                #damage enemy    
                self.HP-=pistol["damage"]
                #bleed
                blood= bleed()
                all_sprites_list.add(blood)
                blood_list.add(blood)
                blood.rect.x=self.rect.x
                blood.rect.y=self.rect.y
                #----

        for bullet_ak in ak_list:
            if self.rect.colliderect(bullet_ak.rect):
                #remove bullet
                ak_list.remove(bullet_ak)
                all_sprites_list.remove(bullet_ak)
  
                #damage enemy 
                self.HP-=ak["damage"]
                #bleed
                blood= bleed()
                all_sprites_list.add(blood)
                blood_list.add(blood)
                blood.rect.x=self.rect.x
                blood.rect.y=self.rect.y

        for mine in mine_list:
            if self.rect.colliderect(mine.rect):
                
                #damage enemy 
                self.HP-=allMine["damage"]
                #bleed
                blood= bleed()
                all_sprites_list.add(blood)
                blood_list.add(blood)
                blood.rect.x=self.rect.x
                blood.rect.y=self.rect.y

        #kill enemy
        if self.HP<=0:
            score += 1
            #bleed
            blood= bleed()
            all_sprites_list.add(blood)
            blood_list.add(blood)
            blood.rect.x=self.rect.x
            blood.rect.y=self.rect.y
            self.kill()

class bleed(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        spin=[90,180,130,360]
        rand=random.randint(0,3)
                                #rotate                 #scale           #load                            | random rotation|
        blood= pygame.transform.rotate(pygame.transform.scale(pygame.image.load('img/blood.png'),(50,50)),spin[rand] )# spins the blood image randomly to make it look diferent each time 
        self.image = blood
        self.image.set_alpha(28)

        self.timer=0
        self.rect = self.image.get_rect()
    
    def update(self):
        if MENU ==True:
            self.kill()
        self.timer+=1
        #remove over time
        if self.timer>1000:
            self.kill()

        
#-------------------------------------------------------------------------
pygame.display.set_caption('GOLDRUNNER')
pygame.display.set_icon(Icon)
def BackTOMenu():    
    global MENU
    global PLAY
    global END_SCREEN
    global PAUSE
    global HOW_TO_PLAY
    global SETTINGS
    global score
    global count_shoot
    global reloadTime
    global ammo
    global MAXammo
    global ammoBAR
    global MAXhealth
    global EnemiesNUM
    global spawnRate
    global count_enemy
    global count_main
    global Player
    global wave
    global canUseMine
    global MAXMine_ammo
    global Mine_ammo
    #reset the game 
    wave=1
    score=0
    count_shoot=0
    count_main=0
    ammoBAR=0
    MAXammo=50
    ammo=MAXammo
    MAXMine_ammo=3
    Mine_ammo=MAXMine_ammo
    spawnRate=100
    count_enemy=spawnRate
    Player["health"]=MAXhealth
    Player["weapon"]=0
    canUseMine=False
    MENU = True# display the menu
    PLAY = False# 
    SETTINGS =False
    END_SCREEN =False#
    PAUSE = False#
    HOW_TO_PLAY =False#
    main()

fontObj = pygame.font.Font(None, 75)
Text_msg = fontObj.render("", True, BLACK, None)
Text_mid = Text_msg.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
#shows a text that is given 
def display(txt,time,y,colour):
    global count_msg
    global length_msg
    global Text_msg
    global Text_mid
    count_msg=0
    length_msg=time
    fontObj = pygame.font.Font(None, 75)
    Text_msg = fontObj.render(txt, True, colour, None)
    Text_mid = Text_msg.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT-y))
    WINDOW.blit(Text_msg,Text_mid)


Text_msg_2 = fontObj.render("", True, BLACK, None)
Text_mid_2 = Text_msg_2.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

show=False
def displayWave(txt,t,y,colour):
    global Text_msg_2
    global Text_mid_2
    global show

    Text_msg_2 = fontObj.render(f"{txt}", True,colour, None)
    Text_mid_2 = Text_msg_2.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT-y))
    
    show=True
   
    

gameModeToTxt=""
def settings():
    #display instruction

    global MENU
    global PLAY
    global END_SCREEN
    global PAUSE
    global HOW_TO_PLAY
    global SETTINGS
    global mute
    global volume
    global vol_a
    global gameMode
    global MAXhealth
    global gameModeToTxt
    MENU = True# display the menu
    PLAY = False# 
    END_SCREEN =False#
    PAUSE = False#
    HOW_TO_PLAY = False#display how to play
    SETTINGS=True
    
    #the loop 
    while SETTINGS:
        updatecursor("normal")
        fontObj = pygame.font.Font(None, 75)
        mouse = pygame.mouse.get_pos()


        for event in pygame.event.get() :           

            if event.type == QUIT :
                pygame.quit()
                sys.exit()
        
        #box
        X = pygame.Rect((WINDOW_WIDTH-400)/2,0, 400,70)

        if X.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0] == 1:
                if mute==False:
                    select.play()
                SETTINGS = False
        smlFont = pygame.font.Font(None, 45)
        gameMode=settings_buttons(100,80,gameMode,0,2,1)#game mode

        
        if gameMode==0:
            #make dispay the game mode with text 
            gameModeToTxt="EASY"
            #make the game more easy
            MAXhealth=150
            pistol["damage"]=3
            ak["damage"]=2 
            
            Enemies["health"]=[1,2,3]


        if gameMode==1:
            gameModeToTxt="MEDIUM"
            #
            MAXhealth=100
            pistol["damage"]=2
            ak["damage"]=1
            Enemies["health"]=[3,4,5]

        if gameMode==2:
            gameModeToTxt="HARD"
            #make the game more hard
            MAXhealth=50
            pistol["damage"]=1
            ak["damage"]=1
            Enemies["health"]=[3,6,7]


        gameMode_txt=smlFont.render(f'{gameModeToTxt}', True, WHITE, None)

        volume=settings_buttons(100,-20,volume*10,0,10,1)/10#volume
        volume_txt=smlFont.render(f'{int(volume*100)}%', True, WHITE, None)

        global backon
        txtBG=["Spring","Autumn","Road","Snowy"]
        backon=settings_buttons(100,-140,backon,0,3,1)#gameBG
        BG_txt=smlFont.render(f'{(txtBG[backon])}', True, WHITE, None)
        #-mute-volume---------------------------------------------------------------------
        ofsetX=10
        ofsetY=4230
        newy=46
        vol_mute_BTN = pygame.Rect(WINDOW_WIDTH-76+ofsetX,WINDOW_HEIGHT-ofsetY,20,20)
        volBTN = pygame.Rect(WINDOW_WIDTH-76+ofsetX,WINDOW_HEIGHT-ofsetY,0,0)

        if mute ==False:
            vol_mute_BTN = pygame.Rect(WINDOW_WIDTH-78+ofsetX,WINDOW_HEIGHT-newy,20,20)
            volBTN = pygame.Rect(WINDOW_WIDTH+ofsetX,WINDOW_HEIGHT,0,0)
            
            if vol_mute_BTN.collidepoint(mouse):
                if pygame.mouse.get_pressed()[0] == 1:
                        select.play()
                        mute=True    
                        vol_mute_BTN = pygame.Rect(WINDOW_WIDTH+ofsetX,WINDOW_HEIGHT,0,0)
                        volBTN = pygame.Rect(WINDOW_WIDTH-54+ofsetX,WINDOW_HEIGHT-ofsetY,20,20)
        if mute ==True:  
            vol_mute_BTN = pygame.Rect(WINDOW_WIDTH+ofsetX,WINDOW_HEIGHT,0,0)
            volBTN = pygame.Rect(WINDOW_WIDTH-54+ofsetX,WINDOW_HEIGHT-newy,20,20)

            if volBTN.collidepoint(mouse):
                if pygame.mouse.get_pressed()[0] == 1:
                    select.play()
                    mute=False
                    vol_mute_BTN = pygame.Rect( -76+ofsetX,WINDOW_HEIGHT-ofsetY,20,20)
                    volBTN = pygame.Rect(WINDOW_WIDTH+ofsetX,WINDOW_HEIGHT,0,0)
        
        pygame.draw.rect(WINDOW, BLACK, volBTN)
        pygame.draw.rect(WINDOW, BLACK, vol_mute_BTN)
        WINDOW.blit(gameMode_txt,(100,270+60))
        WINDOW.blit(volume_txt,(120,370+60))
        WINDOW.blit(BG_txt,(110,375+170))
            
        pygame.display.update()
        WINDOW.blit(settingsBG_scale,(0,0))
        fpsClock.tick(FPS)

def howToPlay():
    #display instruction
    global MENU
    global PLAY
    global END_SCREEN
    global PAUSE
    global HOW_TO_PLAY
    MENU = True# display the menu 
    PLAY = False# 
    END_SCREEN =False#
    PAUSE = False#
    HOW_TO_PLAY = True#display how to play
    SETTINGS=False
    #the loop 
    while HOW_TO_PLAY:
        updatecursor("normal")
        fontObj = pygame.font.Font(None, 75)    
        mouse = pygame.mouse.get_pos()
        WINDOW.blit(howBG_scale,(0,0))
        #box
        X = pygame.Rect((0),0, 300,70)
        info_x=WINDOW_WIDTH-70
        info_y=20
        info=pygame.transform.scale(pygame.image.load("img/info.png"),(50,50))

        if X.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0] == 1:
                if mute==False:
                    select.play()
                HOW_TO_PLAY = False
        infoBox=pygame.Rect(info_x,info_y,80,80)
        if infoBox.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0] == 1:
                if mute==False:
                    select.play()
                webbrowser.open(r"https://sites.google.com/education.nsw.gov.au/goldrunner/how-to-play")

        # need to run
        for event in pygame.event.get() :           
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
        WINDOW.blit(info,(info_x,info_y))
                
        pygame.display.update()

        WINDOW.blit(BACKGROUND_scale,(0,0))

        fpsClock.tick(FPS)


def exit():
    #exit the game
    pygame.quit()
    sys.exit()
#make the enemy 
def calculate_enemy(wave):
    enemyNum=int(wave*10*1.5)
    return enemyNum
#make the cursor into a dot, normal and a cross
def updatecursor(state):

    if state=="normal":    #noraml cursor
        pygame.mouse.set_visible(True)
    
    if state=="mine":   # cross cursor
        pygame.mouse.set_visible(False)
        m1,m2=pygame.mouse.get_pos()
        # Get inputs
        w1=5
        h1=20
        w2=20
        h2=5

        up=pygame.Rect(m1-w2/2,m2-h2/2,w2,h2)  
        pygame.draw.rect(WINDOW, BLACK, up) 
        left=pygame.Rect(m1-w1/2,m2-h1/2,w1,h1)  
        pygame.draw.rect(WINDOW, BLACK, left) 
        
    if state=="dot":    #dot cursor
        pygame.mouse.set_visible(False)
        m1,m2=pygame.mouse.get_pos()
        # Get inputs
        w=10
        h=10
        cursor=pygame.Rect(m1-w/2,m2-h/2,w,h)  
        pygame.draw.rect(WINDOW, BLACK, cursor)

def gradientRect( window, top_colour, bottom_colour, target_rect ):# code from: https://stackoverflow.com/questions/62336555/how-to-add-color-gradient-to-rectangle-in-pygame 
    #changed to make the gradient top to bottom
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # 2x2 bitmap
    pygame.draw.line( colour_rect, top_colour,  ( 0,1 ), ( 1,1 ) )            # top colour line
    pygame.draw.line( colour_rect, bottom_colour, ( 0,0 ), ( 1,0 ) )            # bottom colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch 

    colour_rect.set_alpha(30)# make transperent 
    window.blit( colour_rect, target_rect )    

def Play():
    global Player
    global Enemies
    global count_enemy
    global PAUSE
    global score
    global count_shoot
    global display_msg
    global display_msg_2
    global ammoBAR
    global ammo
    global count_main
    global count_msg
    global MAXammo
    global spawnRate
    global END_SCREEN
    global HOW_TO_PLAY
    global MENU
    global Text_msg
    global Text_msg_2
    global Text_mid_2
    global fontObj
    global enemy_made 
    global canUseMine
    global Mine_ammo
    global MC
    MENU = False#
    PLAY = True# 
    END_SCREEN =False#
    PAUSE = False#
    HOW_TO_PLAY =False
    wave=1
    enemy_made=0                    
    aBreak=False
    breakTime=500
    Player["health"]=MAXhealth
    Player["weapon" ]=1
    i=0
    num=0
    global canhit
    global hit
    global show
    global walk
    global step
    while PLAY:
        for event in pygame.event.get() :
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #-MAIN-GAME------------------------------------------------------------
        if PAUSE==False:

            if(walk>0):
                walk-=8# the walk value is always going down if it is over 0
                if walk<=0:
                    step=2
                    walk=0
            if(walk>1):
                #walk code (the walk variable is added to every time the player walks)
                if walk % 36==0:# trigers every at a set time when walking  
                    num+=1
                if num % 2==0: # swap foot (the step value represents the plays foot step)
                    step=1#right
                else:
                    step=0#left

            #music
            if mute:
                pygame.mixer.music.set_volume(0) 
            else:
                pygame.mixer.music.set_volume(volume)
            #enemy spawn
            if count_enemy<spawnRate:
                count_enemy+=1
            if aBreak==False:
            #brake after every wave

                if count_enemy>=spawnRate:#timer

                    if enemy_made<=calculate_enemy(wave):
                        createEnemy()
                        enemy_made+=1
                        if score==3 or score ==4:
                            display(f"Unlock: Landmine",80,250,DARK_BLUE)
                            canUseMine=True

                    if enemy_made>=calculate_enemy(wave):#if all the enemies are made 
                        wave+=1
                        enemy_made=0
                        breakTime=0
                        #reload all ammo
                        ammo=MAXammo
                        Mine_ammo=MAXMine_ammo

            if breakTime<700:#after every wave
                aBreak=True
                breakTime+=1
                #set text to wave
                displayWave(f"WAVE: {wave}",80,250,DARK_BLUE)
            else: 
                #set text nothing
                displayWave(f"",80,250,DARK_BLUE)
                aBreak=False

            #makes the reload bar stay after there is no ammo 
            if ammo>0:
                ammoBAR=count_shoot
            else:
                ammoBAR=reloadTime
            if Player["weapon"]==1:
                ammoBAR=count_shoot

            if count_msg<length_msg:
                count_msg+=1

            if count_msg>=length_msg:
                Text_msg = fontObj.render("", True, BLACK, None)
            #PLAYER control
            pressed = pygame.key.get_pressed()
            if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]) :
                playerInput("right")
            if (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) :
                playerInput("left")
            if (pressed[pygame.K_SPACE]):
                playerInput("shoot")
            if pygame.mouse.get_pressed()[0]==1 and Player["weapon"]==3:
                playerInput("shoot")
            if  (pressed[pygame.K_ESCAPE]):
                playerInput("pauseGame")
            if  (pressed[pygame.K_1]):
                playerInput("pistol")
            if  (pressed[pygame.K_2]):
                playerInput("ak")

            if  (pressed[pygame.K_3]):
                if canUseMine:
                    playerInput("mine")

            if count_shoot<reloadTime:
                count_shoot+=Player["gunSpeed"]
            if (pressed[pygame.K_r]) and ammo<=0 and Player["weapon"]==2:
                count_R+=1.5
                if count_R>=200:
                    #fill ammo
                    ammo=MAXammo#reload
            elif(pressed[pygame.K_r]) and Mine_ammo<=0 and Player["weapon"]==3:
                count_R+=0.6
                if count_R>=200:
                    #fill ammo
                    Mine_ammo=MAXMine_ammo#reload
            else:
                #count_R=(ammo/MAXammo*200)#ammo
                count_R=0
                        
            #Make the game harder 
            if count_main<1000:
                count_main+=1
                
            if count_main==1000:
                count_main=0  
                MAXammo+=3
                spawnRate-=7#more enemy at a time
                
                if spawnRate<=0:#if the spawn rate is somehow lower than 0 then make it =1(the max difficulty)
                    spawnRate=20 
                    #more enemy and ammo

            #reaload time
            #
            if Player["weapon"]==1:#pistol 
                Player["speed"]=5
                Player["gunSpeed"]=1

            if Player["weapon"]==2:#ak
                Player["speed"]=3
                Player["gunSpeed"]=2

            if Player["weapon"]==3:#ak
                Player["speed"]=6
            
            # Processing        
            character = pygame.Rect(Player["X"],Player["Y"],Player["Width"],Player["Height"])  

            #reload bar
            ammoRe = pygame.Rect(20,WINDOW_HEIGHT-30,(WINDOW_WIDTH-30)*(ammoBAR/reloadTime),10)  
            ammobar = pygame.Rect(20,WINDOW_HEIGHT-20,(WINDOW_WIDTH-30),10)
            #ammo bar
            if Player["weapon"]==1:
                ammobar = pygame.Rect(20,WINDOW_HEIGHT-20,(WINDOW_WIDTH-30),10)
            if Player["weapon"]==2:
                ammobar = pygame.Rect(20,WINDOW_HEIGHT-20,(WINDOW_WIDTH-30)*(ammo/MAXammo),10)
            if Player["weapon"]==3:
                ammobar = pygame.Rect(20,WINDOW_HEIGHT-20,(WINDOW_WIDTH-30)*(Mine_ammo/MAXMine_ammo),10)
                ammobarRE = pygame.Rect(20,WINDOW_HEIGHT-20,(WINDOW_WIDTH-30)*(count_R/200),10)
            else:
                ammobarRE = pygame.Rect(20,WINDOW_HEIGHT-20,(WINDOW_WIDTH-30)*(count_R/200),10)

            #health bar
            HPbar = pygame.Rect(20,WINDOW_HEIGHT-60,(WINDOW_WIDTH-30)*(Player["health"]/MAXhealth),10)  
            
            #score text
            score_setup = pygame.font.Font(None, 50)
            scoreTxt = score_setup.render(f"SCORE: {score}", True, BLACK, None)
            score_pos = scoreTxt.get_rect(center=(WINDOW_WIDTH/2,40))#WINDOW.blit(scoreTxt,score_pos)
            # Render elements of the game
            #WINDOW.blit(gameBG_scale,(0,0))
            WINDOW.blit(bg[backon],(0,0))
            #draw the ak
            akgun=pygame.Rect(Player["X"]+44 ,Player["Y"]-8, 6,40)

            if Player["weapon"]==2:
                pygame.draw.rect(WINDOW,BLACK,akgun)
            
            #red overly
            if hit:

                gradientRect(WINDOW, (255,0, 0),(0,0, 0), pygame.Rect(0,0, WINDOW_WIDTH,WINDOW_HEIGHT))

                canhit=False
                i+=1
                if i>=80:
                    canhit=True
                    i=0
                    hit=False      
            
            global MC
            WINDOW.blit(MC[step],(Player["X"],Player["Y"]))
            pygame.draw.rect(WINDOW, (253, 218, 13), HPbar)#draw hp
            pygame.draw.rect(WINDOW, (199,11,18), ammoRe)#draw ammo reload
            pygame.draw.rect(WINDOW, (139, 0, 0), ammobarRE)#draw ammo filling 
            pygame.draw.rect(WINDOW, (199,11,18), ammobar)#draw ammo
            

            WINDOW.blit(HPlogo_scale,(20,WINDOW_HEIGHT-60))
            WINDOW.blit(ammologo_scale,(20,WINDOW_HEIGHT-30))
            all_sprites_list.update()
            all_sprites_list.draw(WINDOW)
            WINDOW.blit(Text_msg,Text_mid)
            if show:
                WINDOW.blit(Text_msg_2,Text_mid_2)
                show=False
                
            WINDOW.blit(scoreTxt,score_pos)
            
            if Player["weapon"]==3:
                m1,m2=pygame.mouse.get_pos()
                if m2<450: 
                    updatecursor("mine")
                else:
                    updatecursor("dot")
            else:
                    updatecursor("dot")
            pygame.display.flip()
            pygame.display.update()
            fpsClock.tick(FPS) 
            for bullet_p in bullet_list:#for each bullet 
                # Remove the bullet if it flies up off the screen
                if bullet_p.rect.y < -10 :
                    bullet_list.remove(bullet_p)
                    all_sprites_list.remove(bullet_p)

            for bullet_ak in ak_list:#for each bullet 
                # Remove the bullet if it flies up off the screen
                if bullet_ak.rect.y < -10 :
                    bullet_list.remove(bullet_ak)
                    all_sprites_list.remove(bullet_ak)


            #------------------------------------------------------------
        while PAUSE:   
            updatecursor("normal")
            if mute:
                pygame.mixer.music.set_volume(0)  
            else:
                pygame.mixer.music.set_volume(volume/2.5)  
            #run all the time------------------------------
            for event in pygame.event.get() :
                if event.type == QUIT :                        
                    pygame.quit()
                    sys.exit()

            #-------------------------------------------
            fontObj = pygame.font.Font(None, 75)
            Resume_btn=pygame.Rect(0,WINDOW_HEIGHT/2-140, WINDOW_WIDTH,70)  
            menu_btn=pygame.Rect(0,WINDOW_HEIGHT/2-40+200-100, WINDOW_WIDTH,70)
            quit_btn=pygame.Rect(0,WINDOW_HEIGHT/2+60-100, WINDOW_WIDTH,70)
    
            reumeTxt = fontObj.render('Resume', True, BLACK, None)
            menuTxt = fontObj.render('Back to menu', True, BLACK, None)
            quitTxt = fontObj.render('Exit', True, BLACK, None)
            #play position
            reumeTxt_mid = reumeTxt.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100-10))
            menuTxt_mid = menuTxt.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-10+200-100))
            quitTxt_mid = quitTxt.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100-10-100))

            mouse1 = pygame.mouse.get_pos()
            
            #-------------------------------------------

            if Resume_btn.collidepoint(mouse1):
                Resume_btn=pygame.Rect(0,WINDOW_HEIGHT/2-140+10, WINDOW_WIDTH,70)  
                reumeTxt_mid = reumeTxt.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100))
                reumeTxt = fontObj.render('Resume', True, BLACK, None)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if mute==False:
                        select.play()
                    PAUSE = False              
            if menu_btn.collidepoint(mouse1):
                menu_btn=pygame.Rect(0,WINDOW_HEIGHT/2-40+10+200-100, WINDOW_WIDTH,70)
                menuTxt_mid = menuTxt.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-10+10+200-100))
                menuTxt = fontObj.render('Back to menu', True, BLACK, None)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if mute==False:
                        select.play()
                    PLAY = False# start the game
                    BackTOMenu()
                    
            if quit_btn.collidepoint(mouse1):
                quit_btn=pygame.Rect(0,WINDOW_HEIGHT/2+60+10-100, WINDOW_WIDTH,70)
                quitTxt_mid = quitTxt.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100-10+10-100))
                quitTxt = fontObj.render('Exit', True, BLACK, None)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if mute==False:
                        select.play()
                    exit()      

            # Render elements of the game
            WINDOW.blit(MC[step],(Player["X"],Player["Y"]))
            
            
            pygame.draw.rect(WINDOW, (253, 218, 13), HPbar)#draw hp
            pygame.draw.rect(WINDOW, (199,11,18), ammoRe)#draw ammo
            pygame.draw.rect(WINDOW, (199,11,18), ammobar)#draw ammo
            WINDOW.blit(HPlogo_scale,(20,WINDOW_HEIGHT-60))#draw HP logo
            WINDOW.blit(ammologo_scale,(20,WINDOW_HEIGHT-30))#draw ammo logo


            WINDOW.blit(scoreTxt,score_pos)
            pygame.display.flip()
            #the grey shadow [217,217,217,255]
            pygame.draw.rect(WINDOW,GREY,pygame.Rect(0,WINDOW_HEIGHT/2-140+20, WINDOW_WIDTH,70))
            pygame.draw.rect(WINDOW,GREY,pygame.Rect(0,WINDOW_HEIGHT/2-40+20+200-100, WINDOW_WIDTH,70))
            pygame.draw.rect(WINDOW,GREY,pygame.Rect(0,WINDOW_HEIGHT/2+60+20-100, WINDOW_WIDTH,70))
            
            #green
            pygame.draw.rect(WINDOW,GREY,pygame.Rect(0,WINDOW_HEIGHT/2-140, WINDOW_WIDTH,70))
            pygame.draw.rect(WINDOW,GREY,pygame.Rect(0,WINDOW_HEIGHT/2-40+200-100, WINDOW_WIDTH,70))
            pygame.draw.rect(WINDOW,GREY,pygame.Rect(0,WINDOW_HEIGHT/2+60-100, WINDOW_WIDTH,70))

            # Render elements of the pause menu
            pygame.draw.rect(WINDOW,WHITE,Resume_btn)
            pygame.draw.rect(WINDOW,WHITE,menu_btn)
            pygame.draw.rect(WINDOW,WHITE,quit_btn)

            WINDOW.blit(reumeTxt,reumeTxt_mid)
            WINDOW.blit(menuTxt,menuTxt_mid)
            WINDOW.blit(quitTxt,quitTxt_mid)
            pygame.display.flip()
            pygame.display.update()

            fpsClock.tick(FPS)




def playerInput(action):
    global Player
    global PAUSE
    #the "walk" veriable will be added on to when the player walkes 
    global walk
    #player movement
    if action=="left":
        #move left
        if Player["X"]>=10:#setting a range on where the player can move
            Player["X"]-=Player["speed"]
            walk+=9
    if action=="right":
        #move right
        if Player["X"]+Player["Width"]<=460:#setting a range on where the player can move
            Player["X"]+=Player["speed"]
            walk+=9
    #shoot    
    if action=="shoot":
        shoot()
    #pause the game 
    if action=="pauseGame":
        PAUSE =True
    #swap weapons 
    if action=="pistol":#change player weapon to pistol and dispay "[pistol]"
        display("[pistol]",50,200,BLACK)
        Player["weapon"]=1
    if action=="ak":#change player weapon to ak and dispay "[ak]"
        display("[ak]",50,200,BLACK)
        Player["weapon"]=2
    if action=="mine":#change player weapon to mine and dispay "[mine]"
        display("[mine]",50,200,BLACK)
        Player["weapon"]=3
        
        
def createEnemy():
    global count_enemy
    badguy = Enemy()
    location=random.randint(30, WINDOW_WIDTH-50-30)
    # Set the badguy to a random location
    badguy.rect.x = location
    badguy.rect.y = -50
    # Add the badguy to the lists
    all_sprites_list.add(badguy)
    Badguy_list.add(badguy)   
    #delay
    count_enemy=0


def shoot(): #called within playerInput
    global count_shoot
    global ammo
    global Mine_ammo
    global ammoBAR
    
    if Player["weapon"]==1:
        if count_shoot>=reloadTime :
        #pistol
            bullet_p = P_Bullet()
            # Set the bullet so it is where the player is
            bullet_p.rect.x = Player["X"]+30
            bullet_p.rect.y = Player["Y"]-25
            # Add the bullet to the lists
            all_sprites_list.add(bullet_p)
            bullet_list.add(bullet_p)   
            count_shoot=0

    if Player["weapon"]==2:
        if count_shoot>=reloadTime and ammo>0:
            #
            #ak
            bullet_ak = ak_Bullet()
            # Set the bullet so it is where the player is
            bullet_ak.rect.x = Player["X"]+43
            bullet_ak.rect.y = Player["Y"]-25
            # Add the bullet to the lists
            all_sprites_list.add(bullet_ak)
            ak_list.add(bullet_ak)   
            #delay
            count_shoot=0
            ammo-=1
        elif count_shoot>=reloadTime:
            #play sound reload 
            if mute==False:
                click.play()
            count_shoot=0
    Click=False
    if Player["weapon"]==3:
        if pygame.mouse.get_pressed()[0]==1 and Click==False:
            Click = True
            if count_shoot>=reloadTime and Mine_ammo>0:
            #pistol
                m1,m2=pygame.mouse.get_pos()
                if m2<450: 
                    mine = mines()
                    # Set the bullet so it is where the player is
                    mine.rect.x = m1
                    mine.rect.y = m2
                    # Add the bullet to the lists
                    all_sprites_list.add(mine)
                    mine_list.add(mine)   
                    Mine_ammo-=1
                    count_shoot=0
        if pygame.mouse.get_pressed()[0] == 0:
            Click = False

hit=False
canhit=True
def damage(damage):
    global hit
    global canhit
    if canhit==True:
        #damage the Player health 
        Player["health"] -= damage
        hit=True
        #update health bar
        if Player["health"] <= 0:
            Player["health"]=0
            if mute==False:
                die.play()#die sound
            deathMenu()

def deathMenu():
    global MENU
    global PLAY
    global END_SCREEN
    global PAUSE
    global HOW_TO_PLAY
    MENU = False#
    PLAY = False# 
    END_SCREEN =True#start the loop
    PAUSE = False#
    HOW_TO_PLAY =False
    Highscore=False
    score_setup2 = pygame.font.Font(None,60)
    scoreMsg = score_setup2.render("NEW HIGH SCORE!", True, WHITE, None)
    while END_SCREEN:
        updatecursor("normal")
        pygame.mixer.music.set_volume(0)
        fontObj = pygame.font.Font(None, 75)
        #run all the time------------------------------
        for event in pygame.event.get() :
            if event.type == QUIT :                        
                pygame.quit()
                sys.exit()
        #clear all the elements from the screen  
        for bullet in bullet_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
        for badguy in Badguy_list:
            Badguy_list.remove(badguy)
            all_sprites_list.remove(badguy)
        for mine in mine_list:
            mine.timer=10000
        for blood in blood_list:
            blood_list.remove(blood)
            all_sprites_list.remove(blood)
        #------------------------------------------- rendering
        score_setup = pygame.font.Font(None,80)
        scoreTxt = score_setup.render(f"FINAL SCORE", True, WHITE, None)
        score2nd = score_setup.render(f"{score}", True, WHITE, None)
        score_pos = scoreTxt.get_rect(center=(WINDOW_WIDTH/2,100))
        score2nd_pos = score2nd.get_rect(center=(WINDOW_WIDTH/2,160))
        menu_btn=pygame.Rect(0,600-20, WINDOW_WIDTH,70)
        quit_btn=pygame.Rect(0,WINDOW_HEIGHT/2+60-100, WINDOW_WIDTH,70)

        #buttons
        menuTxt = fontObj.render('Exit', True, BLACK, None)
        quitTxt = fontObj.render('Back to menu', True, BLACK, None)
        menuTxt_mid = menuTxt.get_rect(center=(WINDOW_WIDTH/2, 600+20))
        quitTxt_mid = quitTxt.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100-10-100))

        mouse1 = pygame.mouse.get_pos()
        
        #-------------------------------------------
             
        if menu_btn.collidepoint(mouse1):
            menu_btn=pygame.Rect(0,600-10, WINDOW_WIDTH,70)
            menuTxt_mid = menuTxt.get_rect(center=(WINDOW_WIDTH/2, 600+30))
            menuTxt = fontObj.render('Exit', True, BLACK, None)

            if pygame.mouse.get_pressed()[0] == 1:
                if mute==False:
                    select.play()
                exit()


        if quit_btn.collidepoint(mouse1):
            quit_btn=pygame.Rect(0,WINDOW_HEIGHT/2+60+10-100, WINDOW_WIDTH,70)
            quitTxt_mid = quitTxt.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100-100))
            quitTxt = fontObj.render('Back to menu', True, BLACK, None)

            if pygame.mouse.get_pressed()[0] == 1:
                if mute==False:
                    select.play()

                BackTOMenu()      
                

        if (score>int(scoreArray[gameMode])):# if you got the last high score
            #NEW HIGH SCORE
            Highscore=True
            writeTofile(f"{score}")


        if Highscore:
            scoreMsg = score_setup2.render("NEW HIGH SCORE!", True, WHITE, None)

        else:
            scoreMsg = score_setup2.render("", True, WHITE, None)
            if score==0:
                scoreMsg = score_setup2.render("Are you even trying???", True, WHITE, None)

        scoreMsg_pos = scoreMsg.get_rect(center=(WINDOW_WIDTH/2,250))

        # Render elements of the game     
        WINDOW.blit(dieBG_scale,(0,0))
        pygame.draw.rect(WINDOW,GREY,pygame.Rect(0,600, WINDOW_WIDTH,70))
        pygame.draw.rect(WINDOW,GREY,pygame.Rect(0,WINDOW_HEIGHT/2+60+20-100, WINDOW_WIDTH,70))        
        # Render elements of the pause menu
        pygame.draw.rect(WINDOW,WHITE,menu_btn)
        pygame.draw.rect(WINDOW,WHITE,quit_btn)
        WINDOW.blit(menuTxt,menuTxt_mid)
        WINDOW.blit(quitTxt,quitTxt_mid)
        WINDOW.blit(scoreTxt,score_pos)
        WINDOW.blit(score2nd,score2nd_pos)
        WINDOW.blit(scoreMsg,scoreMsg_pos)

        pygame.display.update()
        WINDOW.blit(bg[backon],(0,0))
#----------------------------------------


# The main function that controls the game
def main () :
    readfile()
    #variables that are accessed/changed 
    global PLAY
    global MENU
    global END_SCREEN
    global mute
    global SETTINGS

    run=True
    while run:
        updatecursor("normal")
    #----------------------------------------------------
        MENU =True
        while MENU ==True:
            pygame.mouse.set_visible(True)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0)
        
            #clear all the elements from the screen  
            for bullet in bullet_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
            for badguy in Badguy_list:
                Badguy_list.remove(badguy)
                all_sprites_list.remove(badguy)
            for mine in mine_list:
                mine.timer=10000
            for blood in blood_list:
                blood_list.remove(blood)
                all_sprites_list.remove(blood)
            #quit 
            for event in pygame.event.get() :
                if event.type == QUIT :
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            #render
            WINDOW.blit(BACKGROUND_scale,(0,0))
            fpsClock.tick(FPS)
            fontObj = pygame.font.Font(None, 75)
            Play_btn = pygame.Rect(0,WINDOW_HEIGHT-600, WINDOW_WIDTH,50)
            how_btn = pygame.Rect(0,WINDOW_HEIGHT-500, WINDOW_WIDTH,50)
            Resume_btn = pygame.Rect(0,WINDOW_HEIGHT-400, WINDOW_WIDTH,50)
            HighScore_box_txt = pygame.Rect((470 - 400)/2, 450, 400,70)
            mouse = pygame.mouse.get_pos()
            #------------------------------------------------------------


            #playText
            playText = fontObj.render('PLAY', True, BLACK, None)
            #play position
            playText_mid = playText.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-20-200))

            #howText
            howText = fontObj.render('HOW TO PLAY', True, BLACK, None)
            #howText position
            howText_mid = howText.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-20-100))

            #exitText
            exitText = fontObj.render('EXIT', True, BLACK, None)
            #play position
            exitText_mid = exitText.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-20))

            #high score
            smltxt = pygame.font.Font(None, 45)
            HighScoreE = smltxt.render(f'{readfile()[0]}', True, WHITE, None)# gets the 1st score from the aray
            HighScoreM = smltxt.render(f'{readfile()[1]}', True, WHITE, None)# gets the 2rd score from the aray
            HighScoreH = smltxt.render(f'{readfile()[2]}', True, WHITE, None)# gets the 3rd score from the aray
            #render
            HighScoreE_mid = HighScoreE.get_rect(center=(WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2+130))
            HighScoreM_mid = HighScoreM.get_rect(center=(WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2+210))
            HighScoreH_mid = HighScoreH.get_rect(center=(WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2+280))

            if Play_btn.collidepoint(mouse):
                playText_mid = playText.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-20-200+10))
                Play_btn = pygame.Rect(0,WINDOW_HEIGHT-600+10, WINDOW_WIDTH,50)
                playText = fontObj.render('PLAY', True, BLACK, None)
                pygame.draw.rect(WINDOW, WHITE, Play_btn)
                if pygame.mouse.get_pressed()[0] == 1 :
                    if mute==False:
                        select.play()
                    Play()

            if how_btn.collidepoint(mouse):
                howText_mid = howText.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-20-100+10))
                how_btn = pygame.Rect(0,WINDOW_HEIGHT-500+10, WINDOW_WIDTH,50)
                howText = fontObj.render('HOW TO PLAY', True, BLACK, None)
                pygame.draw.rect(WINDOW, WHITE, how_btn)
                if pygame.mouse.get_pressed()[0] == 1:
                    if mute==False:
                        select.play()
                    howToPlay()

            if Resume_btn.collidepoint(mouse):
                exitText_mid = exitText.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-20+10))
                Resume_btn = pygame.Rect(0,WINDOW_HEIGHT-400+10, WINDOW_WIDTH,50)
                exitText = fontObj.render('EXIT', True, BLACK, None)
                pygame.draw.rect(WINDOW, WHITE, Resume_btn)
                if pygame.mouse.get_pressed()[0] == 1:
                    if mute==False:
                        select.play()
                    exit()
            settings_BTN = pygame.Rect(WINDOW_WIDTH-70,WINDOW_HEIGHT-70,70,70)
            if settings_BTN.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
                if mute==False:
                    select.play()
                settings()



            # Render elements of the game
            pygame.draw.rect(WINDOW, WHITE, Play_btn)
            pygame.draw.rect(WINDOW, WHITE, how_btn)
            pygame.draw.rect(WINDOW, WHITE, Resume_btn)

            WINDOW.blit(playText,playText_mid)
            WINDOW.blit(howText,howText_mid)
            WINDOW.blit(exitText,exitText_mid)
            WINDOW.blit(HighScoreE,HighScoreE_mid)
            WINDOW.blit(HighScoreM,HighScoreM_mid)
            WINDOW.blit(HighScoreH,HighScoreH_mid)
        
        # The main game loop
    
          
            

main()
#_____________
#drivers
#_____________

'''  functions to calculate:

    settings_buttons(posX,posY,var,min,max,change_ammount):
    
    damage(damage):
    
    calculate_enemy(wave)

'''

#_____________________



