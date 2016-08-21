#!/usr/bin/env python3
import curses
from curses import wrapper
from MineShell.MineShell import MineShell

def Main(stdscr):
    mine, log, panel = drawWindowLayout(stdscr)
    while True:
        continue

def drawWindowLayout(stdscr):
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
