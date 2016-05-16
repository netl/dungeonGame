#!/usr/bin/python3
import pygame
from pygame.locals import *
import random

#setup window and graphics
class view:
   width = 800
   height = 600
pygame.init()
screen = pygame.display.set_mode([view.width,view.height])

class world:
   squareSize = 60
   grid = 40
   mapScale = 1/10
   players = 1
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
   controls = {'up':K_k,'down':K_j,'left':K_h,'right':K_l}
   mapColor = (255,255,255)
   perspective = pygame.Surface((view.width/2,view.height/2))

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
      #draw the grid
      for y in range(len(l.map)):
         for x in range(len(l.map[y])):
            pygame.draw.rect(self.perspective, l.color[l.map[y][x]], pygame.Rect(world.squareSize*(-self.x+x)+view.width/4,world.squareSize*(-self.y+y)+view.height/4,world.squareSize,world.squareSize))
      #draw the player
      pygame.draw.rect(self.perspective, self.mapColor, pygame.Rect(view.width/4,view.height/4,world.squareSize,world.squareSize))

#create level
l = level(world.grid,world.grid)

#generate players
pOne = player(int(world.grid/2),int(world.grid/2))
pOne.mapColor = (255,0,0)

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

   pOne.drawView()

   #draw the map
   for y in range(len(l.map)):
      for x in range(len(l.map[y])):
         pygame.draw.rect(world.mapOverview, l.color[l.map[y][x]], pygame.Rect( world.squareSize*x*world.mapScale, world.squareSize*y*world.mapScale, world.squareSize*world.mapScale, world.squareSize*world.mapScale))
   #draw the players on the map
   pygame.draw.rect(world.mapOverview, pOne.mapColor, pygame.Rect( world.squareSize*world.mapScale*pOne.x, world.squareSize*pOne.y*world.mapScale, world.squareSize*world.mapScale, world.squareSize*world.mapScale))

   screen.blit(pOne.perspective,(0,0))
   screen.blit(world.mapOverview,(view.width/2-world.mapOverview.get_width()/2,view.height/2-world.mapOverview.get_height()/2))

   pygame.display.flip()

#cleanup
pygame.quit()
