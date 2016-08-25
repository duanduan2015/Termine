import random
class DeployMines:
    def __init__(self, field, num, x, y):
        self.field = field
        self.num = num
        self.space = ' '
        self.startx = x
        self.starty = y

    def deployField(self):
        #xy = [m for m in range(self.field.width * self.field.height)]
        #minexy = random.sample(xy, self.num)
        #for i in range(len(minexy)) :
        #    self.deploy((int)(minexy[i] / self.field.width), (int)(minexy[i] % self.field.width))
        
        if self.starty - 2 >= 0:
            upWidth, upHeight = self.field.width, self.starty - 1 
        else:
            upWidth, upHeight = self.field.width, 0

        if self.starty + 2 < self.field.height:
            downWidth, downHeight = self.field.width, self.field.height - self.starty - 2
        else:
            downWidth, downHeight = self.field.width, 0

        if self.startx - 2 >= 0:
            leftWidth, leftHeight = self.startx - 1, self.field.height - upHeight - downHeight
        else:
            leftWidth, leftHeight = 0, self.field.height - upHeight - downHeight

        if self.startx + 2 < self.field.width:
            rightWidth, rightHeight = self.field.width - self.startx - 2, self.field.height - upHeight - downHeight
        else:
            rightWidth, rightHeight = 0, leftHeight

        numDivisor = self.num / (self.field.width * self.field.height)
        upNum = (int)(upWidth * upHeight * numDivisor)
        rightNum = (int)(rightWidth * rightHeight * numDivisor)
        downNum = (int)(downWidth * downHeight * numDivisor)
        leftNum = 0
        if leftWidth * leftHeight == 0:
            rightNum = rightNum + self.num - upNum - rightNum - downNum
        else:
            leftNum = self.num - upNum - rightNum - downNum

        xy = [m for m in range(upWidth * upHeight)]
        minexy = random.sample(xy, upNum)
        for i in range(len(minexy)) :
            self.deploy((int)(minexy[i] / upWidth), (int)(minexy[i] % upWidth))

        xy = [m for m in range(rightWidth * rightHeight)]
        minexy = random.sample(xy, rightNum)
        for i in range(len(minexy)) :
            self.deploy((int)(minexy[i] / rightWidth) + upHeight, (int)(minexy[i] % rightWidth) + self.startx + 2)

        xy = [m for m in range(downWidth * downHeight)]
        minexy = random.sample(xy, downNum)
        for i in range(len(minexy)) :
            self.deploy((int)(minexy[i] / downWidth) + self.field.height - downHeight, (int)(minexy[i] % downWidth))

        xy = [m for m in range(leftWidth * leftHeight)]
        minexy = random.sample(xy, leftNum)
        for i in range(len(minexy)) :
            self.deploy((int)(minexy[i] / leftWidth) + upHeight, (int)(minexy[i] % leftWidth))
            
    def deploy(self, y, x):
        self.field.status[y][x] = -1
        self.updateStatusAround(x, y)
        for i in range(self.field.height):
            s = str()
            for j in range(self.field.width):
                s = s + str(self.field.status[i][j])

    def updateStatusAround(self, x, y):
        height = self.field.height
        width = self.field.width
        if y - 1 >= 0 and self.field.status[y - 1][x] >= 0:
            self.field.status[y - 1][x] += 1
        if y + 1 < height and self.field.status[y + 1][x] >= 0:
            self.field.status[y + 1][x] += 1
        if x - 1 >= 0 and self.field.status[y][x - 1] >= 0:
            self.field.status[y][x - 1] += 1
        if x + 1 < width and self.field.status[y][x + 1] >= 0:
            self.field.status[y][x + 1] += 1
        if y - 1 >= 0 and x - 1 >= 0 and self.field.status[y - 1][x - 1] >= 0:
            self.field.status[y - 1][x - 1] += 1
        if y + 1 < height and x + 1 < width and self.field.status[y + 1][x + 1] >= 0:
            self.field.status[y + 1][x + 1] += 1
        if y - 1 >= 0 and x + 1 < width and self.field.status[y - 1][x + 1] >= 0:
            self.field.status[y - 1][x + 1] += 1
        if y + 1 < height and x - 1 >= 0 and self.field.status[y + 1][x - 1] >= 0:
            self.field.status[y + 1][x - 1] += 1
        

        

