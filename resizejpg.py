from PIL import Image, ImageOps

import os
from os import listdir

import logging
logging.basicConfig(filename = "log.txt", level = logging.DEBUG)

imgFolder = './imgs'
totalFiles = 0
maxSize = input('Qual tamanho do maior Lado?\nDigite um valor númerico apenas, sem usar a unidade "px": ')

while not maxSize.isnumeric():
    print(f'\nErro! "{maxSize}" não é numero. Tente novamente\n')
    maxSize = input('Qual tamanho do maior Lado?\nDigite um valor númerico apenas, sem usar a unidade "px": ')
else:
    maxSize = int(maxSize)

for fileName in os.listdir(imgFolder):
    filePath = f'{imgFolder}/{fileName}'

    # CONFERE SE É REALMENTE UM ARQUIVO, E NÃO UMA PASTA
    if os.path.isfile(filePath):
        try:
            with Image.open(filePath) as image:
                image = ImageOps.exif_transpose(image) # MANTÉM A ORIENTAÇÃO DA IMAGEM ORIGINAL

                image.thumbnail((maxSize,maxSize)) # APLICA maxSize NO MAIOR LADO E MANTÉM A PROPORÇÃO ORIGINAL
                image.save(f'{imgFolder}/newsize/{fileName}')

                totalFiles+=1
        except:
            with open('log.txt','w') as logFile:
                logging.error(f'"{fileName}" não é um arquivo de imagem válido!\n')

print(f'{totalFiles} arquivos redimensionados com sucesso!')
