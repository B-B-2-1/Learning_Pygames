import pygame
import os
import sys
import random

# set main game parameters
pygame.init()
pygame.display.set_caption("FG")
clock = pygame.time.Clock()
blocksize = 50
gameheight = blocksize*10
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
base_dir = os.path.abspath(os.path.dirname(__file__))
file_name = os.path.join(base_dir,"env","floortile.png")
background = pygame.image.load(file_name)
# 
# sprite groups
player_sprites = pygame.sprite.Group()
virus_sprites = pygame.sprite.Group()
allSprites = pygame.sprite.Group()
beds_sprites = pygame.sprite.Group()
cupboard_sprites = pygame.sprite.Group()
allSpritesLayered = pygame.sprite.LayeredUpdates()
# 
# Player class. All behavior of player is inside this class
class player(pygame.sprite.Sprite):
    #color picked up. Default is black
    selectedColor = black
    spriteHeight = blocksize
    spriteWidth = blocksize
    # movement constraints
    freeleft = True
    freeright = True
    freeup = True
    freedown = True
    # is dead yet?
    dead = False
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
        self.image = pygame.image.load(os.path.join(self.file_name,"nurses_d.png"))
        self.rect.y = y
        self.rect.x = x
        self.rect.width = self.spriteWidth-10
        self.rect.height = self.spriteHeight-20
        # player speed and direction
        self.speed = blocksize//5
        self.dir = 0
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
        freeleft = True
        freeright = True
        freeup = True
        freedown = True
        if self.rect.y <= 0:
            freeup = False
        if self.rect.y + self.spriteHeight >= gameheight:
            freedown = False
        if self.rect.x <= 0:
            freeleft = False
        if self.rect.x + self.spriteWidth >= gamewidth:
            freeright = False
        
        # Move according to keys. If collision detected, we will reverse the move in the next block 
        if(keys[pygame.K_UP] and freeup):
            self.dir = 1
            self.rect.y -=self.speed
            self.image = pygame.image.load(os.path.join(self.file_name,"nurses_u.png"))
        elif(keys[pygame.K_DOWN] and freedown):
            self.dir = 2
            self.rect.y +=self.speed
            self.image = pygame.image.load(os.path.join(self.file_name,"nurses_d.png"))
        elif(keys[pygame.K_LEFT] and freeleft):
            self.dir = 3
            self.rect.x -=self.speed
            self.image = pygame.image.load(os.path.join(self.file_name,"nurses_l.png"))
        elif(keys[pygame.K_RIGHT] and freeright):
            self.dir = 4
            self.rect.x +=self.speed
            self.image = pygame.image.load(os.path.join(self.file_name,"nurses_r.png"))
        if(keys[pygame.K_x]):
            self.feed(beds_sprites)
            self.getfeed(cupboard_sprites)

        # reversing move if collision detected
        collisions = pygame.sprite.spritecollide(self, allSprites, False)
        if(len(collisions) != 1):
            if self.dir == 1:
                self.rect.y+=self.speed
            if self.dir == 2:
                self.rect.y-=self.speed
            if self.dir == 3:
                self.rect.x+=self.speed
            if self.dir == 4:
                self.rect.x-=self.speed
            if virus_sprites.has(collisions[1]):
                collisions[1].kill()
                self.dead = True
                
    def update(self):
        if not(self.selectedColor==black):
            pygame.draw.rect(win,self.selectedColor,(self.rect.x,self.rect.y-5,5,5))

# 
# Class for beds. All behavior of beds are defined within
class Bed(pygame.sprite.Sprite):

    height = 2*blocksize
    width = 1*blocksize
    # default required medicine color of patient
    needcolor = black
    needPercentage = float(0)
    isinNeed = False
    patientAlive = True

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
        self.rect.height = self.height-20
        # Load bed sprite image
        base_dir = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(base_dir,"sprites","bed")
        self.image = pygame.image.load(os.path.join(file_name,"bed_sprite.png"))
    
    def update(self):
        if not(self.isinNeed):
            self.isinNeed = random.randrange(1000)<10
            if self.isinNeed:
                self.needPercentage = 0
                self.needcolor = random.choice([blue,green,red])
        if self.isinNeed and self.needPercentage<100:
            # Speed with which the bar fills
            self.needPercentage += 0.2
            pygame.draw.rect(win,white,(self.rect.x-5,self.rect.y-15,5,15))
            pygame.draw.rect(win,self.needcolor,(self.rect.x-5,self.rect.y-15,5,(15*self.needPercentage)//100))
        if self.needPercentage >= 100:
            base_dir = os.path.abspath(os.path.dirname(__file__))
            file_name = os.path.join(base_dir,"sprites","bed")
            self.image = pygame.image.load(os.path.join(file_name,"coffin.png"))
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
        # loading sprites for cupboard according to color
        base_dir = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(base_dir,"sprites","cupboard")
        if self.color == white:
            self.image = pygame.image.load(os.path.join(file_name,"cupboard_white.png"))
        elif self.color == green:
            self.image = pygame.image.load(os.path.join(file_name,"cupboard_green.png"))
        elif self.color == red:
            self.image = pygame.image.load(os.path.join(file_name,"cupboard_red.png"))
        elif self.color == blue:
            self.image = pygame.image.load(os.path.join(file_name,"cupboard_blue.png"))


        self.rect.width = self.width-10
        self.rect.height = self.height
# 
# class for virus.
class virus(pygame.sprite.Sprite):
    height = blocksize
    width = blocksize
    speed = blocksize//5
    path = []
    def __init__(self,p):
       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.height = self.height
        self.rect.width = self.width
        base_dir = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(base_dir,"sprites","virus")
        self.image = pygame.image.load(os.path.join(file_name,"virus50.png"))
        self.path = []
        for i in p:
            self.path.append((i[0]*blocksize,i[1]*blocksize))
        print(self.path)
        self.nextpoint = self.path[0]
        self.rect.x = self.path[0][0]
        self.rect.y = self.path[0][1]

    def update(self):
        if (self.nextpoint==(self.rect.x,self.rect.y)):
            if self.path.index((self.rect.x,self.rect.y))==0:
                self.nextpoint = self.path[1]
            elif self.path.index((self.rect.x,self.rect.y))>=len(self.path)-1:
                self.nextpoint = self.path[len(self.path)-2]
            else:
                incr = random.choice([1,1,1,-1,-1,-1])
                self.nextpoint = self.path[self.path.index((self.rect.x,self.rect.y))+incr]
            print(self.nextpoint)

        else:
            if self.rect.x < self.nextpoint[0]:
                self.rect.x += self.speed
            elif self.rect.x > self.nextpoint[0]:
                self.rect.x -= self.speed
            elif self.rect.y < self.nextpoint[1]:
                self.rect.y += self.speed
            elif self.rect.y > self.nextpoint[1]:
                self.rect.y -= self.speed
        
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


# Now creatig nurse and beds and cupboards
# nurse
nurse = player(200,200)
player_sprites.add(nurse)
allSprites.add(nurse)
# beds
beds  = [Bed((blocksize)*2,(blocksize)*1),
    Bed((blocksize)*4,(blocksize)*1),
    Bed((blocksize)*6,(blocksize)*1),   
    Bed((blocksize)*8,(blocksize)*1)]
for bed in beds:
    allSprites.add(bed)
    beds_sprites.add(bed)
# cupboards
cupboards = [cupboard(red,blocksize*2,gameheight-blocksize),
        cupboard(blue,blocksize*4,gameheight-blocksize),
        cupboard(green,blocksize*6,gameheight-blocksize),
        cupboard(white,blocksize*8,gameheight-blocksize)]
for cp in cupboards:
    allSprites.add(cp)
    cupboard_sprites.add(cp) 
# Virus
virus1 = virus([(1,3),(3,3),(5,3),(7,3),(9,3)])
virus2 = virus([(1,6),(3,6),(5,6),(7,6),(9,6)])
allSprites.add(virus1,virus2)
virus_sprites.add(virus1,virus2)

# Main game loop  
startticks = pygame.time.get_ticks()
gamedone = False
run = True
while(run):
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # move the nurse according to the keypressed. If X is pressed, take/give medicine if in right position
    keyspressed = pygame.key.get_pressed()
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
    if seconds==gameTime:
        run=False
        gamedone=True 
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
    for i in range(0,500,50):
        pygame.draw.line(win,white,(i,0),(i,500))
    for i in range(0,500,50):
        pygame.draw.line(win,white,(0,i),(500,i))
    for sprite in allSpritesLayered:
        pygame.draw.rect(win,red,sprite.rect,1)
    # Draw bars above bed and selected color box above nurse
    allSpritesLayered.update()
    # draw selected color above nurse
    pygame.display.update()
    
# 
# Display winmessage if win
patientsSaved = len(beds_sprites)
if(patientsSaved!=0 and gamedone):
    if patientsSaved == len(beds):
        messageDisplay(str("Congratulations, you saved all patients"),white,50,gamewidth//2,20)
    else:
        messageDisplay(str("Congratulations, you managed to save ")+str(patientsSaved)+str(" patients"),white,20,gamewidth//2,20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
# 
# Display message if lose
elif(patientsSaved == 0):
    messageDisplay(str("All patients died"),white,150,gamewidth//2,20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN :
                pygame.quit()
# player died
elif nurse.dead:
    messageDisplay(str("The nurse died bravely"),white,150,gamewidth//2,20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN :
                pygame.quit()

pygame.quit()