import pygame
import os
import sys

# set main game parameters
pygame.init()
pygame.display.set_caption("FG")
clock = pygame.time.Clock()
blocksize = 50
gameheight = blocksize*10
gamewidth = blocksize*10
win = pygame.display.set_mode((gamewidth,gameheight))
# 
# define colors
white=(255,255,255)
black = (0,0,0)
green=(0,255,0)
blue=(0,0,255)
red=(255,0,0)
# 
# sprite groups
player_sprites = pygame.sprite.Group()
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
            if self.rect.y>bed.rect.y and self.rect.y<bed.rect.y+bed.rect.height:
                if self.rect.x == bed.rect.x+bed.rect.width and self.dir == 3:#nurse close to bed
                    self.selectedColor = black
                if self.rect.x+self.rect.width+1 == bed.rect.x and self.dir == 4:#nurse close to bed
                    self.selectedColor = black
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
            # if cupboard_sprites.has(collisions[1]):
                # self.selectedColor = collisions[1].color
                # print(self.selectedColor)
        
# 
# Class for beds. All behavior of beds are defined within
class Bed(pygame.sprite.Sprite):

    height = 2*blocksize
    width = 1*blocksize
    # default required medicine color of patient
    needcolor = black

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
        file_name = os.path.join(base_dir,"sprites","bed","bed_sprite.png")
        self.image = pygame.image.load(file_name)
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

# function to display any message text
def messageDisplay(text,color,x,y,size):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    textSurface = largeText.render(text, True, color)
    TextRect = textSurface.get_rect()
    TextRect.center = (x,y)
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


# Main game loop  
run = True
while(run):
    clock.tick(20) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keyspressed = pygame.key.get_pressed()
    nurse.move(keyspressed,beds_sprites)
    
    win.fill(black)   
    # Creating layered sprites(2.5D)
    allSpritesLayered.empty()
    for sprite in allSprites:
        allSpritesLayered.add(sprite,layer = sprite.rect.y)
    # Drawinf the sprites
    allSpritesLayered.draw(win)
    # draw selected color above nurse
    if(nurse.selectedColor!=(0,0,0)):
        pygame.draw.rect(win,nurse.selectedColor,(nurse.rect.x,nurse.rect.y-5,5,5))
    # 
    pygame.display.update()
    
# 
pygame.quit()