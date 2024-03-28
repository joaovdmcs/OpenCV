#Programa para tracking de veiculos e deteccao de direcao - video road.mp4

import cv2
import numpy as np
import time
from collections import deque

video = cv2.VideoCapture('road.mp4') #captura do video

#criacao de variaveis
trackbarWindow = 'trackbar window'
cv2.namedWindow(trackbarWindow)
pts = deque(maxlen=32)
counter = 0 #contador de frames para o buffer de direcao

def trackbarLimit(): #funcao que levanta constraints para a interface grafica de selecao de hue, saturacao e valor HSV da mascara.
    
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
    
    gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY) #cria um frame cinza com base em result
    _,gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU) #utiliza o metodo OTSU de limiarizacao em cima de gray
    
    contours, hierarchy = cv2.findContours(gray,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #formacao de contorno nos objetos
    
    if contours:
        #variaveis locais
        direction = ''
        (dX,dY) = (0,0)
        maxArea = cv2.contourArea(contours[0]) #caso existe contorno, seleciona um contorno 0 na lista de contornos para achar o maior
        i = 0
        contourMaxAreaId = 0
        
        #processo de busca do maior contorno
        for c in contours:
            if maxArea < cv2.contourArea(c):
                maxArea = cv2.contourArea(c)
                contourMaxAreaId = i 
            
            i+=1
        contourMaxArea = contours[contourMaxAreaId]
        
        #formacao das coordenadas de um retangulo do maior contorno encontrado anteriormente
        x,y,w,h = cv2.boundingRect(contourMaxArea)
        
        #desenho do retangulo em frame
        cv2.rectangle(frame,(x,y) ,(x+w,y+h), (0,0,255),2)
        #definicao do centro do retangulo e realizacao de append das cordenadas do ponto em pts (para a definicao de direcao)
        ponto = (int((2*x+w)/2),int((2*y+h)/2))
        pts.appendleft(ponto)
        
        for i in np.arange(1,len(pts)):
            if pts[i-1] is None or pts[i] is None:
                continue
            if counter >= 10 and i == 1 and pts[-10] is not None:
                dX = pts[-10][0] - pts[i][0]
                dY = pts[-10][1] - pts[i][1]
                (dirX, dirY) = ("", "")
                
                if np.abs(dX) > 20:
                    dirX = 'Leste' if np.sign(dX) == 1 else 'Oeste'
                
                if np.abs(dY) > 20:
                    dirY = 'Norte' if np.sign(dY) == 1 else 'Sul'
                    
                if dirX != '' and dirY != '':
                    direction == "{}-{}".format(dirY,dirX)
                    
                else:
                    direction = dirX if dirX != '' else dirY
            cv2.line(frame,pts[i-1],pts[i],(0,255,255),4) 
            cv2.putText(frame,direction,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,0,255),3)
            cv2.putText(frame,'dx:{},dy{}'.format(dX,dY),(10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,255),1)
              
    
    return frame,gray

def onChange(val): #funcao reduntante para a criacao da trackbar
    return

#criacao da trackbar grafica que permitira a mudanca de valores da mascara.
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

#inicio dos processos
while True:
    #condicao de finalizacao antecipada (antes do video acabar)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #leitura dos frames do video
    succ, frame = video.read()
    
    #processo que recebe os valores com constraints ja aplicados na trackbar (i.e o valor minimo de Hue NAO pode ser maior que o maximo)
    hue,sat,val = trackbarLimit()
    
    frame,gray = computeTracking(frame, hue, sat, val)
    
    #mostra duas janelas, uma contendo a mascara do frame filtrado, o outro o frame com retangulo sobre a maior area dentro das especificaoes de filtracao
    #uma linha demonstrando a trajetoria, a trajetoria cardinal e coordenadas da linha
    cv2.imshow("Mask", gray)
    cv2.imshow('Road', frame)
    #contador para o buffer da trajetoria (conta os frames)
    counter += 1
    
    
    

#apos finalizacao da captura, realisa release no video e destroi todas as janelas criadas.
video.release()
cv2.destroyAllWindows()