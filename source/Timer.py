import time
class Timer:
    def __init__(self):
        self.startTime = None 
        self.endTime = None 
        self.totalTime = None 
        self.timerStarted = False
        self.timerEnded = False

    def start(self):
        self.timerStarted = True
        self.startTime = time.time()
        self.totalTime = 0
        
    def end(self):
        self.timerEnded = True
        self.endTime = time.time()
        self.totalTime = self.totalTime + self.endTime - self.startTime

    def pause(self):
        if self.isTimerStarted() == False:
            return
        curTime = time.time()
        self.totalTime = self.totalTime + curTime - self.startTime
        self.startTime = 0

    def resume(self):
        if self.isTimerPaused() == True and self.isTimerStarted() == True:
            self.startTime = time.time();
        else:
            return

    def getTotalTime(self):
        return self.totalTime


    def isTimerPaused(self):
        if self.startTime == 0:
            return True
        else:
            return False

    def isTimerStarted(self):
        return self.timerStarted
    
    def isTimerEnded(self):
        return self.timerEnded
