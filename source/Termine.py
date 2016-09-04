#!/usr/bin/env python3
import time
from datetime import date
import curses
import Consts
import sys
import os.path
from curses import wrapper
from MineShell.MineShell import MineShell


def Main(stdscr):
    setCursesFeatures()
    if sys.argv[1] == 'help':
        curses.endwin()
        helpInfo()
        sys.exit(1) 
    mineFieldWidth, mineFieldHeight, numMines, mode = parseArgs(sys.argv)
    shell = MineShell()
    createField = 'minefield ' + str(mineFieldWidth) + ' ' + str(mineFieldHeight) + ' ' + str(numMines)
    out = shell.getInput(createField)
    stdscr.refresh()
    mine, log, panel, record = drawWindowLayout(stdscr, mineFieldWidth, mineFieldHeight)
    drawUndeployedMineField(mine, mineFieldWidth, mineFieldHeight)
    start_time = 0
    end_time = 0
    start_pause = 0
    end_pause = 0
    pause_total_time = 0
    fileName = str(mineFieldWidth) + 'X' + str(mineFieldHeight) + 'with' + str(numMines) + 'mines'
    restart = True
    while True:
        queryGameStatus(shell, stdscr)
        event = stdscr.getch()
        if event == ord("q"): break 
        if event == ord("R"):   #display Records
            success = checkSuccess(shell)
            failure = checkFailure(shell)
            if not success and not failure:
                start_pause = pauseGame(mine, mineFieldWidth, mineFieldHeight)
                displayRecords(record, fileName, 0)
            else:
                displayRecords(record, fileName, 0)
                
            continue

        if event == ord("c"):   #continue game
            record.erase()
            record.refresh()
            success = checkSuccess(shell)
            failure = checkFailure(shell)
            if not success and not failure:
                end_pause = continueGame(shell, mine, mineFieldWidth, mineFieldHeight)
                pause_total_time = end_pause - start_pause
                start_pause = 0
                end_pause = 0
            else:
                if success:
                    displayGameOver(shell, stdscr, mine, mineFieldWidth, mineFieldHeight, True)
                else:
                    displayGameOver(shell, stdscr, mine, mineFieldWidth, mineFieldHeight, False)

            continue

        if event == ord("p"):   #pause game
            if start_time == 0 or end_time != 0 or start_pause != 0:
                continue
            else:
                start_pause = pauseGame(mine, mineFieldWidth, mineFieldHeight)
            continue
        if event == ord("r"):   #restart game
            restart = True
            record.clear()
            record.refresh()
            shell = restartNewGame(mine, mineFieldWidth, mineFieldHeight, numMines)
            start_time = 0
            end_time = 0
            start_pause = 0
            end_pause = 0
            pause_total_time = 0 
            continue
        if event == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_PRESSED :
                if start_time == 0:
                    start_time = time.time()
                pokeMineField(stdscr, my, mx, shell, mine)
            elif bstate & curses.BUTTON3_PRESSED:
                alreadyFlagged = flagMineField(my, mx, shell, mine)
                if alreadyFlagged:
                    unflagMineField(my, mx, shell, mine)
            if restart == True:
                if checkSuccess(shell):
                    restart = False
                    end_time = displayGameOver(shell, stdscr, mine, mineFieldWidth, mineFieldHeight, True)
                    totalTime = end_time - start_time - pause_total_time
                    addNewRecord(fileName, totalTime)
                    displayRecords(record, fileName, int(totalTime))

                elif checkFailure(shell):
                    restart = False
                    end_time = displayGameOver(shell, stdscr, mine, mineFieldWidth, mineFieldHeight, False)
            
            
def addNewRecord(fileName, totalTime):
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

def displayRecords(record, fileName, highLightTime):
    fileIsExist = os.path.isfile(fileName)
    if fileIsExist:
        recordsFile = open(fileName, "r")
    else:
        recordsFile = open(fileName, "w")
        recordsFile.close()
        recordsFile = open(fileName, "r")
    drawRecordWindow(record)
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
                record.addstr(starty, 2, strings[0], highLight)
                record.addstr(starty, 12, strings[1] + 's', highLight)
            else:
                record.addstr(starty, 2, strings[0], attr)
                record.addstr(starty, 12, strings[1] + 's', attr)
            starty = starty + 1
    recordsFile.close()
    star = ord('*') | attr
    record.border(star, star, star, star, star, star, star, star)
    record.refresh()
    return

def drawRecordWindow(record):
    attr = curses.A_BOLD | curses.color_pair(2)
    height, width = record.getmaxyx()
    star = ord('*') | attr
    record.border(star, star, star, star, star, star, star, star)
    record.addstr(1, 9, 'RECORDS', attr)
    record.addstr(2, 2, 'Date', attr)
    record.addstr(2, 12, 'Time', attr)


def pauseGame(mineWin, width, height):
    pauseBeginTime = time.time()
    drawUndeployedMineField(mineWin, width, height)
    return pauseBeginTime

def continueGame(shell, mineWin, width, height):
    pauseEndTime = time.time()
    drawUndeployedMineField(mineWin, width, height)
    drawPokedMineField(shell, mineWin, width, height)
    return pauseEndTime


def restartNewGame(mine, mineFieldWidth, mineFieldHeight, numMines):
    shell = MineShell()
    createField = 'minefield ' + str(mineFieldWidth) + ' ' + str(mineFieldHeight) + ' ' + str(numMines)
    out = shell.getInput(createField)
    drawUndeployedMineField(mine, mineFieldWidth, mineFieldHeight)
    return shell


def parseArgs(args):
    if args[1] == 'easy':
        return (8, 8, 10, 'easy')
    if args[1] == 'medium':
        return (16, 16, 40, 'medium')
    if args[1] == 'hard':
        return (30, 16, 99, 'hard')
    if args[1] == 'customized':
        width = int(args[2])
        height = int(args[3])
        num = int(args[4])
        return (width, height, num, 'customized')

def checkSuccess(shell):
    return shell.getInput('query success')

def checkFailure(shell):
    return shell.getInput('query failure')

def queryGameStatus(shell, stdscr):
    flags = shell.getInput('query flags')
    mines = shell.getInput('query mines')

        
def unflagMineField(y, x, shell, mineWin):
    starty, startx = mineWin.getbegyx()
    unitx = Consts.numhlines + 1
    unity = Consts.numvlines + 1
    y, x = y - starty, x - startx
    if x % (unitx)  == 0 or y % (unity) == 0:
        return
    fieldx = (int)(x / unitx)
    fieldy = (int)(y / unity)
    flag = 'unflag' + ' ' + str(fieldx) + ' ' + str(fieldy)
    out = shell.getInput(flag)
    if out == None:
        return
    wx = fieldx * unitx + Consts.numhlines - 1
    wy = fieldy * unity + Consts.numvlines
    mineWin.addch(wy, wx, ord(' '), curses.A_REVERSE)
    mineWin.addch(wy, wx - 1, ord(' '), curses.A_REVERSE)
    mineWin.addch(wy, wx + 1, ord(' '), curses.A_REVERSE)
    mineWin.refresh()


def flagMineField(y, x, shell, mineWin):
    starty, startx = mineWin.getbegyx()
    unitx = Consts.numhlines + 1
    unity = Consts.numvlines + 1
    y, x = y - starty, x - startx
    if x % (unitx)  == 0 or y % (unity) == 0:
        return
    fieldx = (int)(x / unitx)
    fieldy = (int)(y / unity)
    flag = 'flag' + ' ' + str(fieldx) + ' ' + str(fieldy)
    out = shell.getInput(flag)
    if out == None:
        return True 
    wx = fieldx * unitx + Consts.numhlines - 1
    wy = fieldy * unity + Consts.numvlines
    attr = curses.A_BOLD | curses.color_pair(7) | curses.A_REVERSE
    mineWin.addstr(wy, wx, '$', attr)
    mineWin.addch(wy, wx - 1, ord(' '), attr)
    mineWin.addch(wy, wx + 1, ord(' '), attr)
    mineWin.refresh()
    return False 
def peekMineField(y, x, shell, mineWin):
    starty, startx = mineWin.getbegyx()
    unitx = Consts.numhlines + 1
    unity = Consts.numvlines + 1
    y, x = y - starty, x - startx
    if x % (unitx)  == 0 or y % (unity) == 0:
        return
    fieldx = (int)(x / unitx)
    fieldy = (int)(y / unity)
    peek = 'peek' + ' ' + str(fieldx) + ' ' + str(fieldy)
    num = shell.getInput(peek)
    wx = fieldx * unitx + Consts.numhlines - 1
    wy = fieldy * unity + Consts.numvlines
    mineWin.addstr(wy, wx, num)
    mineWin.addch(wy, wx - 1, ord(' '))
    mineWin.addch(wy, wx + 1, ord(' '))
    mineWin.refresh()


def pokeMineField(stdscr, y, x, shell, mineWin):
    starty, startx = mineWin.getbegyx()
    y, x = y - starty, x - startx
    unitx = Consts.numhlines + 1
    unity = Consts.numvlines + 1
    if x % (unitx)  == 0 or y % (unity) == 0:
        return
    fieldx = (int)(x / unitx)
    fieldy = (int)(y / unity)
    poke = 'poke' + ' ' + str(fieldx) + ' ' + str(fieldy)
    pokeOut = shell.getInput(poke)
    if isinstance(pokeOut, list):
        openedx = []
        openedy = []
        nums = []
        for out in pokeOut:
            string = out.split(' ')
            minex = int(string[0])
            miney = int(string[1])
            wx = minex * unitx + Consts.numhlines - 1
            wy = miney * unity + Consts.numvlines
            openedx.append(int(wx))
            openedy.append(int(wy))
            nums.append(string[4])
            number = 0
        for i in range(len(nums)):
            if len(nums[i]) > 1:
                attr = curses.color_pair(7) | curses.A_STANDOUT
                mineWin.addstr(openedy[i], openedx[i], ':(' , attr) 
                mineWin.addch(openedy[i], openedx[i] - 1, ord(' '), attr)
                displayGameOver(shell, stdscr, mineWin, shell.field.width, shell.field.height, False)
                return 
            else:
                number = int(nums[i])
                if number >= 5:
                    number = 5 
            attr = 0
            if number == 0:
                nums[i] = ' '
            else:
                attr = curses.A_BOLD | curses.color_pair(number + 1) 
            mineWin.addch(openedy[i], openedx[i], ord(nums[i]), attr) 
            mineWin.addch(openedy[i], openedx[i] - 1, ord(' '), attr)
            mineWin.addch(openedy[i], openedx[i] + 1, ord(' '), attr)
        mineWin.refresh()
    else:
        return
    mineWin.refresh()

def setCursesFeatures():
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

def drawPokedMineField(shell, mineWin, width, height):
    windowHeight, windowWidth = mineWin.getmaxyx()
    fieldWidth = (Consts.numhlines + 1) * width
    fieldHeight = (Consts.numvlines + 1) * height
    starty, startx = 0, 0
    xindex, yindex = startx, starty
    xend = xindex + fieldWidth
    yend = yindex + fieldHeight 

    halfx = (Consts.numhlines + 1) / 2
    halfy = (Consts.numvlines + 1) / 2

    for x in range (startx, xend):
        for y in range (starty, yend):
            disx = x - startx
            disy = y - starty
            if (disx % halfx == 0) and (disx / halfx) % 2 != 0:
                if (disy % halfy == 0) and (disy / halfy) % 2 != 0:
                    fieldx = int((disx / halfx - 1) / 2)
                    fieldy = int((disy / halfy - 1) / 2)
                    if shell.field.opened[fieldy][fieldx] == True:
                        number = shell.field.status[fieldy][fieldx]
                        attr = curses.A_BOLD | curses.color_pair(number + 1) 
                        if number == 0:
                            number = ' '
                        else:
                            number = str(number)
                        mineWin.addstr(y, x, number, attr) 
                        mineWin.addch(y, x - 1, ord(' '), attr)
                        mineWin.addch(y, x + 1, ord(' '), attr)
                    elif shell.field.flagged[fieldy][fieldx] == True:
                        attr = curses.A_BOLD | curses.color_pair(7) | curses.A_REVERSE
                        mineWin.addstr(y, x, '$', attr)
                        mineWin.addch(y, x - 1, ord(' '), attr)
                        mineWin.addch(y, x + 1, ord(' '), attr)
    mineWin.refresh()

def drawMineFieldFrame(mineWin, width, height, color):
    windowHeight, windowWidth = mineWin.getmaxyx()
    fieldWidth = (Consts.numhlines + 1) * width
    fieldHeight = (Consts.numvlines + 1) * height
    starty, startx = 0, 0
    xindex, yindex = startx, starty
    xend = xindex + fieldWidth
    yend = yindex + fieldHeight 
    attr = curses.A_BOLD | color 
    mineWin.addch(starty, startx, curses.ACS_ULCORNER, attr)
    mineWin.addch(starty + (Consts.numvlines + 1) * height, startx, curses.ACS_LLCORNER, attr)
    mineWin.addch(starty, startx + (Consts.numhlines + 1) * width, curses.ACS_URCORNER, attr)
    mineWin.addch(starty + (Consts.numvlines + 1) * height, startx + (Consts.numhlines + 1) * width, curses.ACS_LRCORNER, attr)
    for x in range(xindex + 1, xend):
        if (x - startx) % (Consts.numhlines + 1) == 0:
            mineWin.addch(yindex, x, curses.ACS_TTEE, attr)
            for y in range(yindex + 1, yend):
                if (y - starty) % (Consts.numvlines + 1) != 0:
                    mineWin.addch(y, x, curses.ACS_VLINE, attr)
        else:
            mineWin.addch(yindex, x, curses.ACS_HLINE, attr)

    for x in range(xindex + 1, xend):
        if (x - startx) % (Consts.numhlines + 1) == 0:
            mineWin.addch(yend, x, curses.ACS_BTEE, attr)
        else:
            mineWin.addch(yend, x, curses.ACS_HLINE, attr)

    for y in range(yindex + 1, yend):
        if (y - starty) % (Consts.numvlines + 1) == 0:
            mineWin.addch(y, startx, curses.ACS_LTEE, attr)
            for x in range(xindex + 1, xend):
                if (x - startx) % (Consts.numhlines + 1) == 0:
                    mineWin.addch(y, x, curses.ACS_PLUS, attr)
                else:
                    mineWin.addch(y, x, curses.ACS_HLINE, attr)
        else:
            mineWin.addch(y, startx, curses.ACS_VLINE, attr)

    for y in range(yindex + 1, yend):
        if (y - starty) % (Consts.numvlines + 1) == 0:
            mineWin.addch(y, xend, curses.ACS_RTEE, attr)
        else:
            mineWin.addch(y, xend, curses.ACS_VLINE, attr)
    #mineWin.refresh()

def drawUndeployedMineField(mineWin, width, height):
    drawMineFieldFrame(mineWin, width, height, curses.color_pair(1))
    #windowHeight, windowWidth = mineWin.getmaxyx()
    #fieldWidth = (Consts.numhlines + 1) * width
    #fieldHeight = (Consts.numvlines + 1) * height
    #starty, startx = 0, 0
    #xindex, yindex = startx, starty
    #xend = xindex + fieldWidth
    #yend = yindex + fieldHeight 
    #attr = curses.A_BOLD | curses.color_pair(1)
    #mineWin.addch(starty, startx, curses.ACS_ULCORNER, attr)
    #mineWin.addch(starty + (Consts.numvlines + 1) * height, startx, curses.ACS_LLCORNER, attr)
    #mineWin.addch(starty, startx + (Consts.numhlines + 1) * width, curses.ACS_URCORNER, attr)
    #mineWin.addch(starty + (Consts.numvlines + 1) * height, startx + (Consts.numhlines + 1) * width, curses.ACS_LRCORNER, attr)
    #for x in range(xindex + 1, xend):
    #    if (x - startx) % (Consts.numhlines + 1) == 0:
    #        mineWin.addch(yindex, x, curses.ACS_TTEE, attr)
    #        for y in range(yindex + 1, yend):
    #            if (y - starty) % (Consts.numvlines + 1) != 0:
    #                mineWin.addch(y, x, curses.ACS_VLINE, attr)
    #    else:
    #        mineWin.addch(yindex, x, curses.ACS_HLINE, attr)

    #for x in range(xindex + 1, xend):
    #    if (x - startx) % (Consts.numhlines + 1) == 0:
    #        mineWin.addch(yend, x, curses.ACS_BTEE, attr)
    #    else:
    #        mineWin.addch(yend, x, curses.ACS_HLINE, attr)

    #for y in range(yindex + 1, yend):
    #    if (y - starty) % (Consts.numvlines + 1) == 0:
    #        mineWin.addch(y, startx, curses.ACS_LTEE, attr)
    #        for x in range(xindex + 1, xend):
    #            if (x - startx) % (Consts.numhlines + 1) == 0:
    #                mineWin.addch(y, x, curses.ACS_PLUS, attr)
    #            else:
    #                mineWin.addch(y, x, curses.ACS_HLINE, attr)
    #    else:
    #        mineWin.addch(y, startx, curses.ACS_VLINE, attr)

    #for y in range(yindex + 1, yend):
    #    if (y - starty) % (Consts.numvlines + 1) == 0:
    #        mineWin.addch(y, xend, curses.ACS_RTEE, attr)
    #    else:
    #        mineWin.addch(y, xend, curses.ACS_VLINE, attr)

    windowHeight, windowWidth = mineWin.getmaxyx()
    fieldWidth = (Consts.numhlines + 1) * width
    fieldHeight = (Consts.numvlines + 1) * height
    starty, startx = 0, 0
    xindex, yindex = startx, starty
    xend = xindex + fieldWidth
    yend = yindex + fieldHeight 
    halfx = (Consts.numhlines + 1) / 2
    halfy = (Consts.numvlines + 1) / 2

    for x in range (startx, xend):
        for y in range (starty, yend):
            disx = x - startx
            disy = y - starty
            if (disx % halfx == 0) and (disx / halfx) % 2 != 0:
                if (disy % halfy == 0) and (disy / halfy) % 2 != 0:
                    fieldx = int((disx / halfx - 1) / 2)
                    fieldy = int((disy / halfy - 1) / 2)
                    mineWin.addch(y, x, ord(' '), curses.A_REVERSE)
                    mineWin.addch(y, x + 1, ord(' '), curses.A_REVERSE)
                    mineWin.addch(y, x - 1, ord(' '), curses.A_REVERSE)
    mineWin.refresh()

def drawWindowLayout(stdscr, fwidth, fheight):
    height, width = stdscr.getmaxyx()
    heightDividor = (int)(height / 8)
    logColumns = 20
    paddingMineLog = 2 
    mineLines = 7 * heightDividor
    mineColumns = width - logColumns - paddingMineLog
    paddingTop = 3 
    windowHeight, windowWidth = mineLines, mineColumns
    fieldWidth = (Consts.numhlines + 1) * (fwidth + 1)
    fieldHeight = (Consts.numvlines + 1) * (fheight + 1)
    starty = (int)((windowHeight - fieldHeight) / 2) 
    startx = (int)((windowWidth - fieldWidth) / 2)
    recordWidth = 25 
    recordHeight = 16 
    recordBeginx = startx + fieldWidth // 2 - recordWidth // 2 - 2 
    recordBeginy = starty + paddingTop + fieldHeight // 2 - recordHeight // 2 - 2 
    recordWin = curses.newwin(recordHeight, recordWidth, recordBeginy, recordBeginx) 
    mineWin = curses.newwin(fieldHeight, fieldWidth, starty + paddingTop, startx)
    logLines = height - 3 
    logWin = curses.newwin(logLines, logColumns, 0, mineColumns + paddingMineLog)
    drawBorder(logWin, curses.color_pair(6))
    logWin.refresh()
    paddingMinePanel = 2
    panelLines = 3 
    panelColumns = width
    panelWin = curses.newwin(panelLines, panelColumns, height - panelLines, 0)
    drawBorder(panelWin, curses.color_pair(5))
    panelWin.refresh()
    return (mineWin, logWin, panelWin, recordWin)

def drawBorder(win, color):
    attr = color | curses.A_BOLD
    ls, rs = attr | curses.ACS_VLINE, attr | curses.ACS_VLINE
    ts, bs = attr | curses.ACS_HLINE, attr | curses.ACS_HLINE
    tl = attr | curses.ACS_ULCORNER
    tr = attr | curses.ACS_URCORNER
    bl = attr | curses.ACS_LLCORNER
    br = attr | curses.ACS_LRCORNER
    win.border(ls, rs, ts, bs, tl, tr, bl, br)

def displayGameOver(shell, stdscr, mineWin, width, height, success):
    end_time = time.time()
    fieldWidth = (Consts.numhlines + 1) * width
    fieldHeight = (Consts.numvlines + 1) * height
    xend = fieldWidth
    yend = fieldHeight 
    halfx = (Consts.numhlines + 1) / 2
    halfy = (Consts.numvlines + 1) / 2
    color = curses.color_pair(1)
    if success:
        color = curses.color_pair(3)
        drawMineFieldFrame(mineWin, width, height, curses.color_pair(3))
    else:
        drawMineFieldFrame(mineWin, width, height, curses.color_pair(7))
    for x in range (0, xend):
        for y in range (0, yend):
            disx = x
            disy = y
            if (disx % halfx == 0) and (disx / halfx) % 2 != 0:
                if (disy % halfy == 0) and (disy / halfy) % 2 != 0:
                    fieldx = int((disx / halfx - 1) / 2)
                    fieldy = int((disy / halfy - 1) / 2)
                    attr = 0
                    if shell.field.flagged[fieldy][fieldx] == False and shell.field.opened[fieldy][fieldx] == False:
                        num = shell.field.status[fieldy][fieldx]
                        shell.field.opened[fieldy][fieldx] = True
                        if num < 0:
                            if success:
                                num = '$'
                                attr = curses.A_STANDOUT | curses.color_pair(7)
                                mineWin.addstr(y, x, num, attr) 
                                mineWin.addch(y, x - 1, ord(' '), attr)
                                mineWin.addch(y, x + 1, ord(' '), attr)
                            else:
                                num = ':('
                                attr = curses.A_STANDOUT | curses.color_pair(7)
                                mineWin.addstr(y, x, num, attr) 
                                mineWin.addch(y, x - 1, ord(' '), attr)
                        else:
                            attr = curses.A_BOLD | curses.color_pair(num + 1) 
                            if num == 0:
                                num = ' '
                            else:
                                num = str(num)
                            mineWin.addstr(y, x, num, attr) 
                            mineWin.addch(y, x + 1, ' ', attr) 
                            mineWin.addch(y, x - 1, ' ', attr)

    mineWin.refresh()
    return end_time

def shineMineField(mineWin, width, height): 
    fieldWidth = (Consts.numhlines + 1) * width
    fieldHeight = (Consts.numvlines + 1) * height
    xend = fieldWidth
    yend = fieldHeight 
    halfx = (Consts.numhlines + 1) / 2
    halfy = (Consts.numvlines + 1) / 2
    while True:
        mineWin.clear()
        for x in range (0, xend):
            for y in range (0, yend):
                disx = x
                disy = y
                if (disx % halfx == 0) and (disx / halfx) % 2 != 0:
                    if (disy % halfy == 0) and (disy / halfy) % 2 != 0:
                        fieldx = int((disx / halfx - 1) / 2)
                        fieldy = int((disy / halfy - 1) / 2)
                        attr = curses.A_STANDOUT | curses.color_pair(3)
                        mineWin.chgat(y, x, 1, attr)
                        mineWin.chgat(y, x + 1, 1, attr)
                        mineWin.chgat(y, x - 1, 1, attr)
        time.sleep(0.05)
        mineWin.refresh()

def helpInfo():
    print('If you want to play standard mode, please enter:')
    print('python3 Termine.py easy/medium/hard')
    print('If you want to play your own customized mode, pleas enter:')
    print('python3 Termine.py customized <width> <height> <numOfMines>')

wrapper(Main)
