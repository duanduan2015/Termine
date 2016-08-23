#!/usr/bin/env python3
import curses
import const
from curses import wrapper
from MineShell.MineShell import MineShell

def Main(stdscr):
    mineFieldWidth = 16 
    mineFieldHeight = 16 
    numMines = 40 
    setCursesFeatures()
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
        if event == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_PRESSED :
                pokeMineField(my, mx, shell, mine)
            elif bstate & curses.BUTTON3_PRESSED:
                alreadyFlagged = flagMineField(my, mx, shell, mine)
                if alreadyFlagged:
                    unflagMineField(my, mx, shell, mine)
            continue

def queryGameStatus(shell, stdscr):
    if shell.getInput('query success'):
        stdscr.addstr(2, 1, 'Success')
    flags = shell.getInput('query flags')
    mines = shell.getInput('query mines')
    stdscr.addstr(3, 1, str(flags) + '/' + str(mines))

        
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
    mineWin.addstr(wy, wx, '$')
    mineWin.addch(wy, wx - 1, ord(' '))
    mineWin.addch(wy, wx + 1, ord(' '))
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


def pokeMineField(y, x, shell, mineWin):
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
        for i in range(len(nums)):
            if len(nums[i]) > 1:
                nums[i] = 'b'
            mineWin.addch(openedy[i], openedx[i], ord(nums[i]))
            #mineWin.addstr(openedy[i], openedx[i], str(nums[i]))
            mineWin.addch(openedy[i], openedx[i] - 1, ord(' '))
            mineWin.addch(openedy[i], openedx[i] + 1, ord(' '))
        mineWin.refresh()
    else:
        return
    #elif isinstance(pokeOut, str):
    #    wx = (int)(0 + fieldx * 2 * halfx + halfx)
    #    wy = (int)(0 + fieldy * 2 * halfy + halfy)
    #    mineWin.addstr(wy, wx, str(pokeOut))
    #    mineWin.addstr(wy, wx - 1, ' ')
    #    mineWin.addstr(wy, wx + 1, ' ')
    mineWin.refresh()

def setCursesFeatures():
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
    mineWin.addch(starty, startx, curses.ACS_ULCORNER)
    mineWin.addch(starty + (const.numvlines + 1) * height, startx, curses.ACS_LLCORNER)
    mineWin.addch(starty, startx + (const.numhlines + 1) * width, curses.ACS_URCORNER)
    mineWin.addch(starty + (const.numvlines + 1) * height, startx + (const.numhlines + 1) * width, curses.ACS_LRCORNER)
    for x in range(xindex + 1, xend):
        if (x - startx) % (const.numhlines + 1) == 0:
            mineWin.addch(yindex, x, curses.ACS_TTEE)
            for y in range(yindex + 1, yend):
                if (y - starty) % (const.numvlines + 1) != 0:
                    mineWin.addch(y, x, curses.ACS_VLINE)
        else:
            mineWin.addch(yindex, x, curses.ACS_HLINE)

    for x in range(xindex + 1, xend):
        if (x - startx) % (const.numhlines + 1) == 0:
            mineWin.addch(yend, x, curses.ACS_BTEE)
        else:
            mineWin.addch(yend, x, curses.ACS_HLINE)

    for y in range(yindex + 1, yend):
        if (y - starty) % (const.numvlines + 1) == 0:
            mineWin.addch(y, startx, curses.ACS_LTEE)
            for x in range(xindex + 1, xend):
                if (x - startx) % (const.numhlines + 1) == 0:
                    mineWin.addch(y, x, curses.ACS_PLUS)
                else:
                    mineWin.addch(y, x, curses.ACS_HLINE)
        else:
            mineWin.addch(y, startx, curses.ACS_VLINE)

    for y in range(yindex + 1, yend):
        if (y - starty) % (const.numvlines + 1) == 0:
            mineWin.addch(y, xend, curses.ACS_RTEE)
        else:
            mineWin.addch(y, xend, curses.ACS_VLINE)

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


wrapper(Main)
