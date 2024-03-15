import cv2 #import da biblioteca opencv-python

imagem = cv2.imread('entrada.jpg') #leitura da imagem no atual diretorio e atribuicao à variavel "imagem"

print('Largura em pixels: ', end = '')
print(imagem.shape[1]) #indice de largura
print('Altura em pixels: ', end = '')
print(imagem.shape[0]) #indice de altura
print('Qtde de canais: ', end = '')
print(imagem.shape[2]) #indice do numero de canais

cv2.imshow('Nome da Janela', imagem) #ilustração da imagem, similar à ilustração do grafico pelo matplotlib/pyplot
cv2.waitKey(0) #espera ser digitado algum caractere

cv2.imwrite('saida.jpg', imagem) #escreve a imagem da linha 3 em um novo arquivo (sendo de maior tamanho)
