#!/usr/bin/python3
import pygame
from pygame.locals import *
import random
import time

#setup window and graphics
class view:
   width = 800
   height = 600
pygame.init()
screen = pygame.display.set_mode([view.width,view.height])

class world:
   grid = 40 #how many blocks per world vertically/horizontally
   viewGrid = 5 #how many blocks can the player see
   players = 4 #how many players, duh.

   #different settings for different amounts of players
   if(players==1): #player view on the left, map overview at the top right
      playerWindowSize = view.height
      playerWindowPosition = ((0,0),(0,0))
      squareSize = playerWindowSize/viewGrid
      mapScale = (view.width-playerWindowSize)/(squareSize*grid)
      miniMapPosition = (playerWindowSize,0)

   elif(players==2): #player 1 on the top right, player 2 on the top left, map overview in bottom center
      playerWindowSize = view.width/2
      playerWindowPosition = ((view.width-playerWindowSize,0),(0,0))
      squareSize = playerWindowSize/viewGrid
      mapScale = (view.height-playerWindowSize)/(squareSize*grid)
      miniMapPosition = (playerWindowSize-(view.height-playerWindowSize)/2,playerWindowSize)

   else: #player 1: top right, player 2: bottom left, player 3: top left, player 4: bottom right, map overview in center
      playerWindowSize = view.height/2
      playerWindowPosition = ((view.width-playerWindowSize,0),(0,view.height-playerWindowSize),(0,0),(view.width-playerWindowSize,view.height-playerWindowSize))
      squareSize = playerWindowSize/viewGrid
      mapScale = (view.width-playerWindowSize*2)/(squareSize*grid)
      miniMapPosition = (playerWindowSize,(view.height-mapScale*squareSize*grid)/2)

   miniMap = pygame.Surface((grid*squareSize*mapScale,grid*squareSize*mapScale)) #minimap

class level:
   color = ((255,128,0),(0,0,0))
   def __init__(self, width, height, tileset):
      self.tileset = pygame.image.load("./"+tileset+".png")
      self.tileset = pygame.transform.scale(self.tileset,(int(2*world.squareSize),int(world.squareSize)))
      self.mapTileset = pygame.transform.scale(self.tileset,(int(2*world.squareSize*world.mapScale),int(world.squareSize*world.mapScale)))
      self.map = [[0 for x in range(width)] for y in range(height)]
  
   #clear the level 
   def clear(self):
      for y in range(len(self.map)):
         for x in range(len(self.map[y])):
            self.map[y][x] = 0
            world.miniMap.fill((0,0,0))
      return(0)
   
   #generate tunnels
   def generate(self):
      miner = player(int(world.grid/2),int(world.grid/2))
      for p in range(len(plr)):
         plr[p].x = miner.x
         plr[p].y = miner.y
      for i in range(world.grid*5):
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
   def __init__(self,x,y):
      self.controls = {'up':K_UP,'down':K_DOWN,'left':K_LEFT,'right':K_RIGHT}
      self.mapColor = (255,255,255)
      self.perspective = pygame.Surface((world.playerWindowSize,world.playerWindowSize))
      self.view = [[0 for x in range(world.viewGrid)] for y in range(world.viewGrid)]
      self.x = x
      self.y = y

   def readInput(self, keys): #do movement according to given key input
      if key[self.controls['up']]:
         self.move('up')
         if(self.underneath() == 0):
            self.move('down')
         return(0)
      if key[self.controls['down']]:
         self.move('down')
         if(self.underneath() == 0):
            self.move('up')
         return(0)
      if key[self.controls['left']]:
         self.move('left')
         if(self.underneath() == 0):
            self.move('right')
         return(0)
      if key[self.controls['right']]:
         self.move('right')
         if(self.underneath() == 0):
            self.move('left')
         return(0)
      return(1)
      
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

   def updateView(self):
      for y in range(world.viewGrid):
         for x in range(world.viewGrid):
            offset=-int((world.viewGrid-1)/2)
            if(x+self.x+offset < world.grid and x+self.x+offset >= 0 and y+self.y+offset < world.grid and y+self.y+offset >= 0):
               self.view[y][x] = l.map[self.y+y+offset][self.x+x+offset]
            else:
               self.view[y][x] = 0
      

   def underneath(self):
      return(l.map[self.y][self.x])

   def drawView(self):
      offset=self.perspective.get_width()/2-world.squareSize/2
      #draw the grid
      for y in range(world.viewGrid):
         for x in range(world.viewGrid):
            #update player view
            self.perspective.blit(l.tileset, (world.squareSize*x,world.squareSize*y), pygame.Rect((self.view[y][x]*world.squareSize,0), (world.squareSize,world.squareSize)))
            #update minimap
            world.miniMap.blit(l.mapTileset, (world.squareSize*world.mapScale*(x+self.x-(world.viewGrid-1)/2), world.squareSize*world.mapScale*(y+self.y-(world.viewGrid-1)/2)), pygame.Rect((self.view[y][x]*world.squareSize*world.mapScale,0), (world.squareSize*world.mapScale,world.squareSize*world.mapScale)))
            
      #draw the players
      for p in range(len(plr)):
         pygame.draw.rect(self.perspective, plr[p].mapColor, pygame.Rect(world.squareSize*(-self.x+plr[p].x)+offset, world.squareSize*(-self.y+plr[p].y)+offset, world.squareSize,world.squareSize))

#create level
l = level(world.grid,world.grid,"tileset")

#generate players
plr = [player(int(world.grid/2),int(world.grid/2)) for p in range(world.players)]
plr[0].mapColor = (255,0,0)
if( world.players > 1):
   plr[1].controls = {'up':K_w,'down':K_s,'left':K_a,'right':K_d}
   plr[1].mapColor = (0,255,0)
if( world.players > 2):
   plr[2].controls = {'up':K_i,'down':K_k,'left':K_j,'right':K_l}
   plr[2].mapColor = (0,0,255)
if( world.players > 3):
   plr[3].controls = {'up':K_KP8,'down':K_KP2,'left':K_KP4,'right':K_KP6}
   plr[3].mapColor = (255,255,0)

#game variables
random.seed()
playing = 1
update = 1 #flag for updating screen

#main loop
while(playing):
   framecounter = time.clock()

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         playing = 0
      elif event.type == pygame.KEYDOWN:
         key = pygame.key.get_pressed()
         if key[K_SPACE]:
            l.clear()
            l.generate()
         for p in range(len(plr)):
            update = update+plr[p].readInput(key)

   if update:
      for p in range(len(plr)):
         plr[p].updateView()
         plr[p].drawView()
         screen.blit(plr[p].perspective,world.playerWindowPosition[p])

      #draw the players on the map
      for p in range(len(plr)):
         pygame.draw.rect(world.miniMap, plr[p].mapColor, pygame.Rect( world.squareSize*world.mapScale*plr[p].x, world.squareSize*plr[p].y*world.mapScale, world.squareSize*world.mapScale, world.squareSize*world.mapScale))

      screen.blit(world.miniMap,world.miniMapPosition)

      pygame.display.flip()
      update = 0 #clar flag for screen refresh
   print("fps: %.f" % (1/(time.clock()-framecounter)))

#cleanup
pygame.display.quit()
pygame.quit()
