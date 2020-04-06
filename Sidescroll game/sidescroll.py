import pygame


screenwidth = 500
screenheight = 500
logNo=0
pygame.init()
pygame.display.set_caption("sidescroller")
win = pygame.display.set_mode((screenwidth,screenheight))

clock = pygame.time.Clock()

rectangles = []

class player():

    height = 50
    width = 20
    gravity = 1
    v_speed = 1
    h_speed = 1
    jumpable = False
    move_l = False
    move_r = False
    max_v_speed = 20
    h_collided = False
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.v_speed = 1
    
    def move_vertical(self):

        self.rect.y += self.v_speed
        for rect in rectangles:
            if self.rect.colliderect(rect):
                if self.v_speed>0:
                    self.rect.bottom = rect.top
                    self.jumpable = True
                    self.v_speed = 1
                elif self.v_speed<=0:
                    self.rect.top = rect.bottom
                    self.v_speed = 0
            elif self.v_speed<self.max_v_speed:
                self.v_speed+=self.gravity

    def move_horizontal(self):
        if self.move_l or self.move_r:
            self.rect.x += self.h_speed
            if self.move_l:
                if self.h_speed>-10:
                    self.h_speed-=1
                if self.h_speed == 0:
                    self.h_speed = -1
            if self.move_r:
                if self.h_speed<10:
                    self.h_speed+=1
                if self.h_speed == 0:
                    self.h_speed = 1
            collided = False
            for rect in rectangles:
                if self.rect.colliderect(rect):
                    collided = True
                    self.max_v_speed = 5
                    if self.h_speed>0:
                        self.rect.right = rect.left
                    if self.h_speed<=0:
                        self.rect.left = rect.right
            if self.h_collided == False and collided == True:
                self.v_speed = 0
            self.h_collided = collided
            if not(self.h_collided):
                self.max_v_speed = 20
            global logNo
            print("collided",logNo)
            logNo+=1
        else:
            self.h_collided = False

rectangles.append(pygame.Rect(0,300,320,200))
rectangles.append(pygame.Rect(400,100,100,400))
rectangles.append(pygame.Rect(0,490,500,10))
rectangles.append(pygame.Rect(120,100,200,100))
p1 = player(200,100)


run = True
while(run):
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if p1.jumpable:
                    p1.v_speed = -20  
                    p1.jumpable = False
                if p1.h_collided:
                    p1.v_speed = -20
                    p1.jumpable = False
                    p1.h_collided = False
                    # p1.h_speed = -(p1.h_speed/abs(p1.h_speed))*15
                    if p1.move_l:
                        p1.h_speed = 15
                    if p1.move_r:
                        p1.h_speed = -15
                    p1.max_v_speed = 20
            if event.key == pygame.K_LEFT:
                if p1.h_speed>0:
                    p1.h_speed = -1
                p1.move_l = True
            if event.key == pygame.K_RIGHT:
                if p1.h_speed <= 0:
                    p1.h_speed = 1
                p1.move_r = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                p1.move_l = False
                p1.max_v_speed = 20
            if event.key == pygame.K_RIGHT:
                p1.move_r = False
                p1.max_v_speed = 20


    win.fill((0,0,0))
    pygame.draw.rect(win,(255,255,255),p1.rect)
    for rect in rectangles:
        pygame.draw.rect(win,(255,0,0),rect)
    pygame.display.update()

    p1.move_vertical()
    p1.move_horizontal()
    if not(p1.rect.colliderect(pygame.Rect(0,0,screenwidth,screenheight))):
        run = False

pygame.quit()
