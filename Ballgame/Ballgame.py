import pygame
import sys

# Required constants and initialisations
blocksize = 20
gamewidth = 50*blocksize
gameheight = 25*blocksize
pygame.init()
win = pygame.display.set_mode((gamewidth, gameheight))
clock = pygame.time.Clock()
# 
# Function to display messages on screen during game. Example "Game over" message at end
def messageDisplay(text,color,x,y,size):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    textSurface = largeText.render(text, True, color)
    TextRect = textSurface.get_rect()
    TextRect.x = x
    TextRect.y = y
    win.blit(textSurface, TextRect)
    pygame.display.update()

class block(pygame.sprite.Sprite):
    # Height of block. Width is defined at initialisation
    height = blocksize
    # Initialisation using parameters
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
    # Move base left function
    def move_l(self,dist):
        if self.rect.left > 0:
            self.rect.x -= dist
    # 
    # Move base right function
    def move_r(self,dist):
        if self.rect.right < gamewidth:
            self.rect.x += dist
    # 
    # Fumction to check collision with the ball. This has to check every condition separately, otherwise it wont be even near perfect
    # I havnt come up with a shortcut yet
    # Each If checks for collision of each side of the ball. The side checked is shown in the print statement
    #                                                                                   eg: print("topright",ball.rect.topright)
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
                ball.speed = [-abs(ball.speed[0]),abs(ball.speed[1])]
                print("topright",ball.rect.topright)
                self.kill()
            if self.rect.bottom == ball.rect.top and ball.rect.left == self.rect.right and ball.speed[0] < 0 and ball.speed[1] < 0 and corner:
                ball.speed = [abs(ball.speed[0]),abs(ball.speed[1])]
                print("topleft",ball.rect.topleft)
                self.kill()
            if ball.rect.bottom == self.rect.top and ball.rect.right == self.rect.left and ball.speed[0] > 0 and ball.speed[1] > 0 and corner:
                ball.speed = [-abs(ball.speed[0]),-abs(ball.speed[1])]
                print("bottomright",ball.rect.bottomright)
                self.kill()
            if ball.rect.bottom == self.rect.top and ball.rect.left == self.rect.right and ball.speed[0] < 0 and ball.speed[1] > 0 and corner:
                ball.speed = [abs(ball.speed[0]),-abs(ball.speed[1])]
                print("bottomleft",ball.rect.bottomleft)
                self.kill()

        else:
            # For different positions on the base, the ball bounces differently
            # 
            #       O                          O                     O                         O
            #           ..                      ..                  ..                    .. 
            #                ..                  ..                ..                 ..
            #                     ..              ..              ..              ..
            #                          ..           ..           ..          ..
            # Base ::::::>       (:::::::A:::::|:::::B:::::|:::::C:::::|:::::D:::::)

            if self.rect.top == ball.rect.bottom:
                if ball.rect.right > self.rect.left - ball.rect.width and ball.rect.right <= self.rect.left + self.rect.width/4:
                    ball.speed = [-5,-2]
                if ball.rect.right > self.rect.left + self.rect.width/4 and ball.rect.right <= self.rect.left + self.rect.width/2:
                    ball.speed = [-4,-4]
                if ball.rect.right > self.rect.left + self.rect.width/2 and ball.rect.right <= self.rect.left + (self.rect.width/4)*3:
                    ball.speed = [4,-4]
                if ball.rect.right > self.rect.left + (self.rect.width/4)*3 and ball.rect.left <= self.rect.right:
                    ball.speed = [5,-2]

class ball(pygame.sprite.Sprite):
    #Set ball height and width
    height = 1*blocksize    
    width = 1*blocksize
    # Initialize ball with starting x and y positions
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.height = self.height
        self.rect.width = self.width
        self.rect.x = x
        self.rect.y = y
        # At start, speed in X direction = 4 pixels per frame(to right) , Y direction = 4 pixels per frame (Up direction)
        self.speed = [4,-4]
    # Ball move function. I am unable to make it less complicated :(
    def move(self):
        sp = self.speed[0]
        print("xmove")
        # in this loop, ball moves pixel by pixel horizontaly to required X position
        # At each motion, checks if ball reaches boundary, if yes, invert X or Y as required
        # at each motion, check for collision with each block sprite using "wall.checkcollide(ball1)" function
        for i in range(abs(self.speed[0])):
            if sp == self.speed[0]:
                print(i,sp)
                self.rect = self.rect.move([self.speed[0]/abs(self.speed[0]),0])
                if self.rect.right>gamewidth:
                    self.speed[0] = -abs(self.speed[0])
                if self.rect.left<0:
                    self.speed[0] = abs(self.speed[0])
        
                for wall in allSprites:
                    if wall == ball1:
                        continue
                    # wall.checkcollide is defined inside block class above
                    wall.checkcollide(ball1)
        sp = self.speed[1]
        print("ymove")
        # Repeats same steps as previous loop byt in Y direction
        for i in range(abs(self.speed[1])):
            if sp == self.speed[1]:
                print(i,sp)
                self.rect = self.rect.move([0,self.speed[1]/abs(self.speed[1])])
                if self.rect.top<0:
                    self.speed[1] = -self.speed[1]
                if self.rect.bottom>gameheight:
                    messageDisplay("Game over",(255,255,255),450,250,20)
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN :
                                pygame.quit()
                                sys.exit()
                
                for wall in allSprites:
                    if wall == ball1:
                        continue
                    wall.checkcollide(ball1)

# Creating the sprites - Blocks, Ball, and Base platform
allSprites = pygame.sprite.OrderedUpdates()
blockSprites = pygame.sprite.Group()

# This loop might look bit complex, but just adding the blocks to correct position
for i in range(10):
    for j in range(-(i%3)*blocksize,gamewidth,3*blocksize):
        blockk = block((0,255,0),j,i*block.height,3)
        blockSprites.add(blockk)
        allSprites.add(blockk)
# 
base = block((255,255,255),0,500-block.height,5)
allSprites.add(base)

ball1 = ball(200,300)
allSprites.add(ball1)
# 

# Main Loop
while(True):
    # 50 frames per second
    clock.tick(50)
    # 
    # check if user closes game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
    # 
    # If right or left keys are pressed, move the base platform (functions inside block class) 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        base.move_l(10)
    if keys[pygame.K_RIGHT]:
        base.move_r(10)
    # 
    # Move the ball. This includes move function inside ball class and collision check function inside block class
    # Can also write this code with collision detection function inside the ball class
    ball1.move()

    # Clear screen and draw the sprites(blocks,boxes and base-platform)
    win.fill((0,0,0))
    allSprites.draw(win)
    for block in blockSprites:
        pygame.draw.rect(win,(255,255,255),block.rect,1)
    pygame.display.update()
