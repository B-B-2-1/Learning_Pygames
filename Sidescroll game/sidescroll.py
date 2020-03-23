import pygame

def setDirection(keys,direction):
    dir=direction
    if(keys[pygame.K_UP]):
        if dir!=2:
            dir = 1
    elif(keys[pygame.K_DOWN]):
       if dir!=1:
            dir = 2
    elif(keys[pygame.K_LEFT]):
        if dir!=4:
            dir = 3
    elif(keys[pygame.K_RIGHT]):
        if dir!=3:
            dir = 4
    elif(keys[pygame.K_SPACE]):
        dir = 5
    return dir

screenwidth = 500
screenheight = 500

charwidth = 30
charheight = 50
stepsize = 10
dir=0

pygame.init()
win = pygame.display.setmode(screenheight,screenwidth)
pygame.set_caption("sidescroll")


isjump = False
run = True
while(run):
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    dir = setDirection(keys,dir)

    if