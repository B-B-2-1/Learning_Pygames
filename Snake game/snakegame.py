import pygame
import random
import math

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def setSnakeDirection(keys,direction):
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
    return dir

def messageDisplay(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    textSurface = largeText.render(text, True, (255,255,255))
    TextRect = textSurface.get_rect()
    TextRect.center = ((250),(250))
    win.blit(textSurface, TextRect)
    pygame.display.update()

pygame.init()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("FG")

height=10
width=10
speed=10
dir=0
score = 0

snake = [(255,255),(255,255),(255,255),(255,255)]
headcentre = (snake[0][0]+width/2,snake[0][1]+height/2)
fruit = (10+random.randrange(49)*10,10+random.randrange(49)*10)

run=True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    dir = setSnakeDirection(keys,dir)

#move snake body
    if dir != 0:
        for i in range(len(snake)-1,0,-1):
            snake[i] = snake[i-1]
#move snake head 
    if dir == 1:
        snake[0] = (snake[0][0],snake[0][1]-speed)
    elif dir == 2:
        snake[0] = (snake[0][0],snake[0][1]+speed)
    elif dir == 3:
        snake[0] = (snake[0][0]-speed,snake[0][1])
    elif dir == 4:
        snake[0] = (snake[0][0]+speed,snake[0][1]) 

#draw background
    win.fill((255,255,255))
    pygame.draw.rect(win,(0,0,0),(5,5,500-width,500-height))
# draw fruit
    pygame.draw.circle(win,(0,0,255),fruit,5)
# draw snake body
    for part in snake:
        pygame.draw.rect(win,(255,0,0),(part[0],part[1],10,10))
# draw snake head
    pygame.draw.rect(win,(0,255,0),(snake[0][0],snake[0][1],10,10))

    pygame.display.update()

# got fruit
    if distance(headcentre,fruit)<10:
        score+=10
        for i in range(4):
            snake.append(snake[len(snake)-1])
        b=(10+random.randrange(49)*10,10+random.randrange(49)*10)
        while snake.count(b):
            b=(10+random.randrange(49)*10,10+random.randrange(49)*10)
        fruit = b
# crash
    headcentre = (snake[0][0]+width/2,snake[0][1]+height/2)
    if dir !=0:
        if snake.count(snake[0])>1 or (headcentre[0]<width) or (headcentre[0]>500-width) or (headcentre[1]<width) or (headcentre[1]>500-width):
            run = False
            messageDisplay("you crashed.  Your score is : "+str(score))
            pygame.time.delay(1000)

# print score
print("score = ")
print(score)
# if game over, wait for keypress to stop
if pygame.event.wait().type == pygame.KEYDOWN:
    pygame.quit()    