#Menggunakan library numpy untuk pengolahan data dan library pillow untuk image
import numpy            #import library numpy
from PIL import Image   #import library pillow untuk pengolahan citra gambar
from modules.svdutils import *

ukuran = int(input("Masukkan ukuran file yang ingin dikompresi: "))

def bacaGambar(pathGambar):
    imageOri = Image.open(pathGambar)
    im = numpy.array(imageOri)

    redColor = im[:, :, 0]
    greenColor = im[:, :, 1]
    blueColor = im[:, :, 2]

    return [redColor, greenColor, blueColor, imageOri]


def imageCompression(dataMatrix, singularValues):
    data1, data2, data3 = svd_decompose(dataMatrix)
    dataCompression = numpy.zeros((dataMatrix.shape[0], dataMatrix.shape[1]))
    k = singularValues

    sisiKiri = numpy.matmul(data1[:, 0:k], numpy.diag(data2)[0:k, 0:k])
    dataCompression2 = numpy.matmul(sisiKiri, data3[0:k, :])
    dataCompression = dataCompression2.astype('uint8')
    return dataCompression


print('*** Image Compression using SVD - a demo')
redColor, greenColor, blueColor, originalImage = bacaGambar('static/photo/lena.png')

width =512
height=512

singularValues = ukuran

redColorCompressed = imageCompression(redColor, singularValues)
greenColorCompressed = imageCompression(greenColor, singularValues)
blueColorCompressed = imageCompression(blueColor, singularValues)

imr = Image.fromarray(redColorCompressed, mode=None)
img = Image.fromarray(greenColorCompressed, mode=None)
imb = Image.fromarray(blueColorCompressed, mode=None)

gambarBaru = Image.merge("RGB", (imr, img, imb))

originalImage.show()
gambarBaru.show()

# CALCULATE AND DISPLAY THE COMPRESSION RATIO
mr = height
mc = width

ukuranAwal = mr * mc * 3
ukuranKompresi = singularValues * (1 + mr + mc) * 3

print('original size:')
print(ukuranAwal)

print('compressed size:')
print(ukuranKompresi)

print('Ratio compressed size / original size:')
ratio = ukuranKompresi * 1.0 / ukuranAwal
print(ratio)

print('Compressed image size is ' + str(round(ratio * 100, 2)) + '% of the original image ')
print('DONE - Compressed the image! Over and out!')
