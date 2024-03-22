import cv2
imagem = cv2.imread('entrada.jpg')

for i in range(0,imagem.shape[0],10): #Pula de 10 em 10
    for j in range(0,imagem.shape[1],10):
        imagem[i:i+5,j:j+5] = (0,255,255) 

cv2.imshow('Imagem modificada', imagem)
cv2.waitKey(0) 



 

