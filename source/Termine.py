#!/usr/bin/env python3
import curses
from curses import wrapper
from MineShell.MineShell import MineShell

def Main(stdscr):
    setCursesFeatures()
    mine, log, panel = drawWindowLayout(stdscr)
    mineFieldWidth = 16 
    mineFieldHeight = 16 
    drawMineField(mine, mineFieldWidth, mineFieldHeight)
    while True:
        continue

def setCursesFeatures():
    curses.mousemask(curses.BUTTON1_PRESSED)
    curses.mouseinterval(0)
    curses.curs_set(0)

def drawMineField(mineWin, width, height):
    numhlines = 3
    numvlines = 1
    windowHeight, windowWidth = mineWin.getmaxyx()
    fieldWidth = (numhlines + 1) * width
    fieldHeight = (numvlines + 1) * height
    starty = (int)((windowHeight - fieldHeight) / 2) 
    startx = (int)((windowWidth - fieldWidth) / 2)
    xindex, yindex = startx, starty
    xend = xindex + fieldWidth
    yend = yindex + fieldHeight 
    vline = curses.ACS_VLINE
    hline = curses.ACS_HLINE
    topT = curses.ACS_TTEE
    botT = curses.ACS_BTEE
    leftT = curses.ACS_LTEE
    rightT = curses.ACS_RTEE
    plus = curses.ACS_PLUS
    uplcor = curses.ACS_ULCORNER
    uprcor = curses.ACS_URCORNER
    lolcor = curses.ACS_LLCORNER
    lorcor = curses.ACS_LRCORNER
    mineWin.addch(starty, startx, uplcor)
    mineWin.addch(starty + (numvlines + 1) * height, startx, lolcor)
    mineWin.addch(starty, startx + (numhlines + 1) * width, uprcor)
    mineWin.addch(starty + (numvlines + 1) * height, startx + (numhlines + 1) * width, lorcor)
    for x in range(xindex + 1, xend):
        if (x - startx) % (numhlines + 1) == 0:
            mineWin.addch(yindex, x, topT)
            for y in range(yindex + 1, yend):
                if (y - starty) % (numvlines + 1) != 0:
                    mineWin.addch(y, x, vline)
        else:
            mineWin.addch(yindex, x, hline)

    for x in range(xindex + 1, xend):
        if (x - startx) % (numhlines + 1) == 0:
            mineWin.addch(yend, x, botT)
        else:
            mineWin.addch(yend, x, hline)

    for y in range(yindex + 1, yend):
        if (y - starty) % (numvlines + 1) == 0:
            mineWin.addch(y, startx, leftT)
            for x in range(xindex + 1, xend):
                if (x - startx) % (numhlines + 1) == 0:
                    mineWin.addch(y, x, plus)
                else:
                    mineWin.addch(y, x, hline)
        else:
            mineWin.addch(y, startx, vline)

    for y in range(yindex + 1, yend):
        if (y - starty) % (numvlines + 1) == 0:
            mineWin.addch(y, xend, rightT)
        else:
            mineWin.addch(y, xend, vline)
    mineWin.refresh()

def drawWindowLayout(stdscr):
    #stdscr.border()
    #stdscr.refresh()
    height, width = stdscr.getmaxyx()
    heightDividor = (int)(height / 8)
    logColumns = 20
    paddingMineLog = 2 
    mineLines = 7 * heightDividor
    mineColumns = width - logColumns - paddingMineLog
    paddingTop = 3
    mineWin = curses.newwin(mineLines, mineColumns, paddingTop, 0)
    mineWin.border()
    mineWin.refresh()
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
