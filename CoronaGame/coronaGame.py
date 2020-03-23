import pygame


pygame.init()
gameheight = 500
gamewidth = 500
win = pygame.display.set_mode((gamewidth,gameheight))
pygame.display.set_caption("FG")
clock = pygame.time.Clock()

allSprites = pygame.sprite.Group()
beds_sprites = pygame.sprite.Group()

class player(pygame.sprite.Sprite):
    speed = 2
    freeleft = True
    freeright = True
    freeup = True
    freedown = True
    def __init__(self,color, x, y,width,height):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.dir = 0
        self.height = height
        self.width = width

    def move(self,keys,beds):
        freeleft = True
        freeright = True
        freeup = True
        freedown = True

        if self.rect.y <= 0:
            freeup = False
        if self.rect.y + self.height > gameheight:
            freedown = False
        if self.rect.x <= 0:
            freeleft = False
        if self.rect.x + self.width >= gamewidth:
            freeright = False
        
        collisions = pygame.sprite.spritecollide(self, beds, False)
        if(len(collisions) != 0):
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
                
        if(keys[pygame.K_UP] and freeup):
            self.dir = 1
            self.rect.y -=self.speed
        elif(keys[pygame.K_DOWN] and freedown):
            self.dir = 2
            self.rect.y +=self.speed
        elif(keys[pygame.K_LEFT] and freeleft):
            self.dir = 3
            self.rect.x -=self.speed
        elif(keys[pygame.K_RIGHT] and freeright):
            self.dir = 4
            self.rect.x +=self.speed

        
class Bed(pygame.sprite.Sprite):
    height = 30
    width = 20
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

def messageDisplay(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    textSurface = largeText.render(text, True, (255,255,255))
    TextRect = textSurface.get_rect()
    TextRect.center = ((250),(250))
    win.blit(textSurface, TextRect)
    pygame.display.update()


nurse = player((255,255,255),200,200,10,20)
allSprites.add(nurse)
beds  = [Bed((255,0,255),300,300)]
for bed in beds:
    allSprites.add(bed)
    beds_sprites.add(bed)

run = True
while(run):
    clock.tick(50) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keyspressed = pygame.key.get_pressed()
    nurse.move(keyspressed,beds_sprites)
    win.fill((0,0,0))   
    allSprites.draw(win)
    pygame.display.update()
    
    
pygame.quit()