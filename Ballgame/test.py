import pygame
import sys


blocksize = 20
gamewidth = 25*blocksize
gameheight = 25*blocksize
pygame.init()
win = pygame.display.set_mode((gamewidth, gameheight))
clock = pygame.time.Clock()


def messageDisplay(text,color,x,y,size):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    textSurface = largeText.render(text, True, color)
    TextRect = textSurface.get_rect()
    TextRect.x = x
    TextRect.y = y
    win.blit(textSurface, TextRect)
    pygame.display.update()

class block(pygame.sprite.Sprite):
    height = blocksize

    def __init__(self,color,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width*blocksize, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.height = self.height-2
        self.rect.width = width*blocksize-2
        self.rect.x = x
        self.rect.y = y
        self.color = color
    def move_l(self,dist):
        if self.rect.left > 0:
            self.rect.x -= dist
    def move_r(self,dist):
        if self.rect.right < gamewidth:
            self.rect.x += dist
    

class ball(pygame.sprite.Sprite):
    height = 1*blocksize
    width = 1*blocksize

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.height = self.height
        self.rect.width = self.width
        self.rect.x = x
        self.rect.y = y
        self.speed = [4,-4]
    
    def move(self):
        

        

allSprites = pygame.sprite.OrderedUpdates()
blockSprites = pygame.sprite.Group()

for i in range(10):
    for j in range(-(i%3)*blocksize,500,3*blocksize):
        blockk = block((0,255,0),j,i*block.height,3)
        blockSprites.add(blockk)
        allSprites.add(blockk)

base = block((255,255,255),0,500-block.height,5)
allSprites.add(base)

ball1 = ball(200,300)
allSprites.add(ball1)

while(True):
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        base.move_l(10)
    if keys[pygame.K_RIGHT]:
        base.move_r(10)

    ball1.move()

    win.fill((0,0,0))
    allSprites.draw(win)
    for block in blockSprites:
        pygame.draw.rect(win,(255,255,255),block.rect,1)
    pygame.display.update()
