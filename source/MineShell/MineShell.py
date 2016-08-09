from MineField.MineField import MineField
#from Deploy import Deploy 
from queue import Queue
class MineShell:
    def __init__(self):
        self.field = None
        self.space = ' '
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
        
    
    
    def peek(self, x, y):
        if x < 0 or x >= self.field.width or y < 0 or y >= self.field.height:
            return 'out of bounds'
        if self.field.flagged[y][x] == True:
            return 'flagged'
        if self.field.opened[y][x] == False:
            return 'unexplored'    
        return str(self.field.status[y][x])



    def createMineField(self, height, width, numOfMines):
        self.field = MineField(height, width) 
        #self.deploy = Deploy(numOfMines, sefl.field)
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
                        if not (px - 1, py - 1) in pos:
                            pos.add((px - 1, py - 1))
                            self.field.opened[py - 1][px - 1] = True
                            if self.field.status[py - 1][px - 1] == 0:
                                queue.put((px - 1, py - 1))
                    if py + 1 < self.field.height:
                        if not (px - 1, py + 1) in pos:
                            pos.add((px - 1, py + 1))
                            self.field.opened[py + 1][px - 1] = True
                            if self.field.status[py + 1][px - 1] == 0:
                                queue.put((px - 1, py + 1))
                    if not (px - 1, py) in pos:
                        pos.add((px - 1, py))
                        self.field.opened[py][px - 1] = True
                        if self.field.status[py][px - 1] == 0:
                            queue.put((px - 1, py))
                if py - 1 >= 0:
                    if not (px, py - 1) in pos:
                        pos.add((px, py - 1))
                        self.field.opened[py - 1][px] = True
                        if self.field.status[py - 1][px] == 0:
                            queue.put((px, py - 1))
                if py + 1 < self.field.height:
                    if not (px, py + 1) in pos:
                        pos.add((px, py + 1))
                        self.field.opened[py + 1][px] = True
                        if self.field.status[py + 1][px] == 0:
                            queue.put((px, py + 1))
                if px + 1 < self.field.width:
                    if py - 1 >= 0:
                        if not (px + 1, py - 1) in pos:
                            pos.add((px + 1, py - 1))
                            self.field.opened[py - 1][px + 1] = True
                            if self.field.status[py - 1][px + 1] == 0:
                                queue.put((px + 1, py - 1))
                    if py + 1 < self.field.height:
                        if not (px + 1, py + 1) in pos:
                            pos.add((px + 1, py + 1))
                            self.field.opened[py + 1][px + 1] = True
                            if self.field.status[py + 1][px + 1] == 0:
                                queue.put((px + 1, py + 1))
                    if not (px + 1, py) in pos:
                        pos.add((px + 1, py))
                        self.field.opened[py][px + 1] = True
                        if self.field.status[py][px + 1] == 0:
                            queue.put((px + 1, py))
        return self.pokeOutPut(pos)

    def pokeOutPut(self, pos):
        out = [] 
        for (x, y) in pos :
            out.append(str(x) + self.space + str(y) + self.space + 'opened as' + self.space + str(self.field.status[x][y]))
        return out



