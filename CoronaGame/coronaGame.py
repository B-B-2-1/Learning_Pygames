import pygame


pygame.init()
gameheight = 500
gamewidth = 500
win = pygame.display.set_mode((gamewidth,gameheight))
pygame.display.set_caption("FG")
clock = pygame.time.Clock()

class player(object):
    speed = 2
    freeleft = True
    freeright = True
    freeup = True
    freedown = True
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = 0
        self.playerbox = (self.x,self.y,self.width,self.height)

    def move(self,keys):
        if(keys[pygame.K_UP] and self.freeup):
            self.dir = 1
            self.y -=self.speed
            self.freedown = True
            if self.y <= 0:
                self.freeup = False
        elif(keys[pygame.K_DOWN] and self.freedown):
            self.dir = 2
            self.y +=self.speed
            self.freeup = True
            if self.y + self.height > gameheight:
                self.freedown = False
        elif(keys[pygame.K_LEFT] and self.freeleft):
            self.dir = 3
            self.x -=self.speed
            self.freeright = True
            if self.x <= 0:
                self.freeleft = False
        elif(keys[pygame.K_RIGHT] and self.freeright):
            self.dir = 4
            self.x +=self.speed
            self.freeleft = True
            if self.x + self.width >= gamewidth:
                self.freeright = False

    def drawplayer(self,win):
        self.playerbox = (self.x,self.y,self.width,self.height)
        pygame.draw.rect(win,(255,255,255),self.playerbox)
        
class Bed(object):
    height = 30
    width = 20
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.bedbox = (x,y,self.width,self.height)

    def playerclose(self,nurse):
        if nurse.y + nurse.height > bed.y and nurse.y < bed.y + bed.height:
            if nurse.x + nurse.width == bed.x:
                nurse.freeright = False
            if nurse.x == bed.x + bed.width:
                nurse.freeleft = False
        if nurse.x + nurse.width > bed.x and nurse.x < bed.x + bed.width:
            if nurse.y + nurse.height == bed.y:
                nurse.freedown = False
            if nurse.y == bed.y + bed.height:
                nurse.freeup = False
        if nurse.playerbox[0]<=self.bedbox[0]+self.width+1 and nurse.playerbox[0]+nurse.playerbox[2]>=self.bedbox[0]-1:
            if nurse.playerbox[1]+nurse.playerbox[3]<=self.bedbox[1]+self.height and nurse.playerbox[1]>=self.bedbox[1]:
                return True

    def drawBed(self,win):
        pygame.draw.rect(win,(255,0,255),self.bedbox)

def messageDisplay(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    textSurface = largeText.render(text, True, (255,255,255))
    TextRect = textSurface.get_rect()
    TextRect.center = ((250),(250))
    win.blit(textSurface, TextRect)
    pygame.display.update()

run = True
nurse = player(200,200,10,20)
beds  = [Bed(300,300)]
while(run):
    clock.tick(50) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keyspressed = pygame.key.get_pressed()
    nurse.move(keyspressed)
    win.fill((0,0,0))
    print(1)
    nurse.drawplayer(win)
    
    for bed in beds:
        bed.drawBed(win)
        if bed.playerclose(nurse):
            messageDisplay("collision")

    pygame.display.update()
    
    
pygame.quit()