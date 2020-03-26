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
        self.rect.height = self.height
        self.rect.width = width*blocksize
        self.rect.x = x
        self.rect.y = y
        self.color = color
    def move_l(self,dist):
        if self.rect.left > 0:
            self.rect.x -= dist
    def move_r(self,dist):
        if self.rect.right < gamewidth:
            self.rect.x += dist
    def checkcollide(self,ball):
        corner = True
        if blockSprites.has(self):
            if self.rect.bottom == ball.rect.top and ball.rect.right >= self.rect.left and ball.rect.left <= self.rect.right:
                ball.speed[1] = abs(ball.speed[1])
                print("top",ball.rect.top)
                corner = False
                self.kill()
            if self.rect.top == ball.rect.bottom and ball.rect.right >= self.rect.left and ball.rect.left <= self.rect.right:
                ball.speed[1] = -abs(ball.speed[1])
                print("bottom",ball.rect.bottom)
                corner = False
                self.kill()
            if self.rect.right == ball.rect.left and ball.rect.top < self.rect.bottom and ball.rect.bottom > self.rect.top:
                ball.speed[0] = abs(ball.speed[0])
                print("left",ball.rect.left)
                corner = False
                self.kill()
            if self.rect.left == ball.rect.right and ball.rect.top < self.rect.bottom and ball.rect.bottom > self.rect.top:
                ball.speed[0] = -abs(ball.speed[0])
                print("right",ball.rect.right)
                corner = False
                self.kill()
            if self.rect.bottom == ball.rect.top and ball.rect.right == self.rect.left and ball.speed[0] > 0 and ball.speed[1] < 0 and corner:
                ball.speed = [-4,4]
                print("topright",ball.rect.topright)
                self.kill()
            if self.rect.bottom == ball.rect.top and ball.rect.left == self.rect.right and ball.speed[0] < 0 and ball.speed[1] < 0 and corner:
                ball.speed = [4,4]
                print("topleft",ball.rect.topleft)
                self.kill()
            if ball.rect.bottom == self.rect.top and ball.rect.right == self.rect.left and ball.speed[0] > 0 and ball.speed[1] > 0 and corner:
                ball.speed = [-4,-4]
                print("bottomright",ball.rect.bottomright)
                self.kill()
            if ball.rect.bottom == self.rect.top and ball.rect.left == self.rect.right and ball.speed[0] < 0 and ball.speed[1] > 0 and corner:
                ball.speed = [4,-4]
                print("bottomleft",ball.rect.bottomleft)
                self.kill()

        else:
            if self.rect.top == ball.rect.bottom:
                # if ball.rect.right > self.rect.left and ball.rect.left <= self.rect.right:
                #     ball.speed[1] = -abs(ball.speed[1])
                if ball.rect.right > self.rect.left and ball.rect.right <= self.rect.left + self.rect.width/4:
                    ball.speed = [-5,-2]
                if ball.rect.right > self.rect.left + self.rect.width/4 and ball.rect.right <= self.rect.left + self.rect.width/2:
                    ball.speed = [-4,-4]
                if ball.rect.right > self.rect.left + self.rect.width/2 and ball.rect.right <= self.rect.left + (self.rect.width/4)*3:
                    ball.speed = [4,-4]
                if ball.rect.right > self.rect.left + (self.rect.width/4)*3 and ball.rect.right <= self.rect.right:
                    ball.speed = [5,-2]

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
        sp = self.speed[0]
        print("xmove")
        for i in range(abs(self.speed[0])):
            if sp == self.speed[0]:
                print(i,sp)
                self.rect = self.rect.move([self.speed[0]/abs(self.speed[0]),0])
                if self.rect.right>500:
                    self.speed[0] = -abs(self.speed[0])
                if self.rect.left<0:
                    self.speed[0] = abs(self.speed[0])
                if self.rect.top<0:
                    self.speed[1] = abs(self.speed[1])
                if self.rect.bottom>500:
                    messageDisplay("Game over",(255,255,255),200,250,20)
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN :
                                pygame.quit()
                                sys.exit()

                for wall in allSprites:
                    if wall == ball1:
                        continue
                    wall.checkcollide(ball1)
        sp = self.speed[1]
        print("ymove")
        for i in range(abs(self.speed[1])):
            if sp == self.speed[1]:
                print(i,sp)
                self.rect = self.rect.move([0,self.speed[1]/abs(self.speed[1])])
                if self.rect.right>500 or self.rect.left<0:
                    self.speed[0] = -self.speed[0]
                if self.rect.top<0:
                    self.speed[1] = -self.speed[1]
                if self.rect.bottom>500:
                    messageDisplay("Game over",(255,255,255),200,250,20)
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN :
                                pygame.quit()
                                sys.exit()
                
                for wall in allSprites:
                    if wall == ball1:
                        continue
                    wall.checkcollide(ball1)

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
    # for wall in allSprites:
    #     if wall == ball1:
    #         continue
    #     wall.checkcollide(ball1)

    win.fill((0,0,0))
    allSprites.draw(win)
    for block in blockSprites:
        pygame.draw.rect(win,(255,255,255),block.rect,1)
    pygame.display.update()
