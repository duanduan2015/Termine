import time
import threading 
import curses
import Consts

class ClockUpdater(threading.Thread):
    def run(self):
        Consts.totalTime = 0
        maxLen = 0
        while True:
            attr = curses.A_STANDOUT | curses.color_pair(3) | curses.A_BOLD
            if not Consts.TIMER.isTimerStarted():
                Consts.totalTime = 0.0
                maxLen = 0
            elif not Consts.TIMER.isTimerPaused() and not Consts.TIMER.isTimerEnded():
                Consts.totalTime = Consts.totalTime + 0.1
            msg = str(round(Consts.totalTime, 1))
            if maxLen < len(msg) + 1:
                maxLen = len(msg) + 1
            Consts.PANEL.addstr(1, 56 + maxLen, " ", attr)
            Consts.PANEL.addstr(1, 56, msg, attr)
            Consts.PANEL.addstr(1, 56 + len(msg), "s", attr)

            Consts.PANEL.refresh()
            time.sleep(0.1)

class Timer:
    def __init__(self):
        self.timerStarted = False
        self.timerEnded = False
        self.timerPaused = False

    def start(self):
        self.timerStarted = True
        
    def end(self):
        self.timerEnded = True

    def pause(self):
        if self.isTimerStarted() == False:
            return
        else:
            self.timerPause = True

    def resume(self):
        if self.isTimerPaused() == True and self.isTimerStarted() == True:
            self.timerPaused = False
        else:
            return

    def getTotalTime(self):
        return Consts.totalTime


    def isTimerPaused(self):
        return self.timerPaused

    def isTimerStarted(self):
        return self.timerStarted
    
    def isTimerEnded(self):
        return self.timerEnded
