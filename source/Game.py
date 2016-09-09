import sys
from MineShell.MineShell import MineShell
from Window import Window
from Record import Record
from Mine import Mine
from Timer import Timer

class Game:
    def __init__(self, stdscr, width, height, num):
        self.width = width
        self.height = height
        self.num = num
        self.scr = stdscr
        self.fileName = str(width) + 'X' + str(height) + 'with' + str(num) + 'mines'
        self.isPaused = False
        self.record = None
        self.mine = None
        self.timer = None
        self.mineWin = None
        self.startTime = None

    def start(self):
        shell = MineShell()
        self.timer = Timer()
        createField = 'minefield ' + str(self.width) + ' ' + str(self.height) + ' ' + str(self.num)
        shell.getInput(createField)
        window = Window(self.scr)
        self.mineWin, log, panel, record = window.drawLayout(self.width, self.height)
        self.record = Record(record)
        self.mine = Mine(self.mineWin, shell)
        self.mine.drawUndeployedMineField()
        return self.mine, log, panel, self.record

    def pause(self):
        self.timer.pause()
        self.mine.drawUndeployedMineField()
        self.mine.disablePoke()
        return

    def resume(self):
        self.timer.resume()
        self.record.eraseRecord()
        self.mine.drawUndeployedMineField()
        self.mine.drawPokedMineField()
        self.mine.enablePoke()
        return

    def restart(self):
        self.record.eraseRecord()
        shell = MineShell()
        self.timer = Timer()
        createField = 'minefield ' + str(self.width) + ' ' + str(self.height) + ' ' + str(self.num)
        shell.getInput(createField)
        self.mine = Mine(self.mineWin, shell)
        self.mine.drawUndeployedMineField()
        return
    
    def poke(self, y, x):
        if self.timer.isTimerStarted() == False:
            self.timer.start()
        return self.mine.pokeMineField(y, x)

    def flag(self, y, x):
        alreadyFlagged = self.mine.flagMineField(y, x)
        if alreadyFlagged:
            self.mine.unflagMineField(y, x)

    def checkWin(self):
        return self.mine.shell.getInput('query success')

    def checkLose(self):
        return self.mine.shell.getInput('query failure')
    
    def status(self):
        flags = self.mine.shell.getInput('query flags')
        mines = self.mine.shell.getInput('query mines')
        return flags, mines

    def exit(self):
        sys.exit(0) 
        return

    def addNewRecord(self):
        time = self.timer.getTotalTime()
        self.record.addNewRecord(self.fileName, time)

    def displayRecord(self):
        if not self.checkWin() and not checkLose():
            self.pause()
        self.record.displayRecords(self.fileName, 0)
        return

    def displayGameOver(self, success):
        self.timer.end()
        self.mine.displayGameOver(success)
        self.mine.disablePoke()
        return

