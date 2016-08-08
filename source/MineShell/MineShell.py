from MineField.MineField import MineField
from Deploy import Deploy 
class MineShell:
    def __init__(self):
        self.field = None
        self.space = ' '
        self.deploy = None

    def getInput(self, string):
        strings = string.split(' ')
        #for s in strings:
            #print(s)
        if (strings[0] == 'minefield'):
            return self.createMineField(int(strings[2]), int(strings[1]), int(strings[3]))
        if (strings[0] == 'poke'):
            return self.poke(int(strings[1]), int(strings[2]))
        

    def createMineField(self, height, width, numOfMines):
        self.field = MineField(height, width) 
        self.deploy = Deploy(numOfMines, sefl.field)
        return 'created minefield ' + str(20) + ' x ' + str(10) + ' with ' + str(30)+' mines'

    def poke(self, x, y):
        if (self.field == None):
            return 'no minefield'
        if (x < 0 or x >= self.field.width or y < 0 or y >= self.field.width):
            return 'out of bounds'
        status = self.field.status
        if (status == -1) :
            return 'boom'
        else:
            pos = set ()
            self.getPositionSet(pos, x, y)
        return self.pokeOutPut(pos)

    def pokeOutPut(self, pos):
        out = [] 
        for (x, y) in pos :
            out.append(str(x) + self.space + str(y) + self.space + 'opened as' + self.space + str(self.field.status[x][y]))
        return out

    def getPositionSet(self, pos, x, y):
        if (len(pos) >= self.field.width * self.field.height):
            return 
        if (x < 0 or x >= self.field.getWidth() or y < 0 or y >= self.field.getHeight()):
            return
        if (self.field.status[y][x] == 0):
            pos.add((x,y))
            if (not(x + 1, y) in pos):
                self.getPositionSet(pos, x + 1, y)
            if (not(x - 1, y) in pos):
                self.getPositionSet(pos, x - 1, y)
            if (not(x + 1, y + 1) in pos):
                self.getPositionSet(pos, x + 1, y + 1)
            if (not(x + 1, y - 1) in pos):
                self.getPositionSet(pos, x + 1, y - 1)
            if (not(x, y - 1) in pos):
                self.getPositionSet(pos, x, y - 1)
            if (not(x, y + 1) in pos):
                self.getPositionSet(pos, x, y + 1)
            if (not(x - 1, y - 1) in pos):
                self.getPositionSet(pos, x - 1, y - 1)
            if (not(x - 1, y + 1) in pos):
                self.getPositionSet(pos, x - 1, y + 1)
        else:
            pos.add((x,y))


