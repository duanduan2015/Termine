import os.path
from datetime import date
import curses
class Record:
    def __init__(self, recordWin):
        self.win = recordWin

    def displayRecords(self, fileName, highLightTime):
        fileIsExist = os.path.isfile(fileName)
        if fileIsExist:
            recordsFile = open(fileName, "r")
        else:
            recordsFile = open(fileName, "w")
            recordsFile.close()
            recordsFile = open(fileName, "r")
        self.drawRecordWindow()
        starty = 4 
        attr = curses.A_BOLD | curses.color_pair(2)
        line = recordsFile.readline()
        records = []
        highLighted = False
        if line != '':
            records = line.split('#')
            for r in records:
                if r == '':
                    continue
                strings = r.split(' ')
                highLight = curses.A_BOLD | curses.color_pair(4)
                if int(strings[1]) == highLightTime and highLighted == False:
                    highLighted = True
                    self.win.addstr(starty, 2, strings[0], highLight)
                    self.win.addstr(starty, 12, strings[1] + 's', highLight)
                else:
                    self.win.addstr(starty, 2, strings[0], attr)
                    self.win.addstr(starty, 12, strings[1] + 's', attr)
                starty = starty + 1
        recordsFile.close()
        star = ord('*') | attr
        self.win.border(star, star, star, star, star, star, star, star)
        self.win.refresh()
        return
        
    def addNewRecord(self, fileName, totalTime):
        fileIsExist = os.path.isfile(fileName)
        if fileIsExist:
            recordsFile = open(fileName, "r")
        else:
            recordsFile = open(fileName, "w")
            recordsFile.close()
            recordsFile = open(fileName, "r")
        time = int(totalTime)
        today = date.today().strftime("%d/%m/%y")
        records = [] 
        line = recordsFile.readline()
        if line != '':
            oldRecords = line.split('#')
            for x in range(len(oldRecords) - 1):
                records.append(oldRecords[x])
            added = False
            for x in range(len(records)):
                r = records[x].split(' ')
                t = int(r[1])
                if t > time:
                    newLine = today + ' ' + str(time)
                    records.insert(x, newLine)
                    added = True
                    break
            if not added:
                newLine = today + ' ' + str(time)
                records.append(newLine)
        else:
            newLine = today + ' ' + str(time)
            records.append(newLine)
        recordsFile.close()
        recordsFile = open(fileName, 'w+')
        newFile = '' 
        num = 0
        for line in records:
            num = num + 1
            newFile = newFile + line + ' ' + '#'
            if num == 10:
                break

        recordsFile.write(newFile)
        recordsFile.close()

    def drawRecordWindow(self):
        attr = curses.A_BOLD | curses.color_pair(2)
        height, width = self.win.getmaxyx()
        star = ord('*') | attr
        self.win.border(star, star, star, star, star, star, star, star)
        self.win.addstr(1, 9, 'RECORDS', attr)
        self.win.addstr(2, 2, 'Date', attr)
        self.win.addstr(2, 12, 'Time', attr)

    def eraseRecord(self):
        self.win.erase()
        self.win.refresh()
