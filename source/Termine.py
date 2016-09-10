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
from Arguments import Arguments

def Main(stdscr):
    args = Arguments(sys.argv)
    mineFieldWidth, mineFieldHeight, numMines, mode = args.parse()
    game = Game(stdscr, mineFieldWidth, mineFieldHeight, numMines)
    game.start() 
    while True:
        event = stdscr.getch()

        if game.checkWin():
            game.gameWin()

        if event == ord("q"): 
            game.exit() 

        if event == ord("R"):   
            game.displayRecord()

        if event == ord("c"):   
            game.resume()

        if event == ord("p"):   
            game.pause()

        if event == ord("r"):   
            game.restart()

        if event == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_PRESSED :
                if game.poke(my, mx) == "dead":
                    game.gameLose()
            elif bstate & curses.BUTTON3_PRESSED:
                game.flag(my, mx)

wrapper(Main)
