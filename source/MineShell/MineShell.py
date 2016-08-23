from MineField.MineField import MineField
from DeployMines.DeployMines import DeployMines 
from collections import deque
class MineShell:
    def __init__(self):
        self.field = None
        self.space = ' '
        self.flagNum = 0
        self.mineNum = 0

    def getInput(self, string):
        strings = string.split(' ')
        if (strings[0] == 'minefield'):
            return self.createMineField(int(strings[2]), int(strings[1]), int(strings[3]))
        if self.field == None:
            return 'no minefield'
        if (strings[0] == 'poke'):
            x = int(strings[1])
            y = int(strings[2])
            if not self.checkPositionValid(x, y):
                return 'out of bounds'
            pos =  self.poke(x, y)
            return self.pokeOutPut(pos)
        if (strings[0] == 'peek'):
            x = int(strings[1])
            y = int(strings[2])
            if not self.checkPositionValid(x, y):
                return 'out of bounds'
            return self.peek(x, y)
        if (strings[0] == 'flag'):
            x = int(strings[1])
            y = int(strings[2])
            if not self.checkPositionValid(x, y):
                return 'out of bounds'
            return self.flag(x, y)
        if (strings[0] == 'unflag'):
            x = int(strings[1])
            y = int(strings[2])
            if not self.checkPositionValid(x, y):
                return 'out of bounds'
            return self.unflag(x, y)
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
                return self.isSuccess()

    def isSuccess(self):
        if self.flagNum != self.mineNum:
            return False
        for y in range(self.field.height):
            for x in range(self.field.width):
                if self.field.status[y][x] == -1 and self.field.flagged[y][x] == False:
                    return False
                if self.field.status[y][x] != -1 and self.field.flagged[y][x] == True:
                    return False
        return True

    def flag(self, x, y):
        if self.field.opened[y][x] == False and self.field.flagged[y][x] ==  False:
            self.field.flagged[y][x] = True
            self.flagNum = self.flagNum + 1
            return str(x) + self.space + str(y) + self.space + 'flagged'
        else:
            return None

    def unflag(self, x, y):
        if self.field.opened[y][x] == False and self.field.flagged[y][x] == True:
            self.field.flagged[y][x] = False
            self.flagNum = self.flagNum - 1
            return str(x) + self.space + str(y) + self.space + 'unflagged'
        else:
            return None
 

    
    
    def peek(self, x, y):
        if x < 0 or x >= self.field.width or y < 0 or y >= self.field.height:
            return 'out of bounds'
        if self.field.flagged[y][x] == True:
            return 'flagged'
        #if self.field.opened[y][x] == False:
        #    return 'unexplored'    
        if self.field.status[y][x] < 0:
            return 'b'
        return str(self.field.status[y][x])



    def createMineField(self, height, width, numOfMines):
        self.field = MineField(height, width) 
        self.mineNum = numOfMines
        d = DeployMines(self.field, numOfMines)
        d.deployField()
        return 'created minefield ' + str(width) + ' x ' + str(height) + ' with ' + str(numOfMines)+' mines'

    def pokeOpenedMine(self, x, y):
        num = self.field.status[y][x]
        numflag = 0
        pos = set()
        if x + 1 < self.field.width:
            if self.field.flagged[y][x + 1] == True:
                numflag = numflag + 1
            elif self.field.opened[y][x + 1] == False:
                pos.add((x+1, y))

        if x - 1 >= 0:
            if self.field.flagged[y][x - 1] == True:
                numflag = numflag + 1
            elif self.field.opened[y][x - 1] == False:
                pos.add((x-1, y))
        if y - 1 >= 0:
            if self.field.flagged[y - 1][x] == True:
                numflag = numflag + 1
            elif self.field.opened[y - 1][x] == False:
                pos.add((x, y - 1))

        if y + 1 < self.field.height:
            if self.field.flagged[y + 1][x] == True:
                numflag = numflag + 1
            elif self.field.opened[y + 1][x] == False:
                pos.add((x, y + 1))

        if y + 1 < self.field.height and x + 1 < self.field.width:
            if self.field.flagged[y + 1][x + 1] == True:
                numflag = numflag + 1
            elif self.field.opened[y + 1][x + 1] == False:
                pos.add((x + 1, y + 1))

        if y + 1 < self.field.height and x - 1 >= 0:
            if self.field.flagged[y + 1][x - 1] == True:
                numflag = numflag + 1
            elif self.field.opened[y + 1][x - 1] == False:
                pos.add((x - 1, y + 1))

        if y - 1 >= 0 and x + 1 < self.field.width:
            if self.field.flagged[y - 1][x + 1] == True:
                numflag = numflag + 1
            elif self.field.opened[y - 1][x + 1] == False:
                pos.add((x + 1, y - 1))

        if y - 1 >= 0 and x - 1 >= 0:
            if self.field.flagged[y - 1][x - 1] == True:
                numflag = numflag + 1
            elif self.field.opened[y - 1][x - 1] == False:
                pos.add((x - 1, y - 1))

        totalPos = set() 
        if numflag == num:
            for (x, y) in pos:
                totalPos = totalPos | self.poke(x, y)
            return totalPos 
        else:
            return totalPos 





    def poke(self, x, y):
        pos =  set()
        if self.field.status[y][x] == -1 :
            pos.add((x, y))
            self.field.opened[y][x] = True
            return pos 
        else:
            if self.field.flagged[y][x] == True:
                return pos
            if self.field.opened[y][x] == True:
                return self.pokeOpenedMine(x, y)
            else:
                pos.add((x,y))
                queue = deque()
                if self.field.status[y][x] == 0:
                    queue.append((x,y))
                while len(queue) > 0:
                    p = queue.pop();
                    px = p[0]
                    py = p[1]
                    if self.checkPositionValid(px - 1, py):
                        if self.field.opened[py][px - 1] == False:
                            pos.add((px - 1, py))
                            self.field.opened[py][px - 1] = True
                            if self.field.status[py][px - 1] == 0:
                                queue.append((px - 1, py))
                    if self.checkPositionValid(px + 1, py):
                        if self.field.opened[py][px + 1] == False:
                            pos.add((px + 1, py))
                            self.field.opened[py][px + 1] = True
                            if self.field.status[py][px + 1] == 0:
                                queue.append((px + 1, py))
                    if self.checkPositionValid(px, py - 1):
                        if self.field.opened[py - 1][px] == False:
                            pos.add((px, py - 1))
                            self.field.opened[py - 1][px] = True
                            if self.field.status[py - 1][px] == 0:
                                queue.append((px, py - 1))
                    if self.checkPositionValid(px, py + 1):
                        if self.field.opened[py + 1][px] == False:
                            pos.add((px, py + 1))
                            self.field.opened[py + 1][px] = True
                            if self.field.status[py + 1][px] == 0:
                                queue.append((px, py + 1))
                    if self.checkPositionValid(px + 1, py + 1):
                        if self.field.opened[py + 1][px + 1] == False:
                            pos.add((px + 1, py + 1))
                            self.field.opened[py + 1][px + 1] = True
                            if self.field.status[py + 1][px + 1] == 0:
                                queue.append((px + 1, py + 1))
                    if self.checkPositionValid(px + 1, py - 1):
                        if self.field.opened[py - 1][px + 1] == False:
                            pos.add((px + 1, py - 1))
                            self.field.opened[py - 1][px + 1] = True
                            if self.field.status[py - 1][px + 1] == 0:
                                queue.append((px + 1, py - 1))
                    if self.checkPositionValid(px - 1, py - 1):
                        if self.field.opened[py - 1][px - 1] == False:
                            pos.add((px - 1, py - 1))
                            self.field.opened[py - 1][px - 1] = True
                            if self.field.status[py - 1][px - 1] == 0:
                                queue.append((px - 1, py - 1))
                    if self.checkPositionValid(px - 1, py + 1):
                        if self.field.opened[py + 1][px - 1] == False:
                            pos.add((px - 1, py + 1))
                            self.field.opened[py + 1][px - 1] = True
                            if self.field.status[py + 1][px - 1] == 0:
                                queue.append((px - 1, py + 1))
                        
                #return self.pokeOutPut(pos)
                return pos

    def pokeOutPut(self, pos):
        out = [] 
        for (x, y) in pos :
            if self.field.opened[y][x] == False:
                self.field.opened[y][x] = True
            out.append(str(x) + self.space + str(y) + self.space + 'opened as' + self.space + str(self.field.status[y][x]))
        return out

    def checkPositionValid(self, x, y):
        if x < 0 or y < 0 or x >= self.field.width or y >= self.field.height:
            return False
        return True


