import sys
from random import randint
from math import floor
import pygame
from pygame.locals import *
#Balloon object with functions that pick color of balloon at random and change balloon color when clicked; in this order: Blue, Green, Red.
class balloon:
    def __init__(self,x):
        self.x = x
        self.y = 500
        self.bloonColor = None
        self.img = None
        self.imgPopped = 'assets/bloonRedPopped.png'
        self.popped = False
        self.popTimer = 5
    #Function to pick random balloon color    
    def pickColor(self):
        color = randint(1,3)
        match color: 
            case 1:
                self.bloonColor = 'Red'
                self.img = 'assets/bloonRed.png'
                self.popTimer = 5
            case 2:
                self.bloonColor = 'Green'
                self.img = 'assets/bloonGreen.png'
            case 3:
                self.bloonColor = "Blue"
                self.img = 'assets/bloonBlue.png'
    #Function to change balloon color when clicked            
    def checkPopped(self):
        if self.popped:
            if self.bloonColor == 'Blue':
                self.bloonColor = 'Green'
                self.img = 'assets/bloonGreen.png'
                self.popTimer = 0
                self.popped = False
            elif self.bloonColor == 'Green':
                self.bloonColor = 'Red'
                self.img = 'assets/bloonRed.png'
                self.popTimer = 0
                self.popped = False
#Initiate Pygame  with fonts and window caption              
pygame.init()
pygame.font.init()
pygame.display.set_caption('Bloon Popper')
#Set screen, font and game speed
screen = pygame.display.set_mode((500,500))
gameFont = pygame.font.SysFont('Comic Sans MS', 20)
clock = pygame.time.Clock()
#Create empty list to hold balloon objects
bloonList = []
#Level, blooncounter (total balloons), velocity (balloon speed on y axis), popped balloon and lost balloon variables 
level = 1
bloonCounter = 1
velocity = 1
popped = 0
lost = 0
#Standard Pygame loop
while True:
    #Fill screen with blue sky (Clouds comming soon... maybe.)
    screen.fill((0,160,230))
    #Making labels for Current Level, lost balloons and popped balloons
    poppedBloons = gameFont.render('Popped: %s'%(popped), False, (0, 0, 0))
    lostBloons = gameFont.render('Lost: %s'%(lost), False, (0, 0, 0))
    currentLevel = gameFont.render('Level: %s'%(level), False, (0, 0, 0))
    screen.blit(poppedBloons, (1,0))
    screen.blit(lostBloons, (1,21))
    screen.blit(currentLevel, (215,1))
    #Setting level conditions based off of popped baloons
    if popped == 30:
        level = 2
    elif popped >= 100:
        level = 3
    #Setting balloon spawn rate bassed on level
    if level == 1:
        if bloonCounter >= 5:
            bloonCounter = 5
    elif level == 2:
        if bloonCounter >= 10:
            bloonCounter = 10
    else:
        if bloonCounter >= 20:
            bloonCounter = 20
    #Setting velocity (speed on y axis) of balloons based on level
    if level < 3:
        if velocity >= 2:
            velocity = 2 
    else:
        if velocity >= 5:
            velocity = 5  
    #Creating and adding balloon objects to empty list based on balloon counter
    if len(bloonList) < floor(bloonCounter):
        x = randint(40,460)
        b = balloon(x)
        b.pickColor()
        bloonList.append(b)
    #Assigning mouse postion to x,y variables
    mx, my = pygame.mouse.get_pos()
    #Iterating over balloons in balloon list
    for entity in bloonList:
        #Loading balloon image and adding rect
        bloon = pygame.image.load(entity.img)
        bloon.set_colorkey('white')
        bloonRect = bloon.get_rect(topleft = [entity.x, entity.y])
        #Condition to get rid of offscreen balloons and add to lost variable
        if entity.y <= -50:
            bloonList.remove(entity)
            lost += 1
        #Checking for mouse collisions with rects
        if bloonRect.collidepoint(mx,my) == True and pygame.mouse.get_pressed() == (1,0,0) and entity.popTimer >= 5:
            #Setting popped to true, but will only stay true if current balloon is red
            entity.popped = True
            entity.checkPopped()
            #Blits popped image at coords of current balloon entity 
            if entity.popped == True:
                del bloon
                del bloonRect
                bloon = pygame.image.load(entity.imgPopped)
                bloon.set_colorkey('white')
                bloonRect = bloon.get_rect(topleft = [entity.x-15, entity.y-15])
                #Adding to variables after pop for game progression
                bloonCounter += 0.2
                velocity += 0.05
                popped += 1
            #This statement is meant for when checkPopped returns a balloon other than red
            else:
                del bloon
                del bloonRect
                bloon = pygame.image.load(entity.img)
                bloon.set_colorkey('white')
                bloonRect = bloon.get_rect(topleft = [entity.x, entity.y])
        #Moving Balloon    
        entity.y -= velocity
        #Removing Balloon or adding poptimer (poptimer is needed to make sure all balloon colors don't pop at once)
        if entity.popped:
            screen.blit(bloon,bloonRect)
            bloonList.remove(entity)
        else:
            screen.blit(bloon,bloonRect)
            entity.popTimer += 1
    #Standard pygame exit conditions        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    #Update and clock
    pygame.display.update()
    clock.tick(60)
