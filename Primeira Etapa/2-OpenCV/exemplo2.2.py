import cv2
imagem = cv2.imread('entrada.jpg')

for i in range(0,imagem.shape[0]): #Percorre as "linhas" da imagem  
    for j in range(0,imagem.shape[1]): #Percorre as coluna respectivas da imagem
        imagem[i,j] = (255,0,0)  #Colore os pixels

cv2.imshow('Imagem modificada', imagem)
cv2.waitKey(0) #faltou no codigo exemplo 