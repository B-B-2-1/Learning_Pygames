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
    max_v_speed = 20
    max_h_speed = 10
    move_l = False
    move_r = False
    jumpable = False
    wallcollided = False
    floorcollided = False
    collidedRect = 0
    wallJumpedRect = 0

    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.v_speed = 1
        self.h_speed = 0
    
    def move_vertical(self):
        self.rect.y += self.v_speed
        coll = False
        for rect in rectangles:
            if self.rect.colliderect(rect):
                self.collidedRect = rect
                coll = True
                if self.v_speed>0:
                    self.rect.bottom = rect.top
                    self.v_speed = 1
                elif self.v_speed<=0:
                    self.rect.top = rect.bottom
                    self.v_speed = 0
            elif self.v_speed<self.max_v_speed:
                self.v_speed+=self.gravity
        if self.floorcollided == False and coll == True:
            self.jumpable = True #first floorcoll
            self.wallJumpedRect = 0
            if not((self.h_speed>0 and self.move_r) or (self.h_speed<0 and self.move_l)):
                self.h_speed = 0
        if self.floorcollided == True and coll == False:
            self.jumpable = False
        self.floorcollided = coll

    def move_horizontal(self):
        if self.move_l or self.move_r or not(self.wallcollided or self.floorcollided):
            self.rect.x+=self.h_speed
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
            coll = False
            for rect in rectangles:
                if self.rect.colliderect(rect):
                    self.collidedRect = rect
                    coll = True
                    if self.h_speed<0:
                        self.rect.left = rect.right
                    if self.h_speed>0:
                        self.rect.right = rect.left
            if self.wallcollided == False and coll == True:
                self.jumpable = True#First wall coll
                self.max_v_speed = 5
            if self.wallcollided == True and coll == False:
                if not(self.floorcollided):
                    self.jumpable = False
                self.max_v_speed = 20
            if self.floorcollided:
                coll = False
            self.wallcollided = coll

######################################################################Level Design
rectangles.append(pygame.Rect(0,200,320,300))
rectangles.append(pygame.Rect(400,100,100,400))
rectangles.append(pygame.Rect(0,490,500,10))
rectangles.append(pygame.Rect(220,50,100,50))
##################################################################################
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
                    if p1.wallcollided and not(p1.floorcollided) and p1.collidedRect != p1.wallJumpedRect:
                        p1.v_speed = -20
                        if p1.rect.left == p1.collidedRect.right:
                            p1.h_speed = 10
                        if p1.rect.right == p1.collidedRect.left:
                            p1.h_speed = -10
                        p1.wallJumpedRect = p1.collidedRect
                        p1.max_v_speed = 20
                    elif p1.floorcollided :
                        p1.v_speed = -20
                        p1.jumpable = False
            if event.key == pygame.K_LEFT:
                p1.move_l = True
                p1.move_r = False
                if p1.h_speed>0:
                    p1.h_speed = -1
            if event.key == pygame.K_RIGHT:
                p1.move_r = True
                p1.move_l = False
                if p1.h_speed<0:
                    p1.h_speed = 1  
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if p1.move_l and p1.floorcollided:
                    p1.h_speed = 0
                p1.move_l = False
            if event.key == pygame.K_RIGHT:
                if p1.move_r and p1.floorcollided:
                    p1.h_speed = 0
                p1.move_r = False

    win.fill((0,0,0))
    pygame.draw.rect(win,(255,255,255),p1.rect)
    for rect in rectangles:
        pygame.draw.rect(win,(255,0,0),rect)
    # for i in range(0,500,50):
    #     pygame.draw.line(win,(255,255,255),(i,0),(i,500))
    # for i in range(0,500,50):
    #     pygame.draw.line(win,(255,255,255),(0,i),(500,i))
    pygame.display.update()
    
    p1.move_vertical()
    p1.move_horizontal()
    scrollval_x = (p1.rect.x - 200)//20
    scrollval_y = (p1.rect.y - 240)//20
    p1.rect.x -= scrollval_x
    p1.rect.y -= scrollval_y
    for rect in rectangles:
        rect.x -= scrollval_x
        rect.y -= scrollval_y
    if not(p1.rect.colliderect(pygame.Rect(0,0,screenwidth,screenheight))):
        run = False

pygame.quit()
