#!/usr/bin/env python3
import time
import curses
import const
import sys
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
    stdscr.addstr(1, 1, out)
    stdscr.refresh()
    mine, log, panel = drawWindowLayout(stdscr, mineFieldWidth, mineFieldHeight)
    drawUndeployedMineField(mine, mineFieldWidth, mineFieldHeight)
    while True:
        queryGameStatus(shell, stdscr)
        event = stdscr.getch()
        if event == ord("q"): break 
        if event == ord("r"):
            shell = restartNewGame(mine, mineFieldWidth, mineFieldHeight, numMines)
        if event == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_PRESSED :
                pokeMineField(stdscr, my, mx, shell, mine)
            elif bstate & curses.BUTTON3_PRESSED:
                alreadyFlagged = flagMineField(my, mx, shell, mine)
                if alreadyFlagged:
                    unflagMineField(my, mx, shell, mine)
        if checkSuccess(shell):
            displayGameOver(shell, stdscr, mine, mineFieldWidth, mineFieldHeight, True)

        elif checkFailure(shell):
            displayGameOver(shell, stdscr, mine, mineFieldWidth, mineFieldHeight, False)
        else:
            stdscr.addstr(2, 1, '        ')
            
            

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
    stdscr.addstr(3, 1, str(flags) + '/' + mines + ' ')

        
def unflagMineField(y, x, shell, mineWin):
    starty, startx = mineWin.getbegyx()
    unitx = const.numhlines + 1
    unity = const.numvlines + 1
    y, x = y - starty, x - startx
    if x % (unitx)  == 0 or y % (unity) == 0:
        return
    fieldx = (int)(x / unitx)
    fieldy = (int)(y / unity)
    flag = 'unflag' + ' ' + str(fieldx) + ' ' + str(fieldy)
    out = shell.getInput(flag)
    if out == None:
        return
    wx = fieldx * unitx + const.numhlines - 1
    wy = fieldy * unity + const.numvlines
    mineWin.addch(wy, wx, ord(' '), curses.A_REVERSE)
    mineWin.addch(wy, wx - 1, ord(' '), curses.A_REVERSE)
    mineWin.addch(wy, wx + 1, ord(' '), curses.A_REVERSE)
    mineWin.refresh()


def flagMineField(y, x, shell, mineWin):
    starty, startx = mineWin.getbegyx()
    unitx = const.numhlines + 1
    unity = const.numvlines + 1
    y, x = y - starty, x - startx
    if x % (unitx)  == 0 or y % (unity) == 0:
        return
    fieldx = (int)(x / unitx)
    fieldy = (int)(y / unity)
    flag = 'flag' + ' ' + str(fieldx) + ' ' + str(fieldy)
    out = shell.getInput(flag)
    if out == None:
        return True 
    wx = fieldx * unitx + const.numhlines - 1
    wy = fieldy * unity + const.numvlines
    attr = curses.A_BOLD | curses.color_pair(7) | curses.A_REVERSE
    mineWin.addstr(wy, wx, '$', attr)
    mineWin.addch(wy, wx - 1, ord(' '), attr)
    mineWin.addch(wy, wx + 1, ord(' '), attr)
    mineWin.refresh()
    return False 
def peekMineField(y, x, shell, mineWin):
    starty, startx = mineWin.getbegyx()
    unitx = const.numhlines + 1
    unity = const.numvlines + 1
    y, x = y - starty, x - startx
    if x % (unitx)  == 0 or y % (unity) == 0:
        return
    fieldx = (int)(x / unitx)
    fieldy = (int)(y / unity)
    peek = 'peek' + ' ' + str(fieldx) + ' ' + str(fieldy)
    num = shell.getInput(peek)
    wx = fieldx * unitx + const.numhlines - 1
    wy = fieldy * unity + const.numvlines
    mineWin.addstr(wy, wx, num)
    mineWin.addch(wy, wx - 1, ord(' '))
    mineWin.addch(wy, wx + 1, ord(' '))
    mineWin.refresh()


def pokeMineField(stdscr, y, x, shell, mineWin):
    starty, startx = mineWin.getbegyx()
    y, x = y - starty, x - startx
    unitx = const.numhlines + 1
    unity = const.numvlines + 1
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
            wx = minex * unitx + const.numhlines - 1
            wy = miney * unity + const.numvlines
            openedx.append(int(wx))
            openedy.append(int(wy))
            nums.append(string[4])
            number = 0
        for i in range(len(nums)):
            if len(nums[i]) > 1:
                mineWin.addstr(openedy[i], openedx[i], ':(' ) 
                displayGameOver(shell, stdscr, mineWin, shell.field.width, shell.field.height, False)
                return 
            else:
                number = int(nums[i])
                if number >= 5:
                    number = 5 
            attr = 0
            if number == 0:
                #attr = curses.A_BOLD | curses.color_pair(number + 1) | curses.A_DIM
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

def drawUndeployedMineField(mineWin, width, height):
    windowHeight, windowWidth = mineWin.getmaxyx()
    fieldWidth = (const.numhlines + 1) * width
    fieldHeight = (const.numvlines + 1) * height
    starty, startx = 0, 0
    xindex, yindex = startx, starty
    xend = xindex + fieldWidth
    yend = yindex + fieldHeight 
    attr = curses.A_BOLD | curses.color_pair(1)
    mineWin.addch(starty, startx, curses.ACS_ULCORNER, attr)
    mineWin.addch(starty + (const.numvlines + 1) * height, startx, curses.ACS_LLCORNER, attr)
    mineWin.addch(starty, startx + (const.numhlines + 1) * width, curses.ACS_URCORNER, attr)
    mineWin.addch(starty + (const.numvlines + 1) * height, startx + (const.numhlines + 1) * width, curses.ACS_LRCORNER, attr)
    for x in range(xindex + 1, xend):
        if (x - startx) % (const.numhlines + 1) == 0:
            mineWin.addch(yindex, x, curses.ACS_TTEE, attr)
            for y in range(yindex + 1, yend):
                if (y - starty) % (const.numvlines + 1) != 0:
                    mineWin.addch(y, x, curses.ACS_VLINE, attr)
        else:
            mineWin.addch(yindex, x, curses.ACS_HLINE, attr)

    for x in range(xindex + 1, xend):
        if (x - startx) % (const.numhlines + 1) == 0:
            mineWin.addch(yend, x, curses.ACS_BTEE, attr)
        else:
            mineWin.addch(yend, x, curses.ACS_HLINE, attr)

    for y in range(yindex + 1, yend):
        if (y - starty) % (const.numvlines + 1) == 0:
            mineWin.addch(y, startx, curses.ACS_LTEE, attr)
            for x in range(xindex + 1, xend):
                if (x - startx) % (const.numhlines + 1) == 0:
                    mineWin.addch(y, x, curses.ACS_PLUS, attr)
                else:
                    mineWin.addch(y, x, curses.ACS_HLINE, attr)
        else:
            mineWin.addch(y, startx, curses.ACS_VLINE, attr)

    for y in range(yindex + 1, yend):
        if (y - starty) % (const.numvlines + 1) == 0:
            mineWin.addch(y, xend, curses.ACS_RTEE, attr)
        else:
            mineWin.addch(y, xend, curses.ACS_VLINE, attr)

    halfx = (const.numhlines + 1) / 2
    halfy = (const.numvlines + 1) / 2

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
    #stdscr.border()
    #stdscr.refresh()
    height, width = stdscr.getmaxyx()
    heightDividor = (int)(height / 8)
    logColumns = 20
    paddingMineLog = 2 
    mineLines = 7 * heightDividor
    mineColumns = width - logColumns - paddingMineLog
    paddingTop = 3
    windowHeight, windowWidth = mineLines, mineColumns
    fieldWidth = (const.numhlines + 1) * (fwidth + 1)
    fieldHeight = (const.numvlines + 1) * (fheight + 1)
    starty = (int)((windowHeight - fieldHeight) / 2) 
    startx = (int)((windowWidth - fieldWidth) / 2)
    mineWin = curses.newwin(fieldHeight, fieldWidth, starty + paddingTop, startx)
    logLines = mineLines
    logWin = curses.newwin(logLines, logColumns, 3, mineColumns + paddingMineLog)
    logWin.border()
    logWin.refresh()
    paddingMinePanel = 2
    panelLines = height - paddingTop - mineLines - paddingMinePanel 
    panelColumns = width
    panelWin = curses.newwin(panelLines, panelColumns, height - panelLines, 0)
    panelWin.border()
    panelWin.refresh()
    return (mineWin, logWin, panelWin)



def displayGameOver(shell, stdscr, mineWin, width, height, success):
    fieldWidth = (const.numhlines + 1) * width
    fieldHeight = (const.numvlines + 1) * height
    xend = fieldWidth
    yend = fieldHeight 
    halfx = (const.numhlines + 1) / 2
    halfy = (const.numvlines + 1) / 2
    for x in range (0, xend):
        for y in range (0, yend):
            disx = x
            disy = y
            if (disx % halfx == 0) and (disx / halfx) % 2 != 0:
                if (disy % halfy == 0) and (disy / halfy) % 2 != 0:
                    fieldx = int((disx / halfx - 1) / 2)
                    fieldy = int((disy / halfy - 1) / 2)
                    attr = 0
                    if success:
                        if shell.field.status[fieldy][fieldx] == -1 and shell.field.opened[fieldy][fieldx] == False:
                            starty, startx = mineWin.getbegyx()
                            flagMineField(y + starty, x + startx, shell, mineWin)
                        attr = curses.A_NORMAL | curses.A_STANDOUT | curses.color_pair(3)
                        stdscr.addstr(2, 1, 'Success')
                    else:
                        if shell.field.flagged[fieldy][fieldx] == False and shell.field.opened[fieldy][fieldx] == False:
                            num = shell.field.status[fieldy][fieldx]
                            if num < 0:
                                num = ':('
                            else:
                                num = str(num)
                            mineWin.addstr(y, x, num) 
                        shell.field.opened[fieldy][fieldx] = True
                        attr = curses.A_STANDOUT | curses.color_pair(7)
                        stdscr.addstr(2, 1, 'You dead')

                    mineWin.chgat(y, x, 1, attr)
                    mineWin.chgat(y, x + 1, 1, attr)
                    mineWin.chgat(y, x - 1, 1, attr)
    mineWin.refresh()

def shineMineField(mineWin, width, height): 
    fieldWidth = (const.numhlines + 1) * width
    fieldHeight = (const.numvlines + 1) * height
    xend = fieldWidth
    yend = fieldHeight 
    halfx = (const.numhlines + 1) / 2
    halfy = (const.numvlines + 1) / 2
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
