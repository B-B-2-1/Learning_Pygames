import pygame



blocksize = 20
gamewidth = 25*blocksize
gameheight = 25*blocksize
win = pygame.display.set_mode((gamewidth, gameheight))
clock = pygame.time.Clock()

class block(pygame.sprite.Sprite):
    height = blocksize
    width = blocksize*3

    def __init__(self,color,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.height = self.height
        self.rect.width = self.width
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
        self.speed = [5,-5]
    
    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.right>500 or self.rect.left<0:
            self.speed[0] = -self.speed[0]
        if self.rect.top<0:
            self.speed[1] = -self.speed[1]
        if self.rect.bottom>500:
            pygame.quit()


        collisions = pygame.sprite.spritecollide(self, allSprites, False)
        if(len(collisions) > 1):
            print ("col")
            for blocks in collisions:
                if blockSprites.has(blocks):
                    print("block")
                    blocks.kill()
                if self.rect.top > blocks.rect.bottom-10 or self.rect.bottom < blocks.rect.top+10:
                    self.speed[1] = -self.speed[1]
                    break
                    

allSprites = pygame.sprite.OrderedUpdates()
blockSprites = pygame.sprite.Group()

for i in range(10):
    for j in range(-(i%3)*blocksize,500,block.width):
        blockk = block((0,255,0),j,i*block.height)
        blockSprites.add(blockk)
        allSprites.add(blockk)

base = block((255,255,255),0,500-block.height-1)
allSprites.add(base)

ball1 = ball(250,250)
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
