# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 10:25:22 2019

@author: LENOVO
"""

#importing the modules
import pygame ,sys, random ,time
from pygame.locals import *
from color import *

#initializing the pygame window
pygame.init()
win=pygame.display.set_mode((500,500))
pygame.display.set_caption('')

#define all pygame related objects here
bg=pygame.transform.scale(pygame.image.load('nature.jpg'),(1000,500))
Clock=pygame.time.Clock()
pygame.time.set_timer(USEREVENT+1,3000)
#pygame.mixer.music.load('Taylor_Swift_Delicate.mp3')
#pygame.mixer.music.play(-1,0.0)


#defeine all pygame related variables herevariables 
bgX=0
bgX2=1000
fps=10
pipes=[]
pipeGap=100
score=0
#a=pygame.transform.scale(pygame.image.load('greenorg.png'),(50,200))
#b=pygame.transform.scale(pygame.image.load('greenorgdown.jpg'),(50,200))
        


#define all classes here
class birds:
    fly=[pygame.transform.scale(pygame.image.load('bird0.png'),(30,30)),pygame.transform.scale(pygame.image.load('bird1.png'),(30,30)),pygame.transform.scale(pygame.image.load('bird2.png'),(30,30)),pygame.transform.scale(pygame.image.load('bird3.png'),(30,30))]
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=50
        self.height=50
        self.flying=False
        self.falling=True
        self.flyCount=0
        self.vel=8
        self.hitbox=(self.x,self.y,self.width-20,self.height-20)
    
    def draw(self):
        if self.flyCount>14:
            self.flyCount=0
        if self.flying:
            self.y-=self.vel
            self.flyCount+=1
            self.hitbox=(self.x,self.y,self.width-20,self.height-20)
            win.blit(self.fly[self.flyCount//4],(self.x,self.y))
           # pygame.draw.rect(win,RED,self.hitbox,2)
            self.flying=False
        elif self.falling:
            self.y+=self.vel
            win.blit(self.fly[0],(self.x,self.y))
            self.hitbox=(self.x,self.y,self.width-20,self.height-20)
           # pygame.draw.rect(win,RED,self.hitbox,2)
        
    
            
    
class pipe:   
        downPipe=pygame.transform.scale(pygame.image.load('greenorg.png'),(50,100))
        upPipe=pygame.transform.scale(pygame.image.load('greenorgdown.jpg'),(50,100))
        
        def __init__(self,x,y,width,height):
            self.x=x
            self.y=y
            self.width=width
            self.height=height
            self.hitbox=(self.x,self.y,self.width,self.height)
        def draw(self,num):
            if num==0:
                win.blit(pygame.transform.scale(self.downPipe,(self.width,self.height)),(self.x,self.y))
                pygame.draw.rect(win,RED,self.hitbox,2)
            if num==1:
                win.blit(pygame.transform.scale(self.upPipe,(self.width,self.height)),(self.x,self.y))
                pygame.draw.rect(win,RED,self.hitbox,2)
            scoreDisplayer()
        def collide(self,rect,num):
            global score ,run
            scoreCount=0
            if (rect[0]+rect[2]>self.hitbox[0] and rect[0]+rect[2]<self.hitbox[0]+self.hitbox[2]) or (rect[0]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]):
                if num==0:
                    if rect[1]<self.hitbox[1]+self.hitbox[3]:
                        print('hitup')
                        run=False
                elif num==1:
                    if rect[1]+30>self.hitbox[1]:
                          print('hitdown')
                          run=False
                if scoreCount==0:
                    score+=1
                        
      
                

bird=birds(100,200)
#define all boolean flags here
run=True
run1=True
#define all functions here
def reDrawWindow():
    win.blit(bg,(bgX,0))
    win.blit(bg,(bgX2,0))
   # win.blit(a,(200,0))
   # win.blit(b,(200,300))
    for pipo in pipes:
        pipo[0].draw(0)
        pipo[0].collide(bird.hitbox,0)
        pipo[1].draw(1)
        pipo[1].collide(bird.hitbox,1)
    bird.draw()
    
    pygame.display.update()
def scoreDisplayer():
    font1=pygame.font.SysFont('comicsans',30,0,True)
    text1=font1.render('score='+str(score//18),True,BLUE)
    win.blit(text1,((400,10)))
#mainloop
while run:
    for pip in pipes:
        pip[0].x-=5
        pip[0].hitbox=(pip[0].x,pip[0].y,pip[0].width,pip[0].height)
        pip[1].x-=5
        pip[1].hitbox=(pip[1].x,pip[1].y,pip[1].width,pip[1].height)
    for event in pygame.event.get():
        if event.type==QUIT:
            run=False
        if event.type==USEREVENT+1:
            randomHeight=random.randrange(50,200)
            pipes.append((pipe(510,0,50,randomHeight),pipe(510,randomHeight+pipeGap,50,500-randomHeight-pipeGap)))
    bgX-=5
    bgX2-=5
    
    if bgX==bg.get_width()*-1:
        bgX=bg.get_width()
    if bgX2==bg.get_width()*-1:
        bgX2=bg.get_width()
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_c]:
        bird.flying=True
    
    reDrawWindow()
    Clock.tick(fps)


#to display the bird's fall
while run1:
    pygame.time.delay(100)
    if bird.y>500:
        run1=False
    bird.y+=bird.vel
    reDrawWindow()
time.sleep(3)
pygame.quit()
sys.exit()




