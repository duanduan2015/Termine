import MineField from MineField
class MineShell:
    def __init(self):
        self.field = None
        return 'Mine Shell begins'
    def createMineField(self, height, width, numOfMines):
        self.field = new MineField(height, width) 
        return 'created minefield ' + str(20) + ' x ' + str(10) + ' with ' + str(30)+' mines'
    def poke(self, x, y):
        if (field == None):
            return 'no minefield'
