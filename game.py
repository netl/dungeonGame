#!/usr/bin/python3
import pygame
from pygame.locals import *
import sys
import random

class level:
   def __init__(self, width, height):
      self.map=[[0 for x in range(width)] for y in range(height)]
  
   #clear the level 
   def clear(self):
      for y in range(len(self.map)):
         for x in range(len(self.map[y])):
            self.map[y][x]=0
      return(0)
   
   #generate tunnels
   def generate(self):
      miner = player(int(grid/2),int(grid/2))
      pOne.x = miner.x
      pOne.y = miner.y
      for i in range(200):
         self.map[miner.y][miner.x]=1 
         r = random.randint(0,3)
         stepCount=random.randint(0,5)
         if(r == 0):
            while(miner.move("up") and miner.underneath() == 1 and stepCount<5):
               pass
         elif(r == 1):
            while(miner.move("down") and miner.underneath() == 1 and stepCount<5):
               pass
         elif(r == 2):
            while(miner.move("left") and miner.underneath() == 1 and stepCount<5):
               pass
         elif(r == 3):
            while(miner.move("right") and miner.underneath() == 1 and stepCount<5):
               pass
      return(0)


class player:
   def __init__(self,x,y):
      self.x=x
      self.y=y
   def move(self, direction):
      if(direction== "up" and self.y>0):
         self.y = self.y - 1
         return(1)
      elif(direction== "down" and self.y<len(l.map)-1):
         self.y = self.y + 1
         return(1)
      if(direction== "left" and self.x>0):
         self.x = self.x - 1
         return(1)
      elif(direction== "right" and self.x<len(l.map[self.y])-1):
         self.x = self.x + 1
         return(1)
      else:
         return(0)
   def underneath(self):
      return(l.map[self.y][self.x])

#setup window and graphics
squareSize = 20
grid=40
screenWidth = squareSize*grid
screenHeight = squareSize*grid 
color = ((255,255,255),(0,255,0),(0,0,255))
pygame.init()
screen = pygame.display.set_mode([screenWidth,screenHeight])


#create level
l = level(grid,grid)

#game variables
random.seed()
playing = 1

pOne = player(int(grid/2),int(grid/2))

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
         elif key[K_k]:
            pOne.move("up")
            if(pOne.underneath()==0):
               pOne.move("down")
         elif key[K_j]:
            pOne.move("down")
            if(pOne.underneath()==0):
               pOne.move("up")
         elif key[K_h]:
            pOne.move("left")
            if(pOne.underneath()==0):
               pOne.move("right")
         elif key[K_l]:
            pOne.move("right")
            if(pOne.underneath()==0):
               pOne.move("left")
   

   #draw the grid
   for y in range(len(l.map)):
      for x in range(len(l.map[y])):
         pygame.draw.rect(screen, color[l.map[y][x]], pygame.Rect(squareSize*x,squareSize*y,squareSize,squareSize))
   
   pygame.draw.rect(screen, color[2], pygame.Rect(squareSize*pOne.x,squareSize*pOne.y,squareSize,squareSize))

   pygame.display.flip()

#cleanup
pygame.quit()
