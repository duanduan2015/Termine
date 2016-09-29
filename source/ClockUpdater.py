import threading 
import curses
import time
import Consts
class ClockUpdater(threading.Thread):
    def run(self):
        total = 0
        maxLen = 0
        while True:
            attr = curses.A_STANDOUT | curses.color_pair(3) | curses.A_BOLD
            if not Consts.TIMER.isTimerStarted():
                total = 0.0
                maxLen = 0
            elif not Consts.TIMER.isTimerPaused() and not Consts.TIMER.isTimerEnded():
                total = total + 0.1
            msg = str(round(total, 1))
            if maxLen < len(msg) + 1:
                maxLen = len(msg) + 1
            Consts.PANEL.addstr(1, 56 + maxLen, " ", attr)
            Consts.PANEL.addstr(1, 56, msg, attr)
            Consts.PANEL.addstr(1, 56 + len(msg), "s", attr)

            Consts.PANEL.refresh()
            time.sleep(0.1)
        
