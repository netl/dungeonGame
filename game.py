#!/usr/bin/python3
import pygame
from pygame.locals import *
import random

#setup window and graphics
class view:
   width = 1680
   height = 1050
pygame.init()
screen = pygame.display.set_mode([view.width,view.height])

class world:
   grid = 40
   players = 4
   #different settings for different amounts of players
   if(players==1): #player view on the left, map overview at the top right
      playerWindowSize = view.height
      playerWindowPosition = ((0,0),(0,0))
      squareSize = playerWindowSize/11
      mapScale = (view.width-playerWindowSize)/(squareSize*grid)
      mapOverviewPosition = (playerWindowSize,0)
   elif(players==2): #player 1 on the top right, player 2 on the top left, map overview in bottom center
      playerWindowSize = view.width/2
      playerWindowPosition = ((view.width-playerWindowSize,0),(0,0))
      squareSize = playerWindowSize/11
      mapScale = (view.height-playerWindowSize)/(squareSize*grid)
      mapOverviewPosition = (playerWindowSize-(view.height-playerWindowSize)/2,playerWindowSize)
   else: #player 1: top right, player 2: bottom left, player 3: top left, player 4: bottom right, map overview in center
      playerWindowSize = view.height/2
      playerWindowPosition = ((view.width-playerWindowSize,0),(0,view.height-playerWindowSize),(0,0),(view.width-playerWindowSize,view.height-playerWindowSize))
      squareSize = playerWindowSize/11
      mapScale = (view.width-playerWindowSize*2)/(squareSize*grid)
      mapOverviewPosition = (playerWindowSize,playerWindowSize/2)
   mapOverview = pygame.Surface((grid*squareSize*mapScale,grid*squareSize*mapScale))

class level:
   color = ((255,128,0),(0,0,0))
   def __init__(self, width, height):
      self.map = [[0 for x in range(width)] for y in range(height)]
  
   #clear the level 
   def clear(self):
      for y in range(len(self.map)):
         for x in range(len(self.map[y])):
            self.map[y][x] = 0
      return(0)
   
   #generate tunnels
   def generate(self):
      miner = player(int(world.grid/2),int(world.grid/2))
      pOne.x = miner.x
      pOne.y = miner.y
      for i in range(200):
         self.map[miner.y][miner.x] = 1 
         r = random.randint(0,3)
         stepCount = random.randint(0,5)
         if(r == 0):
            while(miner.move('up') and miner.underneath() == 1 and stepCount<5):
               pass
         elif(r == 1):
            while(miner.move('down') and miner.underneath() == 1 and stepCount<5):
               pass
         elif(r == 2):
            while(miner.move('left') and miner.underneath() == 1 and stepCount<5):
               pass
         elif(r == 3):
            while(miner.move('right') and miner.underneath() == 1 and stepCount<5):
               pass
      return(0)

class player:
   controls = {'up':K_UP,'down':K_DOWN,'left':K_LEFT,'right':K_RIGHT}
   mapColor = (255,255,255)
   perspective = pygame.Surface((world.playerWindowSize,world.playerWindowSize))

   def __init__(self,x,y):
      self.x = x
      self.y = y

   def readInput(self, keys): #do movement according to given key input
      if key[self.controls['up']]:
         self.move('up')
         if(self.underneath() == 0):
            self.move('down')
      if key[self.controls['down']]:
         self.move('down')
         if(self.underneath() == 0):
            self.move('up')
      if key[self.controls['left']]:
         self.move('left')
         if(self.underneath() == 0):
            self.move('right')
      if key[self.controls['right']]:
         self.move('right')
         if(self.underneath() == 0):
            self.move('left')
      
   def move(self, direction):
      if(direction == 'up' and self.y>0):
         self.y = self.y - 1
         return(1)
      elif(direction == 'down' and self.y<len(l.map)-1):
         self.y = self.y + 1
         return(1)
      if(direction == 'left' and self.x>0):
         self.x = self.x - 1
         return(1)
      elif(direction == 'right' and self.x<len(l.map[self.y])-1):
         self.x = self.x + 1
         return(1)
      else:
         return(0)

   def underneath(self):
      return(l.map[self.y][self.x])

   def drawView(self):
      offset=self.perspective.get_width()/2-world.squareSize/2
      #draw the grid
      for y in range(len(l.map)):
         for x in range(len(l.map[y])):
            pygame.draw.rect(self.perspective, l.color[l.map[y][x]], pygame.Rect(world.squareSize*(-self.x+x)+offset,world.squareSize*(-self.y+y)+self.perspective.get_height()/2, world.squareSize,world.squareSize))
      #draw the players
      pygame.draw.rect(self.perspective, pOne.mapColor, pygame.Rect(world.squareSize*(-self.x+pOne.x)+offset, world.squareSize*(-self.y+pOne.y)+self.perspective.get_height()/2, world.squareSize,world.squareSize))
      pygame.draw.rect(self.perspective, pTwo.mapColor, pygame.Rect(world.squareSize*(-self.x+pTwo.x)+offset, world.squareSize*(-self.y+pTwo.y)+self.perspective.get_height()/2, world.squareSize,world.squareSize))
      pygame.draw.rect(self.perspective, pThree.mapColor, pygame.Rect(world.squareSize*(-self.x+pThree.x)+offset, world.squareSize*(-self.y+pThree.y)+self.perspective.get_height()/2, world.squareSize,world.squareSize))
      pygame.draw.rect(self.perspective, pFour.mapColor, pygame.Rect(world.squareSize*(-self.x+pFour.x)+offset, world.squareSize*(-self.y+pFour.y)+self.perspective.get_height()/2, world.squareSize,world.squareSize))

#create level
l = level(world.grid,world.grid)

#generate players
pOne = player(int(world.grid/2),int(world.grid/2))
pOne.mapColor = (255,0,0)
pTwo = player(int(world.grid/2),int(world.grid/2))
pTwo.mapColor = (0,255,0)
pTwo.controls = {'up':K_w,'down':K_s,'left':K_a,'right':K_d}
pThree = player(int(world.grid/2),int(world.grid/2))
pThree.mapColor = (0,0,255)
pThree.controls = {'up':K_i,'down':K_k,'left':K_j,'right':K_l}
pFour = player(int(world.grid/2),int(world.grid/2))
pFour.mapColor = (255,255,0)
pFour.controls = {'up':K_KP8,'down':K_KP2,'left':K_KP4,'right':K_KP6}

#game variables
random.seed()
playing = 1

#main loop
while(playing):

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         playing = 0
      elif event.type == pygame.KEYDOWN:
         key = pygame.key.get_pressed()
         if key[K_SPACE]:
            l.clear()
            l.generate()
         pOne.readInput(key)
         pTwo.readInput(key)
         pThree.readInput(key)
         pFour.readInput(key)

   pOne.drawView()
   screen.blit(pOne.perspective,world.playerWindowPosition[0])

   if(world.players>1):
      pTwo.drawView()
      screen.blit(pTwo.perspective,world.playerWindowPosition[1])

   if(world.players>2):
      pThree.drawView()
      screen.blit(pThree.perspective,world.playerWindowPosition[2])
   if(world.players==4):
      pFour.drawView()
      screen.blit(pFour.perspective,world.playerWindowPosition[3])

   #draw the map
   for y in range(len(l.map)):
      for x in range(len(l.map[y])):
         pygame.draw.rect(world.mapOverview, l.color[l.map[y][x]], pygame.Rect( world.squareSize*x*world.mapScale, world.squareSize*y*world.mapScale, world.squareSize*world.mapScale, world.squareSize*world.mapScale))
   #draw the players on the map
   pygame.draw.rect(world.mapOverview, pOne.mapColor, pygame.Rect( world.squareSize*world.mapScale*pOne.x, world.squareSize*pOne.y*world.mapScale, world.squareSize*world.mapScale, world.squareSize*world.mapScale))
   pygame.draw.rect(world.mapOverview, pTwo.mapColor, pygame.Rect( world.squareSize*world.mapScale*pTwo.x, world.squareSize*pTwo.y*world.mapScale, world.squareSize*world.mapScale, world.squareSize*world.mapScale))
   pygame.draw.rect(world.mapOverview, pThree.mapColor, pygame.Rect( world.squareSize*world.mapScale*pThree.x, world.squareSize*pThree.y*world.mapScale, world.squareSize*world.mapScale, world.squareSize*world.mapScale))
   pygame.draw.rect(world.mapOverview, pFour.mapColor, pygame.Rect( world.squareSize*world.mapScale*pFour.x, world.squareSize*pFour.y*world.mapScale, world.squareSize*world.mapScale, world.squareSize*world.mapScale))

   screen.blit(world.mapOverview,world.mapOverviewPosition)

   pygame.display.flip()

#cleanup
pygame.quit()
