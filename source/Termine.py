#!/usr/bin/env python3
import curses
from curses import wrapper
from MineShell.MineShell import MineShell

def Main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.refresh()
    curses.mousemask(1)
    #height, width = stdscr.getmaxyx()
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
    width = 16 
    height = 16 
    numMines = 15 
    startx = 10
    starty = 10
    numhlines = 3
    numvlines = 1

    stdscr.addch(starty, startx, uplcor)
    stdscr.addch(starty + (numvlines + 1) * height, startx, lolcor)
    stdscr.addch(starty, startx + (numhlines + 1) * width, uprcor)
    stdscr.addch(starty + (numvlines + 1) * height, startx + (numhlines + 1) * width, lorcor)
    xindex = startx
    yindex = starty
    xend = startx + (width) + width * numhlines
    yend = starty + (height) + height * numvlines

    for x in range(xindex + 1, xend):
        if (x - startx) % (numhlines + 1) == 0:
            stdscr.addch(yindex, x, topT)
            for y in range(yindex + 1, yend):
                if (y - starty) % (numvlines + 1) != 0:
                    stdscr.addch(y, x, vline)
        else:
            stdscr.addch(yindex, x, hline)

    for x in range(xindex + 1, xend):
        if (x - startx) % (numhlines + 1) == 0:
            stdscr.addch(yend, x, botT)
        else:
            stdscr.addch(yend, x, hline)

    for y in range(yindex + 1, yend):
        if (y - starty) % (numvlines + 1) == 0:
            stdscr.addch(y, startx, leftT)
            for x in range(xindex + 1, xend):
                if (x - startx) % (numhlines + 1) == 0:
                    stdscr.addch(y, x, plus)
                else:
                    stdscr.addch(y, x, hline)
        else:
            stdscr.addch(y, startx, vline)

    for y in range(yindex + 1, yend):
        if (y - starty) % (numvlines + 1) == 0:
            stdscr.addch(y, xend, rightT)
        else:
            stdscr.addch(y, xend, vline)

    shell = MineShell()
    create = 'minefield ' + str(width) + ' ' + str(height) + ' ' + str(numMines)
    out = shell.getInput(create)
    halfx = (numhlines + 1) / 2
    halfy = (numvlines + 1) / 2
    #for x in range (startx, xend):
    #    for y in range (starty, yend):
    #        disx = x - startx
    #        disy = y - starty
    #        if (disx % halfx == 0) and (disx / halfx) % 2 != 0:
    #            if (disy % halfy == 0) and (disy / halfy) % 2 != 0:
    #                fieldx = int((disx / halfx - 1) / 2)
    #                fieldy = int((disy / halfy - 1) / 2)
    #                cmd = 'peek' + ' ' + str(fieldx) + ' ' + str(fieldy)
    #                num = int(shell.getInput(cmd))
    #                if num < 0:
    #                    num = '*'
    #                else:
    #                    num = str(num)
    #                stdscr.addch(y, x, ord(num))

    print(out)
    while True:
        event = stdscr.getch()
        if event == ord("q"): break 
        if event == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            #stdscr.addch(my, mx, ord('&'))
            xlist = [] 
            ylist = [] 
            xlist.append(mx)
            ylist.append(my)
            for i in range(1, int(halfx)):
                xlist.append(mx - i)
                xlist.append(mx + i)
            for i in range(1, int(halfy) + 1):
                ylist.append(my - i)
                ylist.append(my + i)

            for x in xlist:
                for y in ylist:
                    disx = x - startx
                    disy = y - starty
                    if (disx % halfx == 0) and (disx / halfx) % 2 != 0:
                        if (disy % halfy == 0) and (disy / halfy) % 2 != 0:
                            fieldx = int((disx / halfx - 1) / 2)
                            fieldy = int((disy / halfy - 1) / 2)
                            if fieldx >= width or fieldy >= height:
                                    continue
                            cmd = 'peek' + ' ' + str(fieldx) + ' ' + str(fieldy)
                            num = int(shell.getInput(cmd))
                            if num < 0:
                                num = '*'
                            else:
                                num = str(num)
                            stdscr.addch(y, x, ord(num))
                            break
        stdscr.refresh()
        continue
wrapper(Main)

