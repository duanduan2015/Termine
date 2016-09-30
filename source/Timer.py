import time
import threading 
import curses
import Global

class ClockUpdater(threading.Thread):
    def run(self):
        Global.totalTime = 0
        maxLen = 0
        while True:
            attr = curses.A_STANDOUT | curses.color_pair(3) | curses.A_BOLD
            if not Global.timer.isTimerStarted():
                Global.totalTime = 0.0
                maxLen = 0
            elif not Global.timer.isTimerPaused() and not Global.timer.isTimerEnded():
                Global.totalTime = Global.totalTime + 0.1
            msg = str(round(Global.totalTime, 1))
            if maxLen < len(msg) + 1:
                maxLen = len(msg) + 1
            Global.panel.addstr(1, 76 + maxLen, " ", attr)
            Global.panel.addstr(1, 76, msg, attr)
            Global.panel.addstr(1, 76 + len(msg), "s", attr)

            Global.panel.refresh()
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
            self.timerPaused = True

    def resume(self):
        if self.isTimerPaused() == True and self.isTimerStarted() == True:
            self.timerPaused = False
        else:
            return

    def getTotalTime(self):
        return Global.totalTime


    def isTimerPaused(self):
        return self.timerPaused

    def isTimerStarted(self):
        return self.timerStarted
    
    def isTimerEnded(self):
        return self.timerEnded
