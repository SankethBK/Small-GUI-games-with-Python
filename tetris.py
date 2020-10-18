# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:32:50 2019

@author: LENOVO
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 16 20:05:00 2019

@author: LENOVO
"""

#import all modules here
import pygame
from pygame.locals import *
from color import *
import random
import sys
import time

pygame.init()
win = pygame.display.set_mode((500,500))
fpsClock = pygame.time.Clock()
#pygame.mixer.music.load("AlanWalker4.mp3")
#pygame.mixer.music.play()

font1 = pygame.font.SysFont('comicsans',30,1,1)
font2 = pygame.font.SysFont('comicsans',50,1,1)
#define all variables here

shapes = [
          [[0,1,0],
          [1,1,1]],
           
          [[0,1,1],
           [1,1,0]],
           
          [[1,1,0],
           [0,1,1]],

          [[1,1],
           [1,1]],
          
           [[1,0,0,0],
            [1,1,1,1]],
            
            [[0,0,0,1],
             [1,1,1,1]],
             
             [[1,1,1,1]]
             
            ]
        
bn = 12  #no of blocks in a row
bs = 20  #size of each box       
px = 100 #start x coordinate
px2 = px + bn * bs #end coordinate of play zone

kernels={}
mycolorList = colorList
try:
    mycolorList.remove(BLACK)
except:
    pass
fps = 7
score = 0
text1 = font1.render("Score="+str(score),True,CYAN)
text2 = font1.render("You Lost",True,FUCHSIA)
text3 = font1.render("Next Block",True,FUCHSIA)
lock = 0

#define all functione here

def rotate(block):
    s=[]
    k=[]
    for i in range(len(block[0])):
        k=[]
        for j in range(len(block)):
            k.append(block[len(block)-1-j][i])
        s.append(k)
    return s

def getRandomBlock():
    return random.choice(shapes)

def objectCreator(shape):
    sy = -40
    sx = (px + px2)/2
    cL = []
    for i in shape:
        sx = (px + px2)/2
        for j in i:
            if j!=0:
                cL.append([sx ,sy])
            sx+=bs
        sy+=bs
    return Block(random.choice(mycolorList),cL,shape)

def setKernelsZero():
    c=1
    for i in range(px,px2 ,bs):
        kernels[i,500] = 1   
        for j in range(-60,500,bs):
            kernels[(i,j)] = 0
            if c:
                kernels[(px-bs,j)] = 1
                kernels[(px2,j)] = 1
        c=0
    

def reDrawWindow():
    win.fill(BLACK)
    win.blit(text1,(px2+10,50))
    win.blit(text3,(px2+10,200))
    pygame.draw.line(win,CYAN,(px,0),(px,500),5)
    pygame.draw.line(win,CYAN,(px2,0),(px2,500),5)
    nextBlockDisplayer()
    restBlocksDraw()
    myBlock.draw()
    pygame.display.update()
    
def collisionCheck(myBlock,dr):

    if dr == 'l':
        vx = -bs
    elif dr == 'r':
        vx = bs
    for i in myBlock.bL:
        if (i[1]<-20):
            return myBlock.move(dr)
        if kernels[i[0] + vx,i[1]] != 0:
            return 
    return myBlock.move(dr)

def downCollisionCheck(myBlock,d=0):
    global a
    for i in myBlock.bL:

        
        if kernels[i[0],i[1]+bs] != 0 :
            if not myBlock.land:
                myBlock.land = True
                a = time.time()
            return 
        if d==1:
           if kernels[i[0],i[1]+2*bs] != 0 :
               if  kernels[i[0],i[1]+bs] == 0:
                   d=0
                   continue
               
               if not myBlock.land :
                   myBlock.land = True
                   a=time.time()
               return 
    myBlock.land = False
    if d == 1:
      return  myBlock.move('dd')  
    return myBlock.move('d')


def restBlocksDraw():
    for i in kernels:
        if kernels[i] != 0 and kernels[i] != 1:
            pygame.draw.rect(win,kernels[i],(i[0],i[1],bs,bs))
            pygame.draw.rect(win,BLACK,(i[0],i[1],bs,bs),3)
            
def objRotator(myBlock):

    rotBlock = rotate(myBlock.shape)
    sx = myBlock.bL[0][0]
    sy = myBlock.bL[0][1]
    newbL = []
    for i in rotBlock:
      sx = myBlock.bL[0][0]
      for j in i:
          if j != 0:
              newbL.append([sx,sy])
          sx +=bs
      sy += bs
    if rotGuider(newbL)!=False:
        newbl = rotGuider(newbL)
    else:
        return myBlock
    b = Block(myBlock.color,newbL,rotBlock)
    if myBlock.land == True:
        b.land = True
    return b
def rotGuider(blockList):
    flag = True
    offset = 1
    
    for i in blockList:
        if i[1] < 0:
            return blockList
        if kernels[i[0],i[1]] != 0:
            flag = False
            break
    if flag == True:
        return blockList
    while offset<3:
        if leftChecker(blockList,offset*bs):
            blockList = mover(blockList,-offset*bs)
            return blockList
        elif rightChecker(blockList,offset*bs):
            blockList = mover(blockList,offset*bs)
            return blockList
        offset+=1
    return False
def leftChecker(blockList,s):
    for i in blockList:
        if i[0]-s < px:
            return False
        if kernels[i[0]-s,i[1]] != 0:
            return False
    return True
def rightChecker(blockList,s):
    for i in blockList:
        if i[0] + s > px2:
           return False
        if kernels[i[0]+s,i[1]] != 0:
            return False
    return True
def mover(blockList,s):
    for i in range(len(blockList)):
        blockList[i][0]+=s
        
def rowClearCheck():
    global score
    fc = 0
    for i in range(0,500,bs):
        fc = 0
        for j in range(px,px2,bs):
            if kernels[j,i] == 0:
                fc = 0
                continue
            else:
                fc+=1
        if fc == bn:
            score+=10
            return rowclear(i)
    return False
def rowclear(n):
    for i in range(px,px2,bs):
        kernels[i,n]=0
    moveWhenCleared(n)

def moveWhenCleared(n):
    nc = 0
    for i in range(n-bs,0,-bs):
        nc = 0
        for j in range(px,px2,bs):
             kernels[j,i + bs]= kernels[j,i]
             if kernels[j,i]==0:
                 nc += 1
        if nc == bn:
            return

def endChecker():
    for i in range(px,px2,bs):
        if kernels[i,0]!=0:
            win.blit(text2,(250,250))
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            sys.exit()
            

def nextBlock():
    global tempBlock
    tempBlock =  objectCreator(getRandomBlock())         
    
def nextBlockDisplayer():
    sx = px2+20
    sy = 250
    for i in tempBlock.shape:
        sx = px2 + 20
        for j in i:
            if j!=0:
                pygame.draw.rect(win,tempBlock.color,(sx,sy,bs,bs))
                pygame.draw.rect(win,BLACK,(sx,sy,bs,bs),3)
            sx+=bs
        sy+=bs
#define all Boolean flags here
run = True

#define all classes here

class Block:
    
    def __init__(self,color,blockList,shape):
        self.color = color
        self.bL = blockList
        self.land = False
        self.go = True
        self.shape = shape
        
    def draw(self):
        for i in self.bL:
            pygame.draw.rect(win,self.color,(i[0],i[1],bs,bs))
            pygame.draw.rect(win,BLACK,(i[0],i[1],bs,bs),3)
    def move(self,dr):
        if dr =='l':
            for i in range(len(self.bL)):
                self.bL[i][0]-=bs
        elif dr =='r':
            for i in range(len(self.bL)):
                self.bL[i][0]+=bs   
        elif dr == 'd':
            for i in range(len(self.bL)):
                self.bL[i][1]+=bs
        elif dr == 'dd':

            for i in range(len(self.bL)):
                self.bL[i][1]+=2*bs       
    
    


#makefunction calls here
setKernelsZero()
myBlock = objectCreator(getRandomBlock())
nextBlock()
#mainloop
while run:
   # print(myBlock.bL)
    text1 = font1.render("Score="+str(score),True,CYAN)
    if myBlock.land:
        if time.time() - a > 0.5:
            myBlock.go = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    rowClearCheck()
    if lock>0:
        lock-=1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and myBlock.go and not lock:
        myBlock = objRotator(myBlock)
        lock = 5
    if keys[pygame.K_LEFT] and myBlock.go:
        collisionCheck(myBlock,'l')
    if keys[pygame.K_RIGHT] and myBlock.go:
        collisionCheck(myBlock,'r')
    if keys[pygame.K_DOWN] and myBlock.go:
        downCollisionCheck(myBlock,1)

    elif myBlock.go:
        downCollisionCheck(myBlock)
        
    if myBlock.go == False :
        for i in myBlock.bL:
            kernels[i[0],i[1]] = myBlock.color
        myBlock = tempBlock  
        nextBlock()
  
#    for i in kernels:
#        pygame.draw.rect(win,YELLOW,(i[0],i[1],20,20))
    fpsClock.tick(fps)
    reDrawWindow()
    endChecker()
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

#define all classes here