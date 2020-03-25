import os
import random
import pygame
import math
import sys
import copy


screen = pygame.display.set_mode((500, 500))
speed=[10,-10]
clock = pygame.time.Clock()

class box(pygame.sprite.Sprite):
    def __init__(self, color,x,y,width,height):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([10, 10])
       self.image.fill(color)
       self.rect = self.image.get_rect()
       self.rect.x=x
       self.rect.y=y
       self.rect.width = width
       self.rect.height = height

class plat(pygame.sprite.Sprite):
    def __init__(self, color, width, height,x,y):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       self.rect = self.image.get_rect()
       self.rect.x=x
       self.rect.y=y

    def move_r(self,len):
        if(self.rect.right<=600):
            self.rect.x+=len
    def move_l(self,len):
        if self.rect.left>=0:
            self.rect.x-=len


player=box((0,0,0),200,300,10,10)
item=[[box((0,0,0), 10*i,10*j,10,10) for i in range(500//10)]for j in range(20)]
base=plat((0,0,0),100,20,300,480)

allSpritesLayered=pygame.sprite.LayeredUpdates()
allSprites = pygame.sprite.Group()

for i in item:
    for j in i:
        allSprites.add(j)
allSprites.add(player)
allSprites.add(base)
while True:
    clock.tick(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             sys.exit()

    screen.fill((0, 0, 255))
    allSpritesLayered.empty()
    for sprite in allSprites:
        allSpritesLayered.add(sprite,layer = sprite.rect.y)

    allSpritesLayered.draw(screen)  
    for sprites in allSprites:
        pygame.draw.rect(screen,(255,255,255),sprites.rect,1)
    
    player.rect = player.rect.move(speed)
    if player.rect.left <= 0 or player.rect.right >= 500:
        speed[0] = -speed[0]
    if player.rect.top <= 0 or player.rect.bottom >= 500:
        speed[1] = -speed[1]
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        base.move_l(5)
    if keys[pygame.K_RIGHT]:
        base.move_r(5)
    
    p1 = box((0,0,0),200,300,10,10)
    p2 = box((0,0,0),200,300,10,10)
    p3 = box((0,0,0),200,300,10,10)
    p1.rect = player.rect.move([speed[0],0])
    p2.rect = player.rect.move([0,speed[1]])
    p3.rect = player.rect.move([speed[0],speed[1]])

    for i in allSprites:
        if i==player:
            continue
        elif i==base:
            if player.rect.bottom == i.rect.top and player.rect.right>i.rect.left and player.rect.left<i.rect.right:
                speed[1] =- speed[1]
        else:
            if pygame.sprite.collide_rect(i,p1) or pygame.sprite.collide_rect(i,p2):
                if pygame.sprite.collide_rect(i,p1):
                    speed[0] = -speed[0]
                    i.kill()
                if pygame.sprite.collide_rect(i,p2):
                    speed[1] = -speed[1]
                    i.kill()
            elif pygame.sprite.collide_rect(i, p3):
                    speed[0] = -speed[0]
                    speed[1] = -speed[1]
                    i.kill()
    

    pygame.display.update()