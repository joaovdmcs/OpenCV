#Programa para estudo de deteccao de cor - amarelo - versao GIF


import cv2
import numpy as np

video = cv2.VideoCapture('road.mp4')

trackbarWindow = 'trackbar window'
cv2.namedWindow(trackbarWindow)

def trackbarLimit():
    
    hue = {}
    hue['min'] = cv2.getTrackbarPos('Min_Hue', trackbarWindow)
    hue['max'] = cv2.getTrackbarPos('Max_Hue', trackbarWindow)   
    if hue['min'] > hue['max']:
        cv2.setTrackbarPos('Max_Hue', trackbarWindow, hue['min'])
        hue['max'] = cv2.getTrackbarPos('Max_Hue', trackbarWindow)
    
    sat = {}
    sat['min'] = cv2.getTrackbarPos('Min_Sat',trackbarWindow)
    sat['max'] = cv2.getTrackbarPos('Max_Sat',trackbarWindow)
    if sat['min'] > sat['max']:
        cv2.setTrackbarPos('Max_Sat',trackbarWindow, sat['min'])
        sat['max'] = cv2.getTrackbarPos('Max_Sat', trackbarWindow)
        
    val = {}
    val['min'] = cv2.getTrackbarPos('Min_Val',trackbarWindow)
    val['max'] = cv2.getTrackbarPos('Max_Val',trackbarWindow)
    if val['min'] > val['max']:
        cv2.setTrackbarPos('Max_Val', trackbarWindow,val['min'])
        val['max'] = cv2.getTrackbarPos('Max_Val', trackbarWindow)
    
    
    return hue,sat,val

def computeTracking(frame,hue,sat,val):
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #frame da imagem para HSV
    
    #Intervalos de Coloracao na imagem final
    lowerColor = np.array([hue['min'],sat['min'],val['min']])
    upperColor = np.array([hue['max'],sat['max'],val['max']])
    mask = cv2.inRange(image,lowerColor,upperColor) #formacao de uma nova "imagem" com pixels pertencentes ao intervalo upper lower
    
    result = cv2.bitwise_and(frame,frame,mask=mask) #comparacao dos pixels da imagem com ela mesma com a mask como fator "determinante" da cor resultante(filtracao de pixels).
    
    gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    _,gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    return gray

def onChange(val):
    return
cv2.createTrackbar('Min_Hue',trackbarWindow, 0, 255, onChange)
cv2.createTrackbar('Max_Hue',trackbarWindow, 255, 255, onChange)

cv2.createTrackbar('Min_Sat',trackbarWindow, 0, 255, onChange)
cv2.createTrackbar('Max_Sat',trackbarWindow, 255, 255, onChange)

cv2.createTrackbar('Min_Val',trackbarWindow, 0, 255, onChange)
cv2.createTrackbar('Max_Val',trackbarWindow, 255, 255, onChange)

min_hue = cv2.getTrackbarPos('Min_Hue', trackbarWindow)
max_hue = cv2.getTrackbarPos('Max_Hue', trackbarWindow)

min_sat = cv2.getTrackbarPos('Min_Sat', trackbarWindow)
max_sat = cv2.getTrackbarPos('Max_Sat', trackbarWindow)

min_value = cv2.getTrackbarPos('Min_Val', trackbarWindow)
max_value = cv2.getTrackbarPos('Max_Val', trackbarWindow)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
   
    succ, frame = video.read()
    cv2.imshow('Road', frame)
    
    hue,sat,val = trackbarLimit()
    gray = computeTracking(frame, hue, sat, val)
    cv2.imshow("Mask", gray)
    
    
   
video.release()
cv2.destroyAllWindows()