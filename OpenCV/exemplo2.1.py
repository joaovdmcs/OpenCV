import cv2

imagem = cv2.imread('entrada.jpg')
(b,g,r) = imagem[0,0] #Blue Green Red ao invés de Red Green Blue

print('O pixel (0,0) tem as seguintes cores:')
print('Vermelho:',r,'Verde:',g,'Azul:',b)