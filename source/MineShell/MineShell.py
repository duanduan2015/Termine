from MineField.MineField import MineField
from DeployMines.DeployMines import DeployMines 
from queue import Queue
class MineShell:
    def __init__(self):
        self.field = None
        self.space = ' '
        self.flagNum = 0
        self.mineNum = 0
        #self.deploy = None

    def getInput(self, string):
        strings = string.split(' ')
        #for s in strings:
            #print(s)
        if (strings[0] == 'minefield'):
            return self.createMineField(int(strings[2]), int(strings[1]), int(strings[3]))
        if (strings[0] == 'poke'):
            return self.poke(int(strings[1]), int(strings[2]))
        if (strings[0] == 'peek'):
            return self.peek(int(strings[1]), int(strings[2]))
        if (strings[0] == 'flag'):
            return self.flag(int(strings[1]), int(strings[2]))
        if (strings[0] == 'unflag'):
            return self.unflag(int(strings[1]), int(strings[2]))
        if strings[0] == 'deploy':
            return self.deploy(int(strings[1]), int(strings[2]))
        if (strings[0] == 'query'):
            if strings[1] == 'flags':
                return str(self.flagNum)
            if strings[1] == 'mines':
                return str(self.mineNum)
            if strings[1] == 'width':
                return str(self.field.width)
            if strings[1] == 'height':
                return str(self.field.height)
            if strings[1] == 'success':
                if self.isSuccess():
                    return 'yes'
                else:
                    return 'no'
    def deploy(self, x, y):
        if x < 0 or x >= self.field.width or y < 0 or y >= self.field.height:
            return 'out of bounds'
        self.field.status[y][x] = -1
        self.updateStatusAround(x, y)
        return str(x) + self.space + str(y) + self.space + 'deployed'
    def updateStatusAround(self, x, y):
        height = self.field.height
        width = self.field.width
        if y - 1 >= 0:
            self.field.status[y - 1][x] += 1
        if y + 1 < height:
            self.field.status[y + 1][x] += 1
        if x - 1 >= 0:
            self.field.status[y][x - 1] += 1
        if x + 1 < width:
            self.field.status[y][x + 1] += 1
        if y - 1 >= 0 and x - 1 >= 0:
            self.field.status[y - 1][x - 1] += 1
        if y + 1 < height and x + 1 < width:
            self.field.status[y + 1][x + 1] += 1
        if y - 1 >= 0 and x + 1 > width:
            self.field.status[y - 1][x + 1] += 1
        if y + 1 < height and x - 1 >= 0:
            self.field.status[y + 1][x - 1] += 1
        


    def isSuccess(self):
        if self.flagNum != self.mineNum:
            return False
        for y in range(self.field.height):
            for x in range(self.field.width):
                if self.field.status[y][x] == -1 and self.field.flagged[y][x] == False:
                    return False
        return True

    def flag(self, x, y):
        if x < 0 or x >= self.field.width or y < 0 or y >= self.field.height:
            return 'out of bounds'
        if self.field.flagged[y][x] is False:
            self.field.flagged[y][x] = True
            self.flagNum = self.flagNum + 1
        return str(x) + self.space + str(y) + self.space + 'flagged'

    def unflag(self, x, y):
        if x < 0 or x >= self.field.width or y < 0 or y >= self.field.height:
            return 'out of bounds'
        if self.field.flagged[y][x] == True:
            self.field.flagged[y][x] = False
            self.flagNum = self.flagNum - 1
        return str(x) + self.space + str(y) + self.space + 'unflagged'
 

    
    
    def peek(self, x, y):
        if x < 0 or x >= self.field.width or y < 0 or y >= self.field.height:
            return 'out of bounds'
        if self.field.flagged[y][x] == True:
            return 'flagged'
        #if self.field.opened[y][x] == False:
        #    return 'unexplored'    
        return str(self.field.status[y][x])



    def createMineField(self, height, width, numOfMines):
        self.field = MineField(height, width) 
        self.mineNum = numOfMines
        d = DeployMines(self.field, numOfMines)
        d.deployField()
        return 'created minefield ' + str(width) + ' x ' + str(height) + ' with ' + str(numOfMines)+' mines'

    def poke(self, x, y):
        if (self.field == None):
            return 'no minefield'
        if (x < 0 or x >= self.field.width or y < 0 or y >= self.field.width):
            return 'out of bounds'
        status = self.field.status[y][x]
        if (status == -1) :
            return 'boom'
        else:
            pos =  set()
            queue = Queue()
            queue.put((x,y))
            self.field.opened[y][x] = True
            while queue.qsize() > 0:
                p = queue.get();
                px = p[0]
                py = p[1]
                if px - 1 >= 0:
                    if py - 1 >= 0:
                        if not (px - 1, py - 1) in pos and self.field.status[py - 1][px - 1] != -1:
                            if self.field.opened[py - 1][px - 1] is False:
                                pos.add((px - 1, py - 1))
                                self.field.opened[py - 1][px - 1] = True
                            if self.field.status[py - 1][px - 1] == 0:
                                queue.put((px - 1, py - 1))
                    if py + 1 < self.field.height:
                        if not (px - 1, py + 1) in pos and self.field.status[py + 1][px - 1] != -1:
                            if self.field.opened[py + 1][px - 1] is False: 
                                pos.add((px - 1, py + 1))
                                self.field.opened[py + 1][px - 1] = True
                            if self.field.status[py + 1][px - 1] == 0:
                                queue.put((px - 1, py + 1))
                    if not (px - 1, py) in pos and self.field.status[py][px - 1] != -1:
                        if self.field.opened[py][px - 1] is False:
                            pos.add((px - 1, py))
                            self.field.opened[py][px - 1] = True
                        if self.field.status[py][px - 1] == 0:
                            queue.put((px - 1, py))
                if py - 1 >= 0:
                    if not (px, py - 1) in pos and self.field.status[py - 1][px] != -1:
                        if self.field.opened[py - 1][px] is False: 
                            pos.add((px, py - 1))
                            self.field.opened[py - 1][px] = True
                        if self.field.status[py - 1][px] == 0:
                            queue.put((px, py - 1))
                if py + 1 < self.field.height:
                    if not (px, py + 1) in pos and self.field.status[py + 1][px] != -1:
                        if self.field.opened[py + 1][px] is False:
                            pos.add((px, py + 1))
                            self.field.opened[py + 1][px] = True
                        if self.field.status[py + 1][px] == 0:
                            queue.put((px, py + 1))
                if px + 1 < self.field.width:
                    if py - 1 >= 0:
                        if not (px + 1, py - 1) in pos and self.field.status[py - 1][px + 1] != -1:
                            if self.field.opened[py - 1][px + 1] is False:
                                pos.add((px + 1, py - 1))
                                self.field.opened[py - 1][px + 1] = True
                            if self.field.status[py - 1][px + 1] == 0:
                                queue.put((px + 1, py - 1))
                    if py + 1 < self.field.height:
                        if not (px + 1, py + 1) in pos and self.field.status[py + 1][px + 1] != -1:
                            if self.field.opened[py + 1][px + 1] is False:
                                pos.add((px + 1, py + 1))
                                self.field.opened[py + 1][px + 1] = True
                            if self.field.status[py + 1][px + 1] == 0:
                                queue.put((px + 1, py + 1))
                    if not (px + 1, py) in pos and self.field.status[py][px + 1] != -1:
                        if self.field.opened[py][px + 1] is False: 
                            pos.add((px + 1, py))
                            self.field.opened[py][px + 1] = True
                        if self.field.status[py][px + 1] == 0:
                            queue.put((px + 1, py))
        return self.pokeOutPut(pos)

    def pokeOutPut(self, pos):
        out = [] 
        for (x, y) in pos :
            out.append(str(x) + self.space + str(y) + self.space + 'opened as' + self.space + str(self.field.status[y][x]))
        return out



