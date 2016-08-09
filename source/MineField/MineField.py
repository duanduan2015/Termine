class MineField:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.status = [[0 for x in range(width)] for y in range(height)]
        self.flagged = [[False for x in range(width)] for y in range(height)]
        self.opened = [[False for x in range(width)] for y in range(height)]
        self.numFlags = 0
    
    def getHeight(self):
        return self.height
    def getWidth(self):
        return self.width
    def isFlagged(self, x, y):
        return self.flagged[y][x]
    def getStatus(self, x, y):
        return self.status[y][x];
    def flagMine(self, x, y):
        flagged[y][x] = true;
        self.numFlags = self.numFlags + 1
    def setStatus(self, x, y, status):
        self.status[y][x] = status 
    def getFlagNumber(self):
        return self.numFlags

