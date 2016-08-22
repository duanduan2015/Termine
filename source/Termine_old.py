#!/usr/bin/env python3
import curses
from curses import wrapper
from MineShell.MineShell import MineShell

def Main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.refresh()
    curses.mousemask(curses.BUTTON1_PRESSED)
    curses.mouseinterval(0)
    curses.curs_set(0)
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
    block = curses.ACS_BLOCK
    width = 8 
    height = 8 
    numMines = 10 
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

    for x in range (startx, xend):
        for y in range (starty, yend):
            disx = x - startx
            disy = y - starty
            if (disx % halfx == 0) and (disx / halfx) % 2 != 0:
                if (disy % halfy == 0) and (disy / halfy) % 2 != 0:
                    fieldx = int((disx / halfx - 1) / 2)
                    fieldy = int((disy / halfy - 1) / 2)
                    #cmd = 'peek' + ' ' + str(fieldx) + ' ' + str(fieldy)
                    #num = int(shell.getInput(cmd))
                    #if num < 0:
                    #    num = '*'
                    #else:
                    #    num = str(num)
                    #stdscr.addch(y + 1, x, ord(' '), curses.A_REVERSE)
                    #stdscr.addch(y - 1, x, ord(' '), curses.A_REVERSE)
                    stdscr.addch(y, x, ord(' '), curses.A_REVERSE)
                    stdscr.addch(y, x + 1, ord(' '), curses.A_REVERSE)
                    stdscr.addch(y, x - 1, ord(' '), curses.A_REVERSE)
                    #stdscr.addch(y, x + 2, ord(' '), curses.A_REVERSE)
                    #stdscr.addch(y, x - 2, ord(' '), curses.A_REVERSE)

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

            stop = False
            for x in xlist:
                if stop:
                    break
                for y in ylist:
                    if stop:
                        break
                    disx = x - startx
                    disy = y - starty
                    if (disx % halfx == 0) and (disx / halfx) % 2 != 0:
                        if (disy % halfy == 0) and (disy / halfy) % 2 != 0:
                            fieldx = int((disx / halfx - 1) / 2)
                            fieldy = int((disy / halfy - 1) / 2)
                            if fieldx >= width or fieldy >= height:
                                continue
                            #peek = 'peek' + ' ' + str(fieldx) + ' ' + str(fieldy)
                            #num = shell.getInput(peek)
                            #wx = (int)(startx + fieldx * 2 * halfx + halfx)
                            #wy = (int)(starty + fieldy * 2 * halfy + halfy)
                            #stdscr.addstr(wy, wx, num)
                            #stdscr.addch(wy, wx - 1, ord(' '))
                            #stdscr.addch(wy, wx + 1, ord(' '))
                            poke = 'poke' + ' ' + str(fieldx) + ' ' + str(fieldy)
                            pokeOut = shell.getInput(poke)
                            #pokeOut = 'hello' 
                            if isinstance(pokeOut, list):
                                openedx = []
                                openedy = []
                                nums = []
                                for out in pokeOut:
                                    string = out.split(' ')
                                    minex = int(string[0])
                                    miney = int(string[1])
                                    wx = startx + minex * 2 * halfx + halfx
                                    wy = starty + miney * 2 * halfy + halfy 
                                    openedx.append(int(wx))
                                    openedy.append(int(wy))
                                    nums.append(int(string[4]))
                                for i in range(len(nums)):
                                    stdscr.addch(openedy[i], openedx[i], ord(str(nums[i])))
                                    stdscr.addch(openedy[i], openedx[i] - 1, ord(' '))
                                    stdscr.addch(openedy[i], openedx[i] + 1, ord(' '))
                                stop = True
                            elif isinstance(pokeOut, str):
                                wx = (int)(startx + fieldx * 2 * halfx + halfx)
                                wy = (int)(starty + fieldy * 2 * halfy + halfy)
                                stdscr.addstr(wy, wx, str(pokeOut))
                                stdscr.addstr(wy, wx - 1, ' ')
                                stdscr.addstr(wy, wx + 1, ' ')
                                stop = True
                            stdscr.refresh()
        continue
wrapper(Main)

