import random
class DeployMines:
    def __init__(self, field, num):
        self.field = field
        self.num = num
        self.space = ' '

    def deployField(self):
        x = [m for m in range(self.field.width)]
        y = [m for m in range(self.field.height)]
        minex = random.sample(x, self.num)
        miney = random.sample(y, self.num)
        for i in range(len(minex)) :
            self.deploy(minex[i], miney[i])
            print(minex[i], miney[i])

    def deploy(self, x, y):
        self.field.status[y][x] = -1
        self.updateStatusAround(x, y)
        for i in range(self.field.height):
            s = str()
            for j in range(self.field.width):
                s = s + str(self.field.status[i][j])
            print(s) 

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
        

        

