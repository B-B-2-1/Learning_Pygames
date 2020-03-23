import pygame
import os
import sys

# set main game parameters
pygame.init()
gameheight = 500
gamewidth = 500
win = pygame.display.set_mode((gamewidth,gameheight))
pygame.display.set_caption("FG")
clock = pygame.time.Clock()
blocksize = 50
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
# 
# Player class. All behavior of player is inside this class
class player(pygame.sprite.Sprite):
    #color picked up. Default is black
    selectedColor = black
    # movement constraints
    freeleft = True
    freeright = True
    freeup = True
    freedown = True
    # path to sprite images
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(base_dir,"sprites","nurse")
    # init function. Runs when this player class is created
    def __init__(self,color, x, y,width,height):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.image = pygame.image.load(os.path.join(self.file_name,"nurses_d.png"))
        self.rect.y = y
        self.rect.x = x
        self.rect.width = width-10
        self.height = height
        self.width = width
        # player speed and direction
        self.speed = width//5
        self.dir = 0
    # when x is pressed, check if player is close to bed, if yes, feed the patient with holding color
    def feed(self,listOfBeds):
        # print (self.rect.x,self.rect.y)
        for bed in listOfBeds:
            # print(bed.rect.x,bed.rect.y,bed.rect.x+bed.rect.width,bed.rect.y+bed.rect.height)
            if self.rect.y>100 and self.rect.y<150:
                if self.rect.x == bed.rect.x+bed.rect.width and self.dir == 3:#nurse close to bed
                    self.selectedColor = (0,0,0)
                if self.rect.x+self.rect.width+1 == bed.rect.x and self.dir == 4:#nurse close to bed
                    self.selectedColor = (0,0,0)

            
    # function for moving the nurse. its a bit comple. It includes collision detection
    def move(self,keys,beds):
        freeleft = True
        freeright = True
        freeup = True
        freedown = True

        if self.rect.y <= 0:
            freeup = False
        if self.rect.y + self.height >= gameheight:
            freedown = False
        if self.rect.x <= 0:
            freeleft = False
        if self.rect.x + self.width >= gamewidth:
            freeright = False
        
                
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

        collisions = pygame.sprite.spritecollide(self, allSprites, False)
        if(len(collisions) != 1):
            if self.dir == 1:
                freeup = False
                self.rect.y+=self.speed
            if self.dir == 2:
                freedown = False
                self.rect.y-=self.speed
            if self.dir == 3:
                freeleft = False
                self.rect.x+=self.speed
            if self.dir == 4:
                freeright = False
                self.rect.x-=self.speed
            if cupboard_sprites.has(collisions[1]):
                self.selectedColor = collisions[1].color
                print(self.selectedColor)
        
# 
# Class for beds. All behavior of beds are defined within
class Bed(pygame.sprite.Sprite):

    height = 99
    width = 49
    needcolor = black

    def __init__(self,color, x, y):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.rect.width = self.width-10
        base_dir = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(base_dir,"sprites","bed","bed_sprite.png")
        self.image = pygame.image.load(file_name)
# 
# class for cupboards. All behavior of cupboards are defined within
class cupboard(pygame.sprite.Sprite):
    height = 50
    width = 50
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
        self.rect.width = self.width-10
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
nurse = player(white,200,200,50,50)
player_sprites.add(nurse)
allSprites.add(nurse)
# beds
beds  = [Bed((255,0,255),(Bed.width+1)*2+1,(Bed.height+1)*1+1),
    Bed((255,0,255),(Bed.width+1)*4+1,(Bed.height+1)*1+1),
    Bed((255,0,255),(Bed.width+1)*6+1,(Bed.height+1)*1+1),   
    Bed((255,0,255),(Bed.width+1)*8+1,(Bed.height+1)*1+1)]
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
    allSprites.draw(win)
    # draw selected color above
    if(nurse.selectedColor!=(0,0,0)):
        pygame.draw.rect(win,nurse.selectedColor,(nurse.rect.x,nurse.rect.y-5,5,5))
    # 
    pygame.display.update()
    
# 
pygame.quit()