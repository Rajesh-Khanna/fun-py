import pygame
import random
import cv2
#from aurco import *
from cv2 import aruco
import os
import numpy as np
import math
#constants
WIDTH = 800
HEIGHT = 600

FPS = 30

#define colors
w_ = (255,255,255)
b_ =(0,0,0)
blue_ = (0,0,255)
red_ = (255,0,0)
green_ = (0,255,0)

score1 = 0
score2 = 0

class agr():
	def __init__(self):
	    self.cap = cv2.VideoCapture(0)
	    if self.cap:
	        h = 7
	        w = 6
	        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	        objp = np.zeros((w*h,3), np.float32)
	        objp[:,:2] = np.mgrid[0:h,0:w].T.reshape(-1,2)
	        objpoints = [] # 3d point in real world space
	        imgpoints = [] # 2d points in image plane.
	        k=1
	        count = 1
	        while(count < 11):
	            re, frame = self.cap.read()
	            img = frame
	            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	            ret,gray = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	            # Find the chess board corners
	            ret, corners = cv2.findChessboardCorners(gray, (h,w),None)
	            cv2.imshow('img',gray)
	            # If found, add object points, image points (after refining them)
	            if ret == True:
	                objpoints.append(objp)

	                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
	                imgpoints.append(corners2)

	                # Draw and display the corners
	                img = cv2.drawChessboardCorners(img, (h,w), corners2,ret)
	                cv2.imshow('img',img)
	                count+=1
	            k = cv2.waitKey(5)
	        self.ret, self.mtx, self.dist,self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

	        self.dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)
	        self.parameters =  aruco.DetectorParameters_create()
	        self.board = aruco.GridBoard_create(5, 7, 0.04, 0.01, self.dictionary)
	        img = self.board.draw((600, 500), marginSize = 10,borderBits= 1)
	        cv2.imshow('img',img)
	        cv2.waitKey(0)

	def scaling(self,x,y):
	    x = 0.3*x/600
	    y = 0.4*y/800
	    return [x,y]
	def centre2corners(self,a,b): 
	    return np.float32([a,[b[0],a[1],a[2]],[b[0],b[1],a[2]],[a[0],b[1],a[2]],[a[0],a[1],b[2]],[b[0],a[1],b[2]],b,[a[0],b[1],b[2]]])

	def draw(self,img, cp1,cp2,sp,bdr):
	    
	    cp1 = np.int32(cp1).reshape(-1,2)
	    cp2 = np.int32(cp2).reshape(-1,2)
	    bdr = np.int32(bdr).reshape(-1,2)
	    #sp = np.int32(sp).reshape(-1,2)
	    #print(cp1)
	    #print(cp2)
	    #draw ground floor in green
	    img = cv2.drawContours(img, [cp1[:4]],-1,(0,255,0),-3)
	    # draw pillars in blue color
	    for i,j in zip(range(4),range(4,8)):
	        img = cv2.line(img, tuple(cp1[i]), tuple(cp1[j]),(255),3)
	    
	    #img = cv2.drawContours(img, [bdr[:4]],-1,(0,255,0),-3)
	    
	    for i,j in zip(range(4),range(4,8)):
	        img = cv2.line(img, tuple(bdr[i]), tuple(bdr[j]),(0,255,0),3)
	    # draw top layer in red color
	    img = cv2.drawContours(img, [cp1[4:]],-1,(0,0,255),3)
	    img = cv2.drawContours(img, [bdr[4:]],-1,(0,0,255),3)

	    # draw ground floor in green
	    img = cv2.drawContours(img, [cp2[:4]],-1,(0,255,0),-3)
	    # draw pillars in blue color
	    for i,j in zip(range(4),range(4,8)):
	        img = cv2.line(img, tuple(cp2[i]), tuple(cp2[j]),(255),3)
	    # draw top layer in red color
	    img = cv2.drawContours(img, [cp2[4:]],-1,(0,0,255),3)

	    r = math.ceil((((cp1[0]-cp1[1])**2).sum()+((cp1[0]-cp1[3])**2).sum()+((cp1[0]-cp1[4])**2).sum())**0.5)
	    r = math.ceil(r*0.25)
	    #r = 20
	    cv2.circle(img,(sp[0][0][0],sp[0][0][1]),r,(0,255,255),-1)
	    return img

	def reality(self,cp1,cp2,sp):
		border = np.float32([[0,0,0],[0.3,0,0],[0.3,0.4,0],[0,0.4,0],[0,0,1],[0.3,0,1],[0.3,0.4,1],[0,0.4,1]])
		while True:
			_,frame = self.cap.read()
			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			cv2.imshow('frame',frame)
			corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.dictionary, parameters=self.parameters,cameraMatrix = self.mtx,distCoeff =self.dist)
			cv2.imshow('corners',frame)
			if (len(corners)>0):
				valid, rvecs, tvecs= aruco.estimatePoseBoard(corners, ids, self.board, self.mtx,self.dist)
				if(valid):
					#frame = aruco.drawAxis(frame, self.mtx, self.dist, rvecs, tvecs, 0.1)	
					cp1 , _ = cv2.projectPoints(cp1,rvecs,tvecs,self.mtx,self.dist)
					cp2 , _ = cv2.projectPoints(cp2,rvecs,tvecs,self.mtx,self.dist)
					bdr , _ = cv2.projectPoints(border,rvecs,tvecs,self.mtx,self.dist)
					#sp , _ = cv2.projectPoints(sp,rvecs,tvecs,self.mtx,self.dist)
					img = self.draw(frame,cp1,cp2,sp,bdr)
					cv2.imshow('img',img)
					#return
			cv2.imshow('img2',frame)
			#return
			cv2.waitKey(10)
			
def score(a):
	if(a == 1):
		global score1 
		score1 += 1
	else:
		global score2 
		score2 += 1

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
#ag = agr('http://192.168.1.104:4747/mjpegfeed',6,7,800,600)
ag = agr()

font_name = pygame.font.match_font('arial')

#set up assests
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")

def draw_text(surf , text ,size,x,y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text,True,b_)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface,text_rect)

def deg2rad(a):
	return(a*math.pi/180)


class Player(pygame.sprite.Sprite):
	def __init__(self,k):
		self.k = k
		pygame.sprite.Sprite.__init__(self)
		#every sprite we create should have
		#if u want to put an img then pygame.image.load(path).convert()
		self.image = pygame.Surface((100,18))
		#to neglect the rect color self.image.set_colorkey(black)
		self.image.fill(green_)
		self.rect = self.image.get_rect()
		if(k==0):
			self.rect.bottom = HEIGHT
		else:
			self.rect.top = 0
		self.rect.centerx = (WIDTH/2)
		self.speedx = 0
		
	def update(self):
		self.speedx = 0
		if(self.k == 0):
			keystate = pygame.key.get_pressed()
			if keystate[pygame.K_LEFT]:
				if not self.rect.left <= 5:
					self.speedx = -40
			if keystate[pygame.K_RIGHT]:
				if not self.rect.right >= WIDTH - 5:
					self.speedx = 40
			self.rect.x += self.speedx
		else:	
			keystate = pygame.key.get_pressed()
			if keystate[pygame.	K_a]:
				if not self.rect.left <= 5:
					self.speedx = -40
			if keystate[pygame.K_d]:
				if not self.rect.right >= WIDTH - 5:
					self.speedx = 40
			self.rect.x += self.speedx

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((20,20))
		pygame.draw.circle(self.image, blue_,(10,10	),10 , 0)
		self.image.set_colorkey(b_)
		self.rect = self.image.get_rect()
		self.Start()
		
	def refx(self):
		self.speedy = -self.speedy


	def update(self):
		if(self.rect.bottom >= HEIGHT ):
			score(1)
			self.Start()
		if(self.rect.top <= 0):
			score(2)
			self.Start()
		if(self.rect.right >= WIDTH or self.rect.left<=0):
			self.speedx = -self.speedx
		self.rect.x += self.speedx
		self.rect.y += self.speedy

	def Start(self):
		a = [1,-1]
		self.rect.center = (WIDTH/2,HEIGHT/2)
		if random.randrange(2,6)%2 :
			self.angle = random.randrange(45,80)*a[random.randrange(2,6)%2]
		else:
			self.angle = random.randrange(100,135)*a[random.randrange(2,6)%2]
		self.speedy = 5*math.sin(deg2rad(self.angle))
		self.speedx = 5*math.cos(deg2rad(self.angle))

	def over(self):
		pass



player = Player(0)
pc = Player(1)
ball = Ball()

all_sprites = pygame.sprite.Group()
game_players = pygame.sprite.Group()
all_sprites.add(player,pc,ball)
game_players.add(player,pc)

border = np.float32([[0,0,0],[0.4,0,0],[0.4,0.3,0],[0,0.3,0],[0,0,0.05],[0.4,0,0.05],[0.4,0.3,0.05],[0,0.3,0.05]])

RUNING = True
while(RUNING):
	#pause till it reaches fps
	#clock.tick(1)
	#Processed input

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			RUNING = False
	#update
	all_sprites.update()
	cp1 = ag.centre2corners(ag.scaling(player.rect.x,player.rect.y)+[0],ag.scaling(player.rect.bottomright[0],player.rect.bottomright[1])+[0.05])
	cp2 = ag.centre2corners(ag.scaling(pc.rect.x,pc.rect.y)+[0],ag.scaling(pc.rect.bottomright[0],pc.rect.bottomright[1])+[0.05])
	sp = np.float32([ag.scaling(ball.rect.centerx,ball.rect.centery)+[0.05]])
	print(len(sp[0]))
	print(sp.shape)

	#ag.reality(c1pts,c2pts,spts)
	re,frame = ag.cap.read()
	if re:
			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			#cv2.imshow('frame',frame)
			corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, ag.dictionary, parameters=ag.parameters,cameraMatrix = ag.mtx,distCoeff = ag.dist)
			#cv2.imshow('corners',frame)
			if (len(corners)>0):
				valid, rvecs, tvecs= aruco.estimatePoseBoard(corners, ids, ag.board, ag.mtx,ag.dist)
				if(valid > 0):
					#frame = aruco.drawAxis(frame, self.mtx, self.dist, rvecs, tvecs, 0.1)	
					bdr , _ = cv2.projectPoints(border,rvecs,tvecs,ag.mtx,ag.dist)
					cp1 , _ = cv2.projectPoints(cp1,rvecs,tvecs,ag.mtx,ag.dist)
					cp2 , _ = cv2.projectPoints(cp2,rvecs,tvecs,ag.mtx,ag.dist)
					sp , _ = cv2.projectPoints(sp,rvecs,tvecs,ag.mtx,ag.dist)
					print(sp)
					img = cv2.flip(ag.draw(frame,cp1,cp2,sp,bdr),1)
					cv2.imshow('img',img)
					#return
			cv2.imshow('img2',frame)
			#return
	cv2.waitKey(10)
			
	#p = Process(target=ag.reality, args=(c1pts,c2pts,spts))
	#p.start()
	#p.join() # this blocks until the process terminates

	#_ = run_in_separate_process(ag.reality ,c1pts,c2pts,spts)
	#collision check
	hits = pygame.sprite.spritecollide(ball,game_players,False)
	if hits:
		ball.refx()
		pass

	#draw
	screen.fill(w_)
	all_sprites.draw(screen)
	draw_text(screen,str(score1)+' | '+str(score2),18,WIDTH/2,10)
	pygame.display.flip()

pygame.quit()	