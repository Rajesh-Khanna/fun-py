import cv2
from math import sqrt,pi
import numpy as np
from datetime import datetime
import pyautogui
def nothing(x):
    pass


###################### initialization constants #########################

#pyautogui.FAILSAFE = False
newtoscreen = 1
i_px = 0
i_py = 0
m_px = 0
m_py = 0
i_cout = 0
i_coutx = 0
m_cout = 0
m_coutx = 0
i_couty = 0
m_couty = 0
then = datetime.now()
then = then.microsecond
erosion_nu = 2
dialation_nu = 5
kernel = np.ones((3,3),np.uint8)
cv2.namedWindow('frame')
cv2.createTrackbar('lh','frame',0,255,nothing)
cv2.createTrackbar('ls','frame',0,255,nothing)
cv2.createTrackbar('lv','frame',0,255,nothing)
cv2.createTrackbar('uh','frame',0,255,nothing)
cv2.createTrackbar('us','frame',0,255,nothing)
cv2.createTrackbar('uv','frame',0,255,nothing)
cv2.createTrackbar('erosion_nu','frame',1,10,nothing)
cv2.createTrackbar('dialation_nu','frame',1,10,nothing)

#########################################################################

class events():

    def __init__(self,index,middle,radious,r_key):
        
        self.radious = radious
        self.trishold = 0
        self.index = index
        self.midddle = middle
        self.dist = int(sqrt((index[0] - middle[0])**2 + (index[1] - middle[1])**2))
        self.r_key = r_key
    def cclick(self):
        
        if self.dist <= 2*self.radious:
            if self.r_key == 0:
                pyautogui.mouseDown()
            else:
                pyautogui.mouseDown(button='right')
        elif self.dist > 4*self.radious:
            if self.r_key == 0:
                pyautogui.scroll(50)
            else:
                pyautogui.scroll(-50)
        else:
            if self.r_key == 0:
                pyautogui.mouseUp()
            else:
                pyautogui.mouseUp(button = 'right')

cap = cv2.VideoCapture(0)

def centroid(mask,dilation,px,py):
    cout = 0
    coutx = 0
    couty = 0
    for x in range(mask.shape[0]):
        for y in range(mask.shape[1]):
            if dilation.item(x,y) == 255:
                cout = cout + 1
                coutx = coutx + x
                couty = couty + y
    try:
        coutx = coutx/cout
        couty = couty/cout
    except Exception as e:
        #print(e)
        newtoscreen = 1
        coutx = px
        couty = py
    return (coutx,couty,cout)

def mouseg(coutx,couty,px,py,now,then):
    try:
        time = (now - then)/10e6
        dx = (coutx - px)
        dy = (couty - py)
        dx = dx*4
        dy = dy*4
        pyautogui.moveRel(dx,dy,0.1)
    except Exception as e:
        print(e)

def calibration(cap):
    while True:        
        _,frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lh = cv2.getTrackbarPos('lh','frame')
        ls = cv2.getTrackbarPos('ls','frame')
        lv = cv2.getTrackbarPos('lv','frame')
        uh = cv2.getTrackbarPos('uh','frame')
        us = cv2.getTrackbarPos('us','frame')
        uv = cv2.getTrackbarPos('uv','frame')
        dialation_nu = cv2.getTrackbarPos('dialation_nu','frame')
        erosion_nu = cv2.getTrackbarPos('erosion_nu','frame')
        mask = cv2.inRange(hsv,(lh,ls,lv),(uh,us,uv))
        erosion = cv2.erode(mask,kernel,iterations = erosion_nu)
        dilation = cv2.dilate(erosion,kernel,iterations = dialation_nu)
        cv2.imshow('mask',dilation)
        k = cv2.waitKey(1)
        if k == 27:
            break
    limits = (lh,ls,lv,uh,us,uv)
    return limits

def start_mouse_control(cap,index,middle,right,then,ppx = 240,ppy = 340,i_px = 0,i_py = 0,m_px = 0,m_py = 0,i_cout = 0,i_coutx = 0,m_cout = 0,m_coutx = 0,i_couty = 0,m_couty = 0):
    while True:
        r_key = 0
        now = datetime.now()
        now = now.microsecond
        _,frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        i_mask = cv2.inRange(hsv,index[:3],index[3:])
        m_mask = cv2.inRange(hsv,middle[:3],middle[3:])
        i_erosion = cv2.erode(i_mask,kernel,iterations = 3)
        i_dilation = cv2.dilate(i_erosion,kernel,iterations = 6)
        m_erosion = cv2.erode(m_mask,kernel,iterations = 3)
        m_dilation = cv2.dilate(m_erosion,kernel,iterations = 6)
        r_mask = cv2.inRange(hsv,right[:3],right[3:])
        r_erosion = cv2.erode(r_mask,kernel,iterations = 3)
        r_dilation = cv2.dilate(r_erosion,kernel,iterations = 6)

        i_center = centroid(i_mask,i_dilation,i_px,i_py)
        m_center = centroid(m_mask,m_dilation,m_px,m_py)
        r_center = centroid(r_mask,r_dilation,0,0)
        c = i_center[2] 
        if r_center[2] > 20:
            r_key = 1
        c = int (c)

        
        radious = int(sqrt(c/pi)) + 5
        flip = cv2.flip(frame,1)
        cv2.circle(flip,(int(i_mask.shape[1] - i_center[1] - 1),int(i_center[0])),3,(0,0,255),-1)
        cv2.circle(flip,(int(i_mask.shape[1] - i_center[1] - 1),int(i_center[0])),radious,(0,0,255),2)
        indexp = (i_mask.shape[1] - i_center[1] - 1,i_center[0])
        middlep = (i_mask.shape[1] - m_center[1] - 1,m_center[0])
        if not radious < 15:
            mouseg(int(i_mask.shape[1] - i_center[1] - 1),int(i_center[0]),i_py,i_px,now,then)
            mc = events(indexp,middlep,radious,r_key)
            mc.cclick()
            
        
        i_px = int(i_center[0])
        i_py = int(i_mask.shape[1] - i_center[1] - 1)
        r_key = 0
        cv2.imshow('tracker',flip)
        then = now
        k = cv2.waitKey(1)  
        if k == 27: 
            break




index = calibration(cap)

middle = calibration(cap)

right = calibration(cap)
cv2.destroyAllWindows()

c = pyautogui.size()
pyautogui.moveTo(int(c[0]/2),int(c[1]/2))

start_mouse_control(cap,index,middle,right,then)



cap.release()
cv2.destroyAllWindows()
