#!/usr/bin/env python3
import time
from datetime import date
import curses
import Consts
import sys
import os.path
from curses import wrapper
from MineShell.MineShell import MineShell
from Window import Window
from Record import Record
from Mine import Mine
from Game import Game

def Main(stdscr):
    setCursesFeatures()
    if sys.argv[1] == 'help':
        curses.endwin()
        helpInfo()
        sys.exit(1) 
    stdscr.refresh()
    mineFieldWidth, mineFieldHeight, numMines, mode = parseArgs(sys.argv)

    game = Game(stdscr, mineFieldWidth, mineFieldHeight, numMines)
    game.start() 

    while True:
        event = stdscr.getch()

        if game.checkWin():
            game.gameWin()

        if event == ord("q"): 
            game.exit() 

        if event == ord("R"):   #display Records
            game.displayRecord()

        if event == ord("c"):   #continue game
            game.resume()

        if event == ord("p"):   #pause game
            game.pause()

        if event == ord("r"):   #restart game
            game.restart()

        if event == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_PRESSED :
                if game.poke(my, mx) == "dead":
                    game.gameLose()
            elif bstate & curses.BUTTON3_PRESSED:
                game.flag(my, mx)
            

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


def helpInfo():
    print('If you want to play standard mode, please enter:')
    print('python3 Termine.py easy/medium/hard')
    print('If you want to play your own customized mode, pleas enter:')
    print('python3 Termine.py customized <width> <height> <numOfMines>')

wrapper(Main)
