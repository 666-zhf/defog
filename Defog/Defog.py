from Image import Image
import numpy as np

class Defog(object):

    MIN_PRIOR_OMEGA = 2

    def __init__(self, imageLocation):
        image = Image(imageLocation)
        self.image = image.getImageArray(convertToGrayScale=False)
        self.rows = len(self.image)
        self.cols = len(self.image[0])
        self.priors = None
        self.depthMapVal = None

    def maxPrior(self, x, y):
        return max(self.image[x][y][0], self.image[x][y][1], self.image[x][y][2])

    def minPriorForGrid(self, xstart, xend, ystart, yend):
        output = 255
        for row in range(xstart, xend+1):
            for col in range(ystart, yend+1):
                for color in range(3):
                    output = min(output, self.image[row][col][color])
        return output

    def minPrior(self, x, y):
        xstart = max(x-Defog.MIN_PRIOR_OMEGA, 0)
        xend = min(x+Defog.MIN_PRIOR_OMEGA, self.rows-1)
        ystart = max(y-Defog.MIN_PRIOR_OMEGA, 0)
        yend = min(y+Defog.MIN_PRIOR_OMEGA, self.cols-1)
        return self.minPriorForGrid(xstart, xend, ystart, yend)

    def initAirlight(self):
        temp = []
        for row in range(self.rows):
            for col in range(self.cols):
                pixel = self.image[row][col]
                temp.append(float(pixel[0]+pixel[1]+pixel[2])/3)
        temp = sorted(temp, reverse=True)
        cutoff = (self.rows*self.cols)/1000
        temp = temp[:cutoff]
        return np.mean(temp)

    def airlight(self, depthMap):
        return self.initAirlight()

    def getPriors(self):
        priors = []
        airlight = self.initAirlight()
        for row in range(self.rows):
            priors.append([])
            for col in range(self.cols):
                priors[row].append([])
                priors[row][col].append(max(0, airlight-self.maxPrior(row, col))/airlight)
                priors[row][col].append(max(0, airlight-self.minPrior(row, col))/airlight)
        return priors

    def showPrior(self, priors):
        for prior in range(2):
            imgArray = []
            for row in range(self.rows):
                imgArray.append([])
                for col in range(self.cols):
                    imgArray[row].append(priors[row][col][prior])
            Image.showImage(imgArray)

    @property
    def depthMap(self):
        self.depthMapVal = []
        for row in range(self.rows):
            self.depthMapVal.append([])
            for col in range(self.cols):
                value = 0
                for prior in self.priors[row][col]:
                    value += prior
                value /= 2
                self.depthMapVal[row].append(value)
        return self.depthMapVal

    def showInitImage(self):
        depthMap = self.depthMap
        init = []
        for row in range(self.rows):
            init.append([])
            for col in range(self.cols):
                init[row].append(list(self.image[row][col]))
                init[row][col][0] = min(float(init[row][col][0]) / float(depthMap[row][col]), 255)
                init[row][col][1] = min(float(init[row][col][1]) / float(depthMap[row][col]), 255)
                init[row][col][2] = min(float(init[row][col][2]) / float(depthMap[row][col]), 255)
        Image.showImage(init)

    def defog(self):
        Image.showImage(self.image)
        self.priors = self.getPriors()
        self.showPrior(self.priors)
        Image.showImage(self.depthMap)

        airlight = self.airlight(self.depthMapVal)
        temp = []
        for row in range(self.rows):
            temp.append([])
            for col in range(self.cols):
                temp[row].append([])
                for color in range(3):
                    value = max(float(airlight-self.image[row][col][color]), 0)
                    depthMapVal = self.depthMapVal[row][col]
                    value = min(value / max(depthMapVal, 0.5), 2500)
                    value = max(airlight - value, 0)
                    temp[row][col].append(value)

        Image.showImage(temp)
