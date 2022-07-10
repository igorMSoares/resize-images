from PIL import Image, ImageOps

import os
from os import listdir

import logging
logFile = 'log.txt'
logging.basicConfig(
    filename= logFile,
    filemode= 'w',
    level   = logging.INFO,
    format  = '%(asctime)s\n%(levelname)s: %(message)s\n',
    datefmt = '%d/%b/%Y %H:%M:%S')
log = False # Variável de controle será setada True quando algo for adicionado ao arquivo de log

imgDir     = './imgs'
resizedDir = f'{imgDir}/resized'
totalFiles = 0

# TESTANDO SE VALOR DIGITADO É UM NÚMERO, USANDO REGULAR EXPRESSIONS
import re # Regular Expressions Library
maxSize= input('Qual tamanho, em pixels, deverá ter o maior lado da imagem? (A proporção será mantida)\n')

while not re.match('^\d+\s{0,1}(px){0,1}$', maxSize): # 1 ou mais dígitos, seguido por 1 ou nenhum espaço, seguido, ou não, pela unidade 'px'
    # EXEMPLO DE VALORES VÁLIDOS: '1200', '1200px'ou '1200 px'
    print(f'\n[ERRO] "{maxSize}" não é um número válido. Tente novamente.\n')
    maxSize= input('Qual tamanho, em pixels, deverá ter o maior lado da imagem? (Ex.: 1200px)\n')
else:
    maxSize = int(maxSize.strip('px'))

# while True: # TESTANDO SE VALOR DIGITADO É UM NÚMERO, USANDO try except
#     try:
#         maxSize = input('Qual tamanho do maior Lado?\nDigite um valor númerico apenas, sem usar a unidade "px": ')
#         maxSize = int(maxSize.strip('px'))
#         break
#     except ValueError:
#         print(f'\n[ERRO] "{maxSize}" não é numero. Tente novamente\n')

### TESTANDO SE VALOR DIGITADO É UM NÚMERO, SEM USAR try except
# maxSize = input('Qual tamanho do maior Lado?\nDigite um valor númerico apenas, sem usar a unidade "px": ')
#
# while not maxSize.isnumeric():
#     print(f'\nErro! "{maxSize}" não é numero. Tente novamente\n')
#     maxSize = input('Qual tamanho do maior Lado?\nDigite um valor númerico apenas, sem usar a unidade "px": ')
# else:
#     maxSize = int(maxSize)

for fileName in os.listdir(imgDir):
    filePath = f'{imgDir}/{fileName}'

    # CONFERE SE É REALMENTE UM ARQUIVO, E NÃO UMA PASTA
    if os.path.isfile(filePath):
        try:
            with Image.open(filePath) as image: # CONTEXT MANAGER PARA GARANTIR QUE ARQUIVO SERÁ FECHADO QUANDO NÃO FOR MAIS NECESSÁRIO
                image = ImageOps.exif_transpose(image) # MANTÉM A ORIENTAÇÃO DA IMAGEM ORIGINAL

                if maxSize > max(image.size):
                    logging.info(f'"{fileName}" não foi redimensionado.\n"{maxSize}px" é maior do que o tamanho original da imagem: ({image.width}px,{image.height}px)')
                    if not log: log = True
                else:
                    image.thumbnail((maxSize,maxSize)) # APLICA maxSize APENAS NO MAIOR LADO E MANTÉM A PROPORÇÃO ORIGINAL
                    image.save(f'{resizedDir}/{fileName}')
                    totalFiles+=1

        except Image.UnidentifiedImageError as error:
            logging.warning(f'{error} (não é um arquivo de imagem válido)\n')
            if not log: log = True

msg = f'\n{totalFiles} arquivos redimensionados'
if totalFiles > 0:
    msg+=f' e salvos na pasta "{resizedDir}"'

print(msg)
if log: print(f'Acesse o arquivo "./{logFile}" para mais informações')
