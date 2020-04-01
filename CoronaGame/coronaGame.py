import pygame
import os
import sys
import random

# set main game parameters
pygame.init()
pygame.display.set_caption("FG")
clock = pygame.time.Clock()
blocksize = 50
gameheight = blocksize*12
gamewidth = blocksize*10
gameTime = 60 # length of game in seconds
win = pygame.display.set_mode((gamewidth,gameheight))
# 
# define colors
white=(255,255,255)
black = (0,0,0)
green=(0,255,0)
blue=(0,0,255)
red=(255,0,0)
virusSpeedarr = [blocksize//20,blocksize//10,blocksize//5]
bedbarSpeedarr = [0.1,0.2,0.2]
curr_powerup = -1
# Loading images
base_dir = os.path.abspath(os.path.dirname(__file__))
file_nameBG = os.path.join(base_dir,"env","hospitalBGExtended.png")
background = pygame.image.load(file_nameBG)
menuBG = pygame.image.load(os.path.join(base_dir,"env","menuBG2.png"))
congotext = pygame.image.load(os.path.join(base_dir,"env","congoText.png"))
okText = pygame.image.load(os.path.join(base_dir,"env","okText.png"))
badText = pygame.image.load(os.path.join(base_dir,"env","alldead.png"))
deadtext = pygame.image.load(os.path.join(base_dir,"env","DeadText.png"))
bedIMG = [pygame.image.load(os.path.join(base_dir,"sprites","bed","bed1.png")),
          pygame.image.load(os.path.join(base_dir,"sprites","bed","bed2.png")),
          pygame.image.load(os.path.join(base_dir,"sprites","bed","bed3.png")),
          pygame.image.load(os.path.join(base_dir,"sprites","bed","bed4.png")),
          pygame.image.load(os.path.join(base_dir,"sprites","bed","bed5.png")),
          pygame.image.load(os.path.join(base_dir,"sprites","bed","bed6.png")),
          pygame.image.load(os.path.join(base_dir,"sprites","bed","bed7.png")),
          pygame.image.load(os.path.join(base_dir,"sprites","bed","bed8.png")),]
usedbedIMG = []
coffinIMG = pygame.image.load(os.path.join(base_dir,"sprites","bed","coffin.png"))
virusIMG = [pygame.image.load(os.path.join(base_dir,"sprites","virus","virus50.png")),
            pygame.image.load(os.path.join(base_dir,"sprites","virus","virus50_2.png")),
            pygame.image.load(os.path.join(base_dir,"sprites","virus","virus50_3.png")),
            pygame.image.load(os.path.join(base_dir,"sprites","virus","virus50_4.png"))]
cupboardIMG_arr = [pygame.image.load(os.path.join(base_dir,"sprites","cupboard","cupboard_white.png")),
                   pygame.image.load(os.path.join(base_dir,"sprites","cupboard","cupboard_green.png")),
                   pygame.image.load(os.path.join(base_dir,"sprites","cupboard","cupboard_red.png")),
                   pygame.image.load(os.path.join(base_dir,"sprites","cupboard","cupboard_blue.png"))]
handwashIMGarr = [pygame.image.load(os.path.join(base_dir,"sprites","powerups","handwash","hw1.png")),
                  pygame.image.load(os.path.join(base_dir,"sprites","powerups","handwash","hw2.png")),
                  pygame.image.load(os.path.join(base_dir,"sprites","powerups","handwash","hw3.png")),
                  pygame.image.load(os.path.join(base_dir,"sprites","powerups","handwash","hw4.png")),]
maskIMGarr = [pygame.image.load(os.path.join(base_dir,"sprites","powerups","mask","msk1.png")),
              pygame.image.load(os.path.join(base_dir,"sprites","powerups","mask","msk2.png")),
              pygame.image.load(os.path.join(base_dir,"sprites","powerups","mask","msk3.png")),
              pygame.image.load(os.path.join(base_dir,"sprites","powerups","mask","msk4.png")),]
powerupIMGarr = [handwashIMGarr,maskIMGarr]
powerupThumbnailIMG = [pygame.image.load(os.path.join(base_dir,"sprites","powerups","handwash","hwt.png")),
                       pygame.image.load(os.path.join(base_dir,"sprites","powerups","mask","mskt.png"))]
# 
folderN = os.path.join(base_dir,"sprites","nurse")
nurse_left_img = [pygame.image.load(os.path.join(folderN,"NJL1.gif")),pygame.image.load(os.path.join(folderN,"NJL2.gif")),
                pygame.image.load(os.path.join(folderN,"NJL3.png")),pygame.image.load(os.path.join(folderN,"NJL4.gif"))]
nurse_right_img = [pygame.image.load(os.path.join(folderN,"NJR1.gif")),pygame.image.load(os.path.join(folderN,"NJR2.gif")),
                pygame.image.load(os.path.join(folderN,"NJR3.gif")),pygame.image.load(os.path.join(folderN,"NJR4.gif"))]
nurse_up_img = [pygame.image.load(os.path.join(folderN,"NJU1.gif")),pygame.image.load(os.path.join(folderN,"NJU2.gif")),
                pygame.image.load(os.path.join(folderN,"NJU3.gif")),pygame.image.load(os.path.join(folderN,"NJU4.gif"))]
nurse_down_img = [pygame.image.load(os.path.join(folderN,"NJD1.png")),pygame.image.load(os.path.join(folderN,"NJD2.gif")),
                pygame.image.load(os.path.join(folderN,"NJD3.gif")),pygame.image.load(os.path.join(folderN,"NJD4.gif"))]
nurse_img_arr = [nurse_up_img,nurse_down_img,nurse_left_img,nurse_right_img]
# 

# Player class. All behavior of player is inside this class
class player(pygame.sprite.Sprite):
    
    spriteHeight = blocksize
    spriteWidth = blocksize
    
    # path to sprite images
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(base_dir,"sprites","nurse")
    # init function. Runs when this player class is created
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([self.spriteWidth, self.spriteHeight])
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        # self.image = pygame.image.load(os.path.join(self.file_name,"nurses_d.png"))
        self.currImgArr = nurse_img_arr[1]
        self.image = self.currImgArr[0]
        self.rect.y = y
        self.rect.x = x
        self.rect.width = self.spriteWidth-10
        self.rect.height = self.spriteHeight-25
        # player speed and direction
        self.speed = blocksize//10
        self.dir = 0
        self.stepcount = 0
        # movement constraints
        self.freeleft = True
        self.freeright = True
        self.freeup = True
        self.freedown = True
        # is dead yet?
        self.dead = False
        #color picked up. Default is black
        self.selectedColor = black

    # when x is pressed, check if player is close to bed, if yes, feed the patient with holding color
    def feed(self,listOfBeds):
        print (self.rect.x,self.rect.y)
        for bed in listOfBeds:
            print(bed.rect.x,bed.rect.y,bed.rect.x+bed.rect.width,bed.rect.y+bed.rect.height)
            if self.rect.y>=bed.rect.y and self.rect.y<=bed.rect.y+50:
                if self.rect.x == bed.rect.x+bed.rect.width and self.dir == 3:#nurse close to bed
                    if self.selectedColor == bed.needcolor and bed.patientAlive:
                        self.selectedColor = black
                        bed.needcolor = black
                        bed.isinNeed = False
                if self.rect.x+self.rect.width == bed.rect.x and self.dir == 4:#nurse close to bed
                    if self.selectedColor == bed.needcolor and bed.patientAlive:
                        self.selectedColor = black
                        bed.needcolor = black
                        bed.isinNeed = False
    # when x is pressed, check if nurse is close to cupboard. If yes, teke the medicine
    def getfeed(self,listOfCupboards):
        print (self.rect.x,self.rect.y)
        for cupboard in listOfCupboards:
            print(cupboard.rect.x,cupboard.rect.y,cupboard.rect.x+cupboard.rect.width,cupboard.rect.y+cupboard.rect.height)
            if self.rect.y+self.rect.height == cupboard.rect.y:
                if self.rect.x>=cupboard.rect.x-10 and self.rect.x<=cupboard.rect.x+10 and self.dir == 2:
                    self.selectedColor = cupboard.color
                    print(self.selectedColor)
            
    # function for moving the nurse. its a bit comple. It includes collision detection
    def move(self,keys,beds):
        global curr_powerup
        freeleft = True
        freeright = True
        freeup = True
        freedown = True
        if self.rect.y <= 60:
            freeup = False
        if self.rect.y + self.rect.width >= gameheight-35:
            freedown = False
        if self.rect.x <= 0:
            freeleft = False
        if self.rect.x + self.rect.width >= gamewidth:
            freeright = False
        
        # Move according to keys. If collision detected, we will reverse the move in the next block 
        oldDir = self.dir
        if(keys[pygame.K_UP] and freeup):
            self.dir = 1
            if self.dir == oldDir:
                self.rect.y -=self.speed
            else:
                self.currImgArr = nurse_img_arr[self.dir-1]
                self.stepcount=0
            self.image = self.currImgArr[self.stepcount//4]
        elif(keys[pygame.K_DOWN] and freedown):
            self.dir = 2
            if self.dir == oldDir:
                self.rect.y +=self.speed
            else:
                self.currImgArr = nurse_img_arr[self.dir-1]
                self.stepcount=0
            self.image = self.currImgArr[self.stepcount//4]
        elif(keys[pygame.K_LEFT] and freeleft):
            self.dir = 3
            if self.dir == oldDir:
                self.rect.x -=self.speed
            else:
                self.currImgArr = nurse_img_arr[self.dir-1]
                self.stepcount=0
            self.image = self.currImgArr[self.stepcount//4]
        elif(keys[pygame.K_RIGHT] and freeright):
            self.dir = 4
            if self.dir == oldDir:
                self.rect.x +=self.speed
            else:
                self.currImgArr = nurse_img_arr[self.dir-1]
                self.stepcount=0
            self.image = self.currImgArr[self.stepcount//4]
        if(keys[pygame.K_x]):
            self.feed(beds_sprites)
            self.getfeed(cupboard_sprites)

        self.stepcount = (self.stepcount+1)%16
        # reversing move if collision detected
        collisions = pygame.sprite.spritecollide(self, allSprites, False)
        if(len(collisions) != 1):
            print(curr_powerup,collisions[1])
            if not(curr_powerup==1 and virus_sprites.has(collisions[1])):
                if self.dir == 1:
                    self.rect.y+=self.speed
                if self.dir == 2:
                    self.rect.y-=self.speed
                if self.dir == 3:
                    self.rect.x+=self.speed
                if self.dir == 4:
                    self.rect.x-=self.speed
                if powerup_sprites.has(collisions[1]):
                    curr_powerup = collisions[1].typ
                    print(curr_powerup)
                    collisions[1].kill()
                if virus_sprites.has(collisions[1]):
                    collisions[1].kill()
                    self.dead = True
                
    def update(self):
        if not(self.selectedColor==black):
            pygame.draw.rect(win,self.selectedColor,(self.rect.x,self.rect.y-5,5,5))
        global curr_powerup
        if curr_powerup != -1:
            win.blit(powerupThumbnailIMG[curr_powerup],(self.rect.right,self.rect.top-10))

# 
# Class for beds. All behavior of beds are defined within
class Bed(pygame.sprite.Sprite):

    height = 2*blocksize
    width = 1*blocksize

    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([self.width, self.height])
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.rect.width = self.width-10
        self.rect.height = self.height-25
        global usedbedIMG
        while True:
            self.image = random.choice(bedIMG)
            if usedbedIMG.count(self.image)<=0:
                break

        usedbedIMG.append(self.image)
        # default required medicine color of patient
        self.needcolor = black
        self.needPercentage = float(0)
        self.isinNeed = False
        self.patientAlive = True
    
    def update(self):
        global gameMode
        if not(self.isinNeed):
            self.isinNeed = random.randrange(1000)<10
            if self.isinNeed:
                self.needPercentage = 0
                self.needcolor = random.choice([blue,green,red])
        if self.isinNeed and self.needPercentage<100:
            # Speed with which the bar fills
            self.needPercentage += bedbarSpeedarr[gameMode]
            pygame.draw.rect(win,white,(self.rect.x-5,self.rect.y-15,5,15))
            pygame.draw.rect(win,self.needcolor,(self.rect.x-5,self.rect.y-15,5,(15*self.needPercentage)//100))
            pygame.draw.rect(win,black,(self.rect.x-5,self.rect.y-15,5,15),1)
        if self.needPercentage >= 100:
            self.image = coffinIMG
            self.patientAlive = False
            beds_sprites.remove(self)
# 
# class for cupboards. All behavior of cupboards are defined within
class cupboard(pygame.sprite.Sprite):
    height = blocksize
    width = blocksize
    def __init__(self,color, x, y):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([self.width, self.height])
        self.color = color
        self.image.fill(color)


        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        if self.color == white:
            self.image = cupboardIMG_arr[0]
        elif self.color == green:
            self.image = cupboardIMG_arr[1]
        elif self.color == red:
            self.image = cupboardIMG_arr[2]
        elif self.color == blue:
            self.image = cupboardIMG_arr[3]


        self.rect.width = self.width-10
        self.rect.height = self.height
# 
# class for virus.
class virus(pygame.sprite.Sprite):
    height = blocksize
    width = blocksize
    global curr_powerup
    def __init__(self,p,gameMode):
       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.height = self.height-25
        self.rect.width = self.width
        self.movecount = 0
        self.incr = 1
        self.image = virusIMG[self.movecount]
        self.path = []
        for i in p:
            self.path.append((i[0]*blocksize,i[1]*blocksize))
        print(self.path)
        self.nextpoint = self.path[0]
        self.rect.x = self.path[0][0]
        self.rect.y = self.path[0][1]
        self.speed = virusSpeedarr[gameMode]

    def update(self):
        self.image = virusIMG[self.movecount//4]
        if self.movecount == 0:
            self.incr = 1
        if self.movecount == 15:
            self.incr = -1
        self.movecount+=self.incr
        if (self.nextpoint==(self.rect.x,self.rect.y)):
            if self.path.index((self.rect.x,self.rect.y))==0:
                self.nextpoint = self.path[1]
            elif self.path.index((self.rect.x,self.rect.y))>=len(self.path)-1:
                self.nextpoint = self.path[len(self.path)-2]
            else:
                incr = random.choice([1,1,1,-1,-1,-1])
                self.nextpoint = self.path[self.path.index((self.rect.x,self.rect.y))+incr]
            # print(self.nextpoint)

        elif curr_powerup != 0:
            if self.rect.x < self.nextpoint[0]:
                self.rect.x += self.speed
            elif self.rect.x > self.nextpoint[0]:
                self.rect.x -= self.speed
            elif self.rect.y < self.nextpoint[1]:
                self.rect.y += self.speed
            elif self.rect.y > self.nextpoint[1]:
                self.rect.y -= self.speed
#
# class for powerups
class powerup(pygame.sprite.Sprite):
    height = blocksize
    width = blocksize
    def __init__(self,typ,x,y,appeartime,dissappeartime):
        super().__init__()
        self.typ = typ
        self.appeartime = appeartime
        self.dissappeartime = dissappeartime
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.rect.width = self.width-10
        self.rect.height = self.height-25
        self.imagearr = powerupIMGarr[self.typ%(len(powerupIMGarr))]
        self.imgstate = 0
        self.image =self.imagearr[self.imgstate]
        self.incr = 1

    def update(self):
        if self.imgstate==0:
            self.incr=1
        if self.imgstate==15:
            self.incr=-1
        self.image = self.imagearr[self.imgstate//4]
        self.imgstate +=self.incr

# function to display any message text
def messageDisplay(text,color,x,y,size):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    textSurface = largeText.render(text, True, color)
    TextRect = textSurface.get_rect()
    TextRect.x = x
    TextRect.y = y
    win.blit(textSurface, TextRect)
    pygame.display.update()
# 
# Quitmenu
def quitmenu():
    global rungame
    global displayMenu
    global run
    doquit = True
    while doquit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    # rungame = False
                    # pygame.quit()
                    # sys.exit()
                    displayMenu = True
                    doquit = False
                elif event.key == pygame.K_r:
                    doquit = False
                    run = True

# Main loop including menu. Game loop is inside this main loop

displayMenu = True
rungame = True
run = True
while rungame:

    menuitemnum = 0
    gameMode = 0
    while(displayMenu):
        for event in [pygame.event.wait()]:
            if event.type == pygame.QUIT:
                print("quit")
                rungame = False
                run = False
                displayMenu = False
        keyspressed = pygame.key.get_pressed()
        if keyspressed[pygame.K_DOWN]:
            menuitemnum = (menuitemnum+1)%4
        if keyspressed[pygame.K_UP]:
            menuitemnum = (menuitemnum+3)%4
        if keyspressed[pygame.K_x]:
            if menuitemnum == 0:
                displayMenu = False
                gameMode = 0
                run = True
            if menuitemnum == 1:
                displayMenu = False
                gameMode = 1
                run = True
            if menuitemnum == 2:
                displayMenu = False
                gameMode = 2
                run = True
            if menuitemnum == 3:
                rungame = False
                run = False
                displayMenu = False        
        win.blit(menuBG,(0,0))
        menuitems = [(125,100,25,25),(125,175,25,25),(125,250,25,25),(125,325,25,25)]
        pygame.draw.rect(win,blue,menuitems[menuitemnum])
        pygame.display.update()
   
    # sprite groups
    player_sprites = pygame.sprite.Group()
    virus_sprites = pygame.sprite.Group()
    allSprites = pygame.sprite.Group()
    beds_sprites = pygame.sprite.Group()
    cupboard_sprites = pygame.sprite.Group()
    powerup_sprites = pygame.sprite.Group()
    allSpritesLayered = pygame.sprite.LayeredUpdates()
    # 
    ##############################################Level Design#####################################################
    #1. nurse
    nurse = player(200,300)
    #2. beds Max 8 beds as there are only 8 spriteimages
    #   If you want to add more beds than 8, comment out the line 'usedbedIMG.append(self.image)' in bed class __init__ function
    beds  = [Bed((blocksize)*2,(blocksize)*3),
        Bed((blocksize)*4,(blocksize)*3),
        Bed((blocksize)*6,(blocksize)*3),   
        Bed((blocksize)*8,(blocksize)*3)]
    #3. cupboards
    cupboards = [cupboard(red,blocksize*1.5,gameheight-blocksize-25),
            cupboard(blue,blocksize*4.5,gameheight-blocksize-25),
            cupboard(green,blocksize*7.5,gameheight-blocksize-25)]
    #4. Virus
    virus1 = virus([(1,5),(3,5),(5,5),(7,5),(8,5)],gameMode)
    virus2 = virus([(1,8),(3,8),(5,8),(7,8),(8,8)],gameMode)

    #5.powerups
    mask1 = powerup(1,1*blocksize,6*blocksize,5,20)
    handwash1 = powerup(0,8*blocksize,6*blocksize,40,50)
    ###################################################Level Design over##############################################
    
    nurse.add(player_sprites,allSprites)
    for bed in beds:
        bed.add(beds_sprites,allSprites)
    for cp in cupboards:
        cp.add(cupboard_sprites,allSprites) 
    allSprites.add(virus1,virus2)
    virus_sprites.add(virus1,virus2)
    powerup_sprites.add(mask1,handwash1)
    # Game loop  
    startticks = pygame.time.get_ticks()
    gamedDone = False
    curr_powerup = -1
    # This below statement it to avoid using same bed sprite image for all patients
    usedbedIMG = []
    while(run):
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                run = False
        
        # move the nurse according to the keypressed. If X is pressed, take/give medicine if in right position
        keyspressed = pygame.key.get_pressed()
        nurse.move(keyspressed,beds_sprites)
        nurse.move(keyspressed,beds_sprites)
        #if all patients die, quit
        if len(beds_sprites) <= 0:
            run =False

        # refresh the screen
        win.fill(black)
        win.blit(background,(0,0))  
        # Display clock
        seconds=(pygame.time.get_ticks()-startticks)//1000
        messageDisplay(str("Doctor arrives in ")+str(gameTime-seconds)+str(" seconds"),white,0,0,15)
        if seconds>=gameTime:
            gamedDone = True
            run=False
        # Creating layered sprites(2.5D)
        allSpritesLayered.empty()
        for sprite in allSprites:
            allSpritesLayered.add(sprite,layer = sprite.rect.y)
        # check if nurse dead
        if (nurse.dead):
            nurse.image = pygame.image.load(os.path.join(nurse.file_name,"nurse_dead.png"))
            run = False
        # Drawing the sprites
        allSpritesLayered.draw(win)
        # Boxes and grid
        # for i in range(0,500,50):
        #     pygame.draw.line(win,white,(i,0),(i,500))
        # for i in range(0,500,50):
        #     pygame.draw.line(win,white,(0,i),(500,i))
        for sprite in allSpritesLayered:
            pygame.draw.rect(win,red,sprite.rect,1)
        # Draw bars above bed and selected color box above nurse
        allSpritesLayered.update()
        
        for p_ups in powerup_sprites:
            if pygame.time.get_ticks()-startticks>=p_ups.appeartime*1000:
                p_ups.appeartime = gameTime+10
                allSprites.add(p_ups)
            if pygame.time.get_ticks()-startticks>=p_ups.dissappeartime*1000:
                p_ups.kill()
            
        if curr_powerup==-1:
            poweruptime = pygame.time.get_ticks()
        elif pygame.time.get_ticks()-poweruptime>10000:
            curr_powerup = -1
            
        # draw selected color above nurse
        pygame.display.update()
    # Game Loop Over   
    # 
    #
    #
    # Display winmessage if win
    patientsSaved = len(beds_sprites)
    if(patientsSaved!=0 and gamedDone):
        print("quiting")
        if patientsSaved == len(beds):
            win.blit(congotext,(100,250))
            pygame.display.update()
        else:
            win.blit(okText,(80,250))
            pygame.display.update()
        quitmenu()
    # 
    # Display message if lose
    elif(patientsSaved == 0):
        win.blit(badText,(50,250))
        pygame.display.update()
        quitmenu()
    # player died
    elif nurse.dead:
        win.blit(deadtext,(80,250))
        pygame.display.update()
        quitmenu()
# Main loop over
pygame.quit()