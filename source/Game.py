import sys
from types import *
import curses
import Consts
from MineShell.MineShell import MineShell
from Window import Window
from Record import Record
from GameField import GameField 
from Timer import Timer
from ClockUpdater import ClockUpdater

class Game:
    def __init__(self, stdscr, width, height, num):
        self.width = width
        self.height = height
        self.num = num
        self.scr = stdscr
        self.fileName = str(width) + 'X' + str(height) + 'with' + str(num) + 'mines'
        self.success = None
        self.gameOver = None 
        self.record = None
        self.mine = None
        self.timer = None
        self.mineWin = None
        self.startTime = None
        self.totalTime = None
        self.clock = None

    def start(self):
        self.success = False
        self.gameOver = False
        self.setCurses()
        shell = MineShell()
        self.timer = Timer()
        Consts.TIMER = self.timer
        createField = 'minefield ' + str(self.width) + ' ' + str(self.height) + ' ' + str(self.num)
        shell.getInput(createField)
        window = Window(self.scr)
        layout = window.drawLayout(self.width, self.height)
        if layout == None:
            curses.endwin()
            print("The window is too small to display the Game field")
            print("Please increase the window size or decrease the font size")
            sys.exit(0);
        self.mineWin, log, panel, record = layout 
        self.record = Record(record)
        self.mine = GameField(self.mineWin, shell)
        self.mine.drawUndeployedMineField()
        Consts.PANEL = panel
        self.clock = ClockUpdater()
        self.clock.daemon = True
        self.clock.start()
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
        if self.isGameOver():
            self.displayGameOver(self.success)
        else:
            self.mine.drawPokedMineField()
            self.mine.enablePoke()
        return

    def restart(self):
        self.success = False
        self.gameOver = False
        self.record.eraseRecord()
        shell = MineShell()
        self.timer = Timer()
        Consts.TIMER = self.timer
        createField = 'minefield ' + str(self.width) + ' ' + str(self.height) + ' ' + str(self.num)
        shell.getInput(createField)
        self.mine = GameField(self.mineWin, shell)
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
        self.totalTime = self.timer.getTotalTime()
        self.record.addNewRecord(self.fileName, self.totalTime)

    def displayRecord(self):
        if not self.checkWin() and not self.checkLose():
            self.pause()
            self.record.displayRecords(self.fileName, None)
        elif self.checkWin():
            self.record.displayRecords(self.fileName, int(self.totalTime))
        elif self.checkLose():
            self.record.displayRecords(self.fileName, None)
        return

    def displayGameOver(self, success):
        self.mine.displayGameOver(success)
        self.mine.disablePoke()
    
    def isGameOver(self):
        return self.gameOver

    def gameWin(self):
        if self.isGameOver():
            return
        self.success = True
        self.gameOver = True
        self.timer.end()
        self.displayGameOver(True)
        self.addNewRecord()
        self.displayRecord()
        return

    def gameLose(self):
        if self.isGameOver():
            return
        self.timer.end()
        self.gameOver = True
        self.displayGameOver(False)
        return
        

    def setCurses(self):
        self.scr.refresh()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.mousemask(-1)
        curses.mouseinterval(0)
        curses.curs_set(0)
