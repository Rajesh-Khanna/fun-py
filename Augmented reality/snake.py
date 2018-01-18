import pygame
import numpy as np
import cv2
from cv2 import aruco
import random
import os
from time import sleep
import math

WIDTH = 600
HEIGHT = 600
snake_side = 20

FPS = 2

#define colors
w_ = (255,255,255)
b_ =(0,0,0)
blue_ = (0,0,255)
red_ = (255,0,0)
green_ = (0,255,0)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

points = {(snake_side//2,snake_side//2),}
for i in range(1,WIDTH//snake_side-1):
	for j in range(1,HEIGHT//snake_side-1):
		points.add((snake_side*i+snake_side//2,snake_side*j+snake_side//2))


body_points = set()
#set up assests
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")

#---------------------------------------------ag----------------------------------------

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
	            k = cv2.waitKey(0)
	        self.ret, self.mtx, self.dist,self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

	        self.dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)
	        self.parameters =  aruco.DetectorParameters_create()
	        self.board = aruco.GridBoard_create(5, 7, 0.04, 0.01, self.dictionary)
	        img = self.board.draw((600, 500), marginSize = 10,borderBits= 1)
	        cv2.imshow('img',img)
	        cv2.waitKey(5)

	def scaling(self,x,y):
	    x = 0.3*x/600
	    y = 0.3*y/600
	    return [x,y]
	def centre2corners(self,a,b): 
	    return np.float32([a,[b[0],a[1],a[2]],[b[0],b[1],a[2]],[a[0],b[1],a[2]],[a[0],a[1],b[2]],[b[0],a[1],b[2]],b,[a[0],b[1],b[2]]])

	def draw(self,img, cp,fo,bdr):
	    for i in range(len(cp)):
	    	cp[i] = np.int32(cp[i]).reshape(-1,2)
	    fo = np.int32(fo).reshape(-1,2)
	    bdr = np.int32(bdr).reshape(-1,2)
	    #sp = np.int32(sp).reshape(-1,2)
	    #print(cp1)
	    #print(cp2)
	    #draw ground floor in green
	    for cp1 in cp:
	    	img = cv2.drawContours(img, [cp1[:4]],-1,(0,255,0),-3)
	    	# draw pillars in blue color
	    	for i,j in zip(range(4),range(4,8)):
	        	#img = cv2.line(img, tuple(cp1[i]), tuple(cp1[j]),(255),3)
		    	img = cv2.drawContours(img, np.array([[cp1[0],cp1[1],cp1[5],cp1[4]]]),-1,(255,0,255),-3)
		    	img = cv2.drawContours(img, np.array([[cp1[1],cp1[2],cp1[6],cp1[5]]]),-1,(255,0,255),-3)
		    	img = cv2.drawContours(img, np.array([[cp1[2],cp1[3],cp1[7],cp1[6]]]),-1,(255,0,255),-3)
		    	img = cv2.drawContours(img, np.array([[cp1[3],cp1[0],cp1[4],cp1[7]]]),-1,(255,0,255),-3)
	    	img = cv2.drawContours(img, [cp1[4:]],-1,(0,0,255),-3)
		    
	    #img = cv2.drawContours(img, [bdr[:4]],-1,(0,255,0),-3)
	    '''
	    for i,j in zip(range(4),range(4,8)):
	        img = cv2.line(img, tuple(bdr[i]), tuple(bdr[j]),(0,255,0),3)
	    # draw top layer in red color
	    img = cv2.drawContours(img, [bdr[4:]],-1,(0,0,255),3)
	    '''
	    # draw ground floor in green
	    img = cv2.drawContours(img, [fo[:4]],-1,(0,255,0),-3)
	    # draw pillars in blue color
	    for i,j in zip(range(4),range(4,8)):
		    	img = cv2.drawContours(img, np.array([[fo[0],fo[1],fo[5],fo[4]]]),-1,(255,0,0),-3)
		    	img = cv2.drawContours(img, np.array([[fo[1],fo[2],fo[6],fo[5]]]),-1,(255,0,0),-3)
		    	img = cv2.drawContours(img, np.array([[fo[2],fo[3],fo[7],fo[6]]]),-1,(255,0,0),-3)
		    	img = cv2.drawContours(img, np.array([[fo[3],fo[0],fo[4],fo[7]]]),-1,(255,0,0),-3)
	    # draw top layer in red color
	    img = cv2.drawContours(img, [fo[4:]],-1,(0,0,255),3)
	    return img

	def reality(self,cp,cp2,sp):
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

#---------------------------------------------------------------------------------------

class Body(pygame.sprite.Sprite):
	def __init__(self,k,h,w):
		self.k = k
		pygame.sprite.Sprite.__init__(self)
		#every sprite we create should have
		#if u want to put an img then pygame.image.load(path).convert()
		self.image = pygame.Surface((snake_side,snake_side))
		#to neglect the rect color self.image.set_colorkey(black)
		if k%2==0:
			self.image.fill((0,255,255))
		else:	
			self.image.fill((255,0,255))
		self.rect = self.image.get_rect()
		self.rect.centery = h
		self.rect.centerx = w
		#points - {(self.rect.centerx,self.rect.centery),}

	def Update(self,a,b):
		self.rect.x = a
		self.rect.y = b
		
	def update(self):
		pass

class Player(pygame.sprite.Sprite):
	def __init__(self,k):
		global body_points
		self.k = k
		pygame.sprite.Sprite.__init__(self)
		#every sprite we create should have
		#if u want to put an img then pygame.image.load(path).convert()
		self.image = pygame.Surface((snake_side,snake_side))
		#to neglect the rect color self.image.set_colorkey(black)
		self.image.fill(green_)
		self.rect = self.image.get_rect()
		self.rect.centery = HEIGHT/2-snake_side/2
		self.rect.centerx = (WIDTH/2-snake_side/2)
		self.speedx = snake_side
		self.speedy = 0
		self.tempx = snake_side
		self.tempy = 0
		self.body = []
		self.body.append(self)
		body_points.add((WIDTH/2-0*snake_side-snake_side,HEIGHT/2-snake_side/2))
		body_points.add((WIDTH/2-1*snake_side-snake_side,HEIGHT/2-snake_side/2))
		body_points.add((WIDTH/2-2*snake_side-snake_side,HEIGHT/2-snake_side/2))
		body_points.add((WIDTH/2-3*snake_side-snake_side,HEIGHT/2-snake_side/2))
		body_points.add((WIDTH/2-4*snake_side-snake_side,HEIGHT/2-snake_side/2))
		body_points.add((WIDTH/2-5*snake_side-snake_side,HEIGHT/2-snake_side/2))
		body_points.add((WIDTH/2-6*snake_side-snake_side,HEIGHT/2-snake_side/2))
		body_points.add((WIDTH/2-7*snake_side-snake_side,HEIGHT/2-snake_side/2))
		self.body.append(Body(0,HEIGHT/2-snake_side/2,WIDTH/2-0*snake_side-snake_side))
		self.body.append(Body(1,HEIGHT/2-snake_side/2,WIDTH/2-1*snake_side-snake_side))
		self.body.append(Body(2,HEIGHT/2-snake_side/2,WIDTH/2-2*snake_side-snake_side))
		self.body.append(Body(3,HEIGHT/2-snake_side/2,WIDTH/2-3*snake_side-snake_side))
		self.body.append(Body(4,HEIGHT/2-snake_side/2,WIDTH/2-4*snake_side-snake_side))
		self.body.append(Body(5,HEIGHT/2-snake_side/2,WIDTH/2-5*snake_side-snake_side))
		self.body.append(Body(6,HEIGHT/2-snake_side/2,WIDTH/2-6*snake_side-snake_side))
		self.body.append(Body(7,HEIGHT/2-snake_side/2,WIDTH/2-7*snake_side-snake_side))
		self.i = 8
		
	def update(self):
		global body_points
		p = (self.body[-1].rect.centerx,self.body[-1].rect.centery)
		for b in range(1,len(self.body)):
			b = -b
			self.body[b].Update(self.body[b-1].rect.x,self.body[b-1].rect.y)
		if(self.body[-1].rect.center == p):
			pass
		else:
			body_points = body_points-set([p])
		if(True):
			keystate = pygame.key.get_pressed()
			if keystate[pygame.K_LEFT] and self.speedx != snake_side:
					self.tempy = 0
					self.tempx = -snake_side
			if keystate[pygame.K_RIGHT] and self.speedx != -snake_side:
					self.tempy = 0
					self.tempx = snake_side
			if keystate[pygame.K_UP] and self.speedy != snake_side:
					self.tempy = -snake_side
					self.tempx = 0
			if keystate[pygame.K_DOWN] and self.speedy != -snake_side:
					self.tempx = 0
					self.tempy = snake_side
		self.speedx = self.tempx
		self.speedy = self.tempy
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.x > WIDTH - snake_side:
			self.rect.x = 0
		if self.rect.y > HEIGHT -snake_side :
			self.rect.y = 0
		if self.rect.x < 0 :
			self.rect.x = WIDTH
		if self.rect.y < 0 :
			self.rect.y = HEIGHT
		l = len(body_points)
		body_points.add(self.rect.center)
		if(l == len(body_points)):
			for i in range(1,len(self.body)):
				self.body[i].kill()
			self.i = 8
			body_points = body_points - body_points
			for i in range(8):
				body_points.add((WIDTH/2-(i)*snake_side-snake_side,HEIGHT/2-snake_side/2))
				self.body.append(Body(0,HEIGHT/2-snake_side/2,WIDTH/2-0*snake_side-snake_side))
				self.rect.centery = HEIGHT/2-snake_side/2
				self.rect.centerx = (WIDTH/2-snake_side/2)
				self.speedx = snake_side
				self.speedy = 0


class Food(pygame.sprite.Sprite):
	def __init__(self,player):
		self.player=player
		pygame.sprite.Sprite.__init__(self)
		#every sprite we create should have
		#if u want to put an img then pygame.image.load(path).convert()
		self.image = pygame.Surface((snake_side,snake_side))
		#to neglect the rect color self.image.set_colorkey(black)
		self.image.fill(red_)
		point = points - body_points
		self.rect = self.image.get_rect()
		self.rect.center = random.sample(point, 1)[0]
			
	def change(self):
		point = points - body_points
		self.rect.center = random.sample(point, 1)[0]
		
	def update(self):
		pass


ag = agr()
border = np.float32([[0,0,0],[0.4,0,0],[0.4,0.3,0],[0,0.3,0],[0,0,0.05],[0.4,0,0.05],[0.4,0.3,0.05],[0,0.3,0.05]])

player = Player(0)
food = Food(player)
all_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()
food_sprites.add(food)
all_sprites.add(player,food)
for b in player.body:
	all_sprites.add(b)

RUNING = True
while(RUNING):
	#pause till it reaches fps
	sleep(0.05)

	#clock.tick(FPS)
	#Processed input

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			RUNING = False
	#update
	cp = []
	all_sprites.update()
	for b in player.body:
		cp.append(ag.centre2corners(ag.scaling(b.rect.x,b.rect.y)+[0],ag.scaling(b.rect.bottomright[0],b.rect.bottomright[1])+[0.025]))
	fo = ag.centre2corners(ag.scaling(food.rect.x,food.rect.y)+[0],ag.scaling(food.rect.bottomright[0],food.rect.bottomright[1])+[0.025])
	cp2 = []
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
					for cp1 in cp: 
						a, _  =cv2.projectPoints(cp1,rvecs,tvecs,ag.mtx,ag.dist)
						cp2.append(a)
					fo , _ = cv2.projectPoints(fo,rvecs,tvecs,ag.mtx,ag.dist)
					img = cv2.flip(ag.draw(frame,cp2,fo,bdr),1)					
					cv2.imshow('img',img)
					#return
			#cv2.imshow('img2',frame)
			#return
	cv2.waitKey(10)

	if(player.rect.center == food.rect.center):
		player.body.append(Body(player.i,player.body[-1].rect.centery,player.body[-1].rect.centerx))
		all_sprites.add(player.body[-1])
		player.i += 1
		food.change()
	'''hits = pygame.sprite.spritecollide(ball,game_players,False)
	if hits:
		ball.refx()
		pass
	'''
	#draw
	screen.fill(w_)
	all_sprites.draw(screen)
	pygame.display.flip()

pygame.quit()	