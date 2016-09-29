#!/usr/bin/env python3
import time
from datetime import date
import curses
import Consts
import sys
import os.path
import threading
from curses import wrapper
from MineShell.MineShell import MineShell
from Window import Window
from Record import Record
from GameField import GameField 
from Game import Game
from Arguments import Arguments

def Main(stdscr):
    args = Arguments(sys.argv)
    mineFieldWidth, mineFieldHeight, numMines, mode = args.parse()
    game = Game(stdscr, mineFieldWidth, mineFieldHeight, numMines)
    game.start() 
    while True:
        event = stdscr.getch()
        my, mx = 0, 0
        if event == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_PRESSED :
                if game.poke(my, mx) == "dead":
                    game.gameLose()
            elif bstate & curses.BUTTON3_PRESSED:
                game.flag(my, mx)
        maxy, maxx = stdscr.getmaxyx()

        if game.checkWin():
            game.gameWin()

        if event == ord("q") or (mx >= maxx - 9 and mx <= maxx - 4 and my == maxy - 2): 
            game.exit() 

        if event == ord("R") or (mx >= 39 and mx <= 47 and my == maxy - 2):   
            game.displayRecord()

        if event == ord("c") or (mx >= 14 and mx <= 21 and my == maxy - 2):   
            game.resume()

        if event == ord("p") or (mx >= 3 and mx <= 9 and my == maxy - 2):   
            game.pause()

        if event == ord("r") or (mx >= 26 and mx <= 34 and my == maxy - 2):   
            game.restart()
wrapper(Main)
