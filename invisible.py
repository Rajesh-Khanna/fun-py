import cv2
import numpy as np
def nothing(x):
    pass
kernel = np.ones((3,3),np.uint8)
cv2.namedWindow('frame')
cv2.createTrackbar('lh','frame',0,255,nothing)
cv2.createTrackbar('ls','frame',0,255,nothing)
cv2.createTrackbar('lv','frame',0,255,nothing)
cv2.createTrackbar('uh','frame',0,255,nothing)
cv2.createTrackbar('us','frame',0,255,nothing)
cv2.createTrackbar('uv','frame',0,255,nothing)

cap = cv2.VideoCapture(0)

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


limits = calibration(cap)
_,frame1 = cap.read()
while True:
    _,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    msk = cv2.inRange(hsv,limits[:3],limits[3:])
    msk = cv2.erode(msk,kernel,iterations = 2 )
    msk = cv2.dilate(msk,kernel,iterations = 5)
    dele = cv2.bitwise_not(msk)
    frame= cv2.bitwise_and(frame,frame,mask = dele)
    frame2 = cv2.bitwise_and(frame1,frame1,mask = msk)
    frame2 = cv2.addWeighted(frame,1,frame2,1,0)
    cv2.imshow("res",frame2)
    
    cv2.imshow("o",frame)
    cv2.imshow("mask",msk)
    
    cv2.imshow("dele",dele)
    k = cv2.waitKey(5)
    if k == 27:
        break
