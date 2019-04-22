from PIL import Image as ImgLib
import numpy as np


class Image(object):

    def __init__(self, imageLocation):
        self.raw = ImgLib.open(imageLocation)
        self.image = self.raw.load()

    def getPixel(self, x, y, convertToGrayScale=True):
        output = list(self.image[x, y])
        if convertToGrayScale:
            grayScale = 0.21*float(output[0])+0.72*float(output[1])+0.07*float(output[2])
            output = [grayScale, grayScale, grayScale]
        return output

    def set(self, x, y, value):
        self.image[x, y] = value

    def getImageArray(self, convertToGrayScale=True):
        imageArray = []
        cols, rows = self.raw.size
        for row in range(rows):
            imageArray.append([])
            for col in range(cols):
                imageArray[row].append(self.getPixel(col, row, convertToGrayScale))
        return imageArray

    @classmethod
    def grayScaleToRGB(cls, listArray):
        rows = len(listArray)
        cols = len(listArray[0])
        output = []
        for row in range(rows):
            output.append([])
            for col in range(cols):
                value = listArray[row][col]
                output[row].append([value, value, value])
        return output

    @classmethod
    def listArrayToNPArray(cls, listArray):
        rows = len(listArray)
        cols = len(listArray[0])
        if ((type(listArray[0][0]) != list) and (type(listArray[0][0]) != tuple)) or (len(listArray[0][0]) == 1):
            listArray = Image.grayScaleToRGB(listArray)
        output = np.zeros((rows, cols, 3), dtype=np.uint8)
        for row in range(rows):
            for col in range(cols):
                #print listArray[row][col][:3]
                output[row, col] = listArray[row][col][:3]
        return output

    @classmethod
    def normalize(cls, listArray):
        rows = len(listArray)
        cols = len(listArray[0])
        if ((type(listArray[0][0]) != list) and (type(listArray[0][0]) != tuple)) or (len(listArray[0][0]) == 1):
            listArray = Image.grayScaleToRGB(listArray)
        maxIntensity = 0
        for row in range(rows):
            for col in range(cols):
                for color in range(3):
                    maxIntensity = max(maxIntensity, listArray[row][col][color])
        print "MAX ", maxIntensity
        for row in range(rows):
            for col in range(cols):
                for color in range(3):
                    listArray[row][col][color] = float(listArray[row][col][color]) / float(maxIntensity)
                    listArray[row][col][color] *= 255
        return listArray

    @classmethod
    def showImage(cls, imageArray):
        imageArray = Image.normalize(imageArray)
        if type(imageArray) == list:
            imageArray = Image.listArrayToNPArray(imageArray)
        image = ImgLib.fromarray(imageArray, 'RGB')
        image.show()

    @classmethod
    def saveImage(cls, listArray, location):
        arr = np.asarray(listArray)
        img = ImgLib.fromarray(arr, 'RGB')
        img.save(location)
