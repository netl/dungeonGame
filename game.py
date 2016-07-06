#!/usr/bin/python3
import pygame
from pygame.locals import *
import random
import time

debug = 1
if (debug): print("debug mode on!")

#setup window and graphics
class view:
   width = 800
   height = 600

pygame.init()
screen = pygame.display.set_mode([view.width,view.height])

class world:
   grid = 40 #how many blocks per world vertically/horizontally
   viewGrid = 5 #how many blocks can the player see
   players = 2 #how many players, duh.

   #different settings for different amounts of players
   #1 player
   #player view on the left, map overview at the top right
   if(players==1): 
      playerWindowSize = view.height
      playerWindowPosition = ((0,0),(0,0))
      squareSize = playerWindowSize/viewGrid
      mapScale = (view.width-playerWindowSize)/(squareSize*grid)
      miniMapPosition = (playerWindowSize,0)

   #2 players
   #player 1 on the top right, player 2 on the top left, map overview in bottom center
   elif(players==2): 
      playerWindowSize = view.width/2
      playerWindowPosition = ((view.width-playerWindowSize,0),(0,0))
      squareSize = playerWindowSize/viewGrid
      mapScale = (view.height-playerWindowSize)/(squareSize*grid)
      miniMapPosition = (playerWindowSize-(view.height-playerWindowSize)/2,playerWindowSize)

   #3-4 players
   #player 1: top right, player 2: bottom left, player 3: top left, player 4: bottom right, map overview in center
   else:
      playerWindowSize = view.height/2
      playerWindowPosition = ((view.width-playerWindowSize,0),(0,view.height-playerWindowSize),(0,0),(view.width-playerWindowSize,view.height-playerWindowSize))
      squareSize = playerWindowSize/viewGrid
      mapScale = (view.width-playerWindowSize*2)/(squareSize*grid)
      miniMapPosition = (playerWindowSize,(view.height-mapScale*squareSize*grid)/2)

   #map with the overview of the current level
   miniMap = pygame.Surface((grid*squareSize*mapScale,grid*squareSize*mapScale))

class level:
   def __init__(self, width, height, tileset):
      self.tileset = pygame.image.load("./"+tileset+".png")
      self.tileset = pygame.transform.scale(self.tileset,(int(2*world.squareSize),int(world.squareSize)))
      self.mapTileset = pygame.transform.scale(self.tileset,(int(2*world.squareSize*world.mapScale),int(world.squareSize*world.mapScale)))
      self.map = [[0 for x in range(width)] for y in range(height)]
      self.mobSprite = pygame.image.load("./hostile.png")
      self.mobSprite = pygame.transform.scale(self.mobSprite,(int(world.squareSize),int(world.squareSize)))
  
   #clear the level 
   def clear(self):
      for y in range(len(self.map)):
         for x in range(len(self.map[y])):
            self.map[y][x] = 0
            world.miniMap.fill((0,0,0))
      if (debug): print("level cleared")
      return(0)
   
   #make sure nothing is at position
   def isClear(self, x, y):
      #check for walls
      if(self.map[y][x] == 0):
         return(1)

      #check for players
      for p in range(len(plr)):
         if (plr[p].x == x and plr[p].y == y):
            return(2)

      #check for mobs
      for m in range(len(self.mob)):
         if (self.mob[m].x == x and self.mob[m].y == y):
            return(3)

      #all good!
      return(0)

   #generate tunnels
   def generate(self):
      x = int(world.grid/2)
      y = int(world.grid/2)
      
      #move players to center
      for p in range(len(plr)):
         plr[p].x = x
         plr[p].y = y
      if (debug): print("players moved to origin!")
      
      #start diggin'
      for i in range(world.grid*5):
         self.map[y][x] = 1 
         r = random.randint(0,3)
         stepCount = random.randint(0,5)
         if(r == 0):
            while(y > 0 and l.map[y][x] == 1 and stepCount < 5):
               y = y-1
         elif(r == 1):
            while(y < (world.grid-1) and l.map[y][x] == 1 and stepCount < 5):
               y = y+1
         elif(r == 2):
            while(x > 0 and l.map[y][x] == 1  and stepCount<5):
               x = x-1
         elif(r == 3):
            while(x < (world.grid-1) and l.map[y][x] == 1 and stepCount < 5):
               x = x+1
      if (debug): print("digging finished at: %i,%i" % (x, y))

      #create bad guys
      self.mob = [player() for m in range(5)]
      for m in range(len(self.mob)):
         while( self.isClear(x, y)):
            x = random.randint(0, world.grid-1)
            y = random.randint(0, world.grid-1)
         self.mob[m].x = x
         self.mob[m].y = y
         if (debug): print("mob spawned at: %i,%i" % (self.mob[m].x, self.mob[m].y))
      return(0)

class player:
   def __init__(self):
      self.sprite = pygame.image.load("./player1.png")
      self.sprite = pygame.transform.scale(self.sprite,(int(world.squareSize),int(world.squareSize)))
      self.controls = {'up':K_UP,'down':K_DOWN,'left':K_LEFT,'right':K_RIGHT}
      self.mapColor = (255,255,255)
      self.perspective = pygame.Surface((world.playerWindowSize,world.playerWindowSize))
      self.view = [[0 for x in range(world.viewGrid)] for y in range(world.viewGrid)]
      self.x = 0
      self.y = 0

   #do movement according to given key input
   def readInput(self, keys):
      if keys[self.controls['up']]:
         if (debug): print("player wants to move up")
         return(self.move('up'))
      if keys[self.controls['down']]:
         if (debug): print("player wants to move down")
         return(self.move('down'))
      if keys[self.controls['left']]:
         if (debug): print("player wants to move left")
         return(self.move('left'))
      if keys[self.controls['right']]:
         if (debug): print("player wants to move right")
         return(self.move('right'))
      return(2)
    
   #move, if possible
   def move(self, direction):
      #figure out desired location
      x = self.x
      y = self.y
      if( direction == 'up'):
         y = self.y -1
      elif( direction == 'down'):
         y = self.y +1
      elif( direction == 'left'):
         x = self.x -1
      elif( direction == 'right'):
         x = self.x +1
      #figure out what is at location
      p = l.isClear(x,y)
      if(p == 0): #move if possiblle
         self.y = y
         self.x = x
         return(0)
      elif(p == 3): #attack if move failed
         n = 0
         while True: #find mob at desired location
            if(l.mob[n].x == x and l.mob[n].y == y):
               l.mob[n].x = 1
               l.mob[n].y = 1
               return(0)
            else:
               n = n+1
         return(1) 
      return(1)

   #try to move towards given location
   def moveTowards(self, x, y):
      dx = x-self.x 
      dy = y-self.y 
      if (abs(dx) > abs(dy)):
         if (dx > 0):
            self.move('right')
         else:
            self.move('left')
      else:
         if (dy > 0):
            self.move('down')
         elif (dy < 0):
            self.move('up')

   #refresh viewpoint
   def updateView(self):
      for y in range(world.viewGrid):
         for x in range(world.viewGrid):
            offset=-int((world.viewGrid-1)/2)
            if(x+self.x+offset < world.grid and x+self.x+offset >= 0 and y+self.y+offset < world.grid and y+self.y+offset >= 0):
               self.view[y][x] = l.map[self.y+y+offset][self.x+x+offset]
            else:
               self.view[y][x] = 0

   #render viewpoint
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
         self.perspective.blit(self.sprite, (world.squareSize*(-self.x+plr[p].x)+offset, world.squareSize*(-self.y+plr[p].y)+offset))

      #draw bad mobs
      for m in range(len(l.mob)):
         self.perspective.blit(l.mobSprite, (world.squareSize*(-self.x+l.mob[m].x)+offset, world.squareSize*(-self.y+l.mob[m].y)+offset))
         #pygame.draw.rect(self.perspective, l.mob[m].mapColor, pygame.Rect(world.squareSize*(-self.x+l.mob[m].x)+offset, world.squareSize*(-self.y+l.mob[m].y)+offset, world.squareSize,world.squareSize))

#create level
l = level(world.grid,world.grid,"tileset")

#generate players
plr = [player() for p in range(world.players)]
for p in range(len(plr)):
   plr[p].x = int(world.grid/2)
   plr[p].y = int(world.grid/2)
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
l.generate()
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
            update = update+1
         for p in range(len(plr)):
            update = update+(plr[p].readInput(key) == 0)

   if update:
      if (debug): print("requests for frame update: %i" % (update))
      
      #move mobs
      for m in range(len(l.mob)):
         l.mob[m].moveTowards(plr[0].x,plr[0].y)

      #draw player views
      for p in range(len(plr)):
         if (debug): print("player %i view updated" % (p))
         plr[p].updateView()
         plr[p].drawView()
         screen.blit(plr[p].perspective,world.playerWindowPosition[p])

      #draw the players on the minimap
      for p in range(len(plr)):
         pygame.draw.rect(world.miniMap, plr[p].mapColor, pygame.Rect( world.squareSize*world.mapScale*plr[p].x, world.squareSize*plr[p].y*world.mapScale, world.squareSize*world.mapScale, world.squareSize*world.mapScale))

      #draw minimap
      screen.blit(world.miniMap,world.miniMapPosition)

      pygame.display.flip()
      update = 0 #clar flag for screen refresh
      if (debug): print("frame time: %.5f" % ((time.clock()-framecounter)))

#cleanup
pygame.display.quit()
pygame.quit()
