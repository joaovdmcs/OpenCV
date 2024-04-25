#Programa para estudo de deteccao de cor - amarelo


import cv2
import numpy as np

lower = np.array([15,150,20])
upper = np.array([35,255,255])

image = cv2.imread('bola3.jpg')
bola = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
mask = cv2.inRange(bola,lower,upper)

contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

if len(contours) != 0 :
    for c in contours:
        if cv2.contourArea(c) > 500:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),3)

cv2.imshow('Mask', mask)
cv2.imshow('Image', image)
cv2.waitKey(0)