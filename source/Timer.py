import time
class Timer:
    def __init__(self):
        self.startTime = None 
        self.endTime = None 
        self.pauseStartTime = None 
        self.pauseStopTime = None
        self.totalTime = None 

    def start(self):
        self.startTime = time.time()
        self.pauseStartTime = 0
        self.pauseStopTime = 0
        self.totalTime = 0
        
    def end(self):
        self.endTime = time.time()
        self.totalTime = self.totalTime + self.endTime - self.startTime

    def pause(self):
        if self.isTimerStarted() == False:
            return
        curTime = time.time()
        self.totalTime = self.totalTime + curTime - self.startTime
        self.startTime = 0

    def resume(self):
        self.startTime = time.time();

    def getTotalTime(self):
        return self.totalTime

    def isTimerStarted(self):
        if self.startTime == None:
            return False
        else:
            return True


    

