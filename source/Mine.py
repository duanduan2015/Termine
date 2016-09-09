import curses
import time
import Consts
from MineShell import MineShell
class Mine:
    def __init__(self, mine, shell):
        self.win = mine
        self.shell = shell
        self.disablePokeFlag = False

    def disablePoke(self):
        self.disablePokeFlag = True

    def enablePoke(self):
        self.disablePokeFlag = False

    def drawUndeployedMineField(self):
        self.drawMineFieldFrame(curses.color_pair(1))
        yend, xend = self.win.getmaxyx()
        halfx = (Consts.numhlines + 1) / 2
        halfy = (Consts.numvlines + 1) / 2
        for x in range (0, xend - 1):
            for y in range (0, yend - 1):
                if (x % halfx == 0) and (x / halfx) % 2 != 0:
                    if (y % halfy == 0) and (y / halfy) % 2 != 0:
                        fieldx = int((x / halfx - 1) / 2)
                        fieldy = int((y / halfy - 1) / 2)
                        self.win.addch(y, x, ord(' '), curses.A_REVERSE)
                        self.win.addch(y, x + 1, ord(' '), curses.A_REVERSE)
                        self.win.addch(y, x - 1, ord(' '), curses.A_REVERSE)
        self.win.refresh()

    def drawMineFieldFrame(self, color):
        height, width = self.win.getmaxyx()
        starty, startx = 0, 0
        xindex, yindex = startx, starty
        xend, yend = width - 1, height - 1
        attr = curses.A_BOLD | color 
        self.drawBorder(color)
        for x in range(xindex + 1, xend):
            if (x - startx) % (Consts.numhlines + 1) == 0:
                self.win.addch(yindex, x, curses.ACS_TTEE, attr)
                for y in range(yindex + 1, yend):
                    if (y - starty) % (Consts.numvlines + 1) != 0:
                        self.win.addch(y, x, curses.ACS_VLINE, attr)
            else:
                self.win.addch(yindex, x, curses.ACS_HLINE, attr)

        for x in range(xindex + 1, xend):
            if (x - startx) % (Consts.numhlines + 1) == 0:
                self.win.addch(yend, x, curses.ACS_BTEE, attr)
            else:
                self.win.addch(yend, x, curses.ACS_HLINE, attr)

        for y in range(yindex + 1, yend):
            if (y - starty) % (Consts.numvlines + 1) == 0:
                self.win.addch(y, startx, curses.ACS_LTEE, attr)
                for x in range(xindex + 1, xend):
                    if (x - startx) % (Consts.numhlines + 1) == 0:
                        self.win.addch(y, x, curses.ACS_PLUS, attr)
                    else:
                        self.win.addch(y, x, curses.ACS_HLINE, attr)
            else:
                self.win.addch(y, startx, curses.ACS_VLINE, attr)

        for y in range(yindex + 1, yend):
            if (y - starty) % (Consts.numvlines + 1) == 0:
                self.win.addch(y, xend, curses.ACS_RTEE, attr)
            else:
                self.win.addch(y, xend, curses.ACS_VLINE, attr)

    def unflagMineField(self, y, x):
        starty, startx = self.win.getbegyx()
        unitx = Consts.numhlines + 1
        unity = Consts.numvlines + 1
        y, x = y - starty, x - startx
        if x % (unitx)  == 0 or y % (unity) == 0:
            return
        fieldx = x // unitx
        fieldy = y // unity
        flag = 'unflag' + ' ' + str(fieldx) + ' ' + str(fieldy)
        out = self.shell.getInput(flag)
        if out == None:
            return
        wx = (fieldx + 1) * (Consts.numhlines + 1) - 2
        wy = fieldy * (Consts.numvlines + 1) + 1
        self.win.addch(wy, wx, ord(' '), curses.A_REVERSE)
        self.win.addch(wy, wx - 1, ord(' '), curses.A_REVERSE)
        self.win.addch(wy, wx + 1, ord(' '), curses.A_REVERSE)
        self.win.refresh()

    def flagMineField(self, y, x):
        starty, startx = self.win.getbegyx()
        unitx = Consts.numhlines + 1
        unity = Consts.numvlines + 1
        y, x = y - starty, x - startx
        if x % (unitx)  == 0 or y % (unity) == 0:
            return
        fieldx = x // unitx
        fieldy = y // unity
        flag = 'flag' + ' ' + str(fieldx) + ' ' + str(fieldy)
        out = self.shell.getInput(flag)
        if out == None:
            return True 
        wx = (fieldx + 1) * (Consts.numhlines + 1) - 2
        wy = fieldy * (Consts.numvlines + 1) + 1
        attr = curses.A_BOLD | curses.color_pair(7) | curses.A_REVERSE
        self.win.addstr(wy, wx, '$', attr)
        self.win.addch(wy, wx - 1, ord(' '), attr)
        self.win.addch(wy, wx + 1, ord(' '), attr)
        self.win.refresh()
        return False 

    def pokeMineField(self, y, x):
        if self.disablePokeFlag:
            return
        starty, startx = self.win.getbegyx()
        y, x = y - starty,  x - startx
        unitx = Consts.numhlines + 1 
        unity = Consts.numvlines + 1 
        if x % (unitx)  == 0 or y % (unity) == 0:
            return
        fieldx = x // unitx
        fieldy = y // unity
        poke = 'poke' + ' ' + str(fieldx) + ' ' + str(fieldy)
        pokeOut = self.shell.getInput(poke)
        if isinstance(pokeOut, list):
            openedx = []
            openedy = []
            nums = []
            for out in pokeOut:
                string = out.split(' ')
                minex = int(string[0])
                miney = int(string[1])
                wx = (minex + 1) * (Consts.numhlines + 1) - 2
                wy = miney * (Consts.numvlines + 1) + 1
                openedx.append(int(wx))
                openedy.append(int(wy))
                nums.append(string[4])
                number = 0
            for i in range(len(nums)):
                if len(nums[i]) > 1:
                    attr = curses.color_pair(7) | curses.A_STANDOUT
                    self.win.addstr(openedy[i], openedx[i], ':(' , attr) 
                    self.win.addch(openedy[i], openedx[i] - 1, ord(' '), attr)
                    self.win.refresh()
                    return "dead"
                else:
                    number = int(nums[i])
                    if number >= 5:
                        number = 5 
                    attr = 0
                    if number == 0:
                        nums[i] = ' '
                    else:
                        attr = curses.A_BOLD | curses.color_pair(number + 1) 
                    self.win.addch(openedy[i], openedx[i], ord(nums[i]), attr) 
                    self.win.addch(openedy[i], openedx[i] - 1, ord(' '), attr)
                    self.win.addch(openedy[i], openedx[i] + 1, ord(' '), attr)

            self.win.refresh()
            return "alive"
        else:
            return None


    def displayGameOver(self, success):
        end_time = time.time()
        yend, xend = self.win.getmaxyx()
        halfx = (Consts.numhlines + 1) / 2
        halfy = (Consts.numvlines + 1) / 2
        color = curses.color_pair(1)
        if success:
            color = curses.color_pair(3)
            self.drawMineFieldFrame(curses.color_pair(3))
        else:
            self.drawMineFieldFrame(curses.color_pair(7))
        for x in range (0, xend):
            for y in range (0, yend):
                if (x % halfx == 0) and (x / halfx) % 2 != 0:
                    if (y % halfy == 0) and (y / halfy) % 2 != 0:
                        fieldx = int((x / halfx - 1) / 2)
                        fieldy = int((y / halfy - 1) / 2)
                        attr = 0
                        if self.shell.field.flagged[fieldy][fieldx] == False and self.shell.field.opened[fieldy][fieldx] == False:
                            num = self.shell.field.status[fieldy][fieldx]
                            self.shell.field.opened[fieldy][fieldx] = True
                            if num < 0:
                                if success:
                                    num = '$'
                                    attr = curses.A_STANDOUT | curses.color_pair(7)
                                    self.win.addstr(y, x, num, attr) 
                                    self.win.addch(y, x - 1, ord(' '), attr)
                                    self.win.addch(y, x + 1, ord(' '), attr)
                                else:
                                    num = ':('
                                    attr = curses.A_STANDOUT | curses.color_pair(7)
                                    self.win.addstr(y, x, num, attr) 
                                    self.win.addch(y, x - 1, ord(' '), attr)
                            else:
                                attr = curses.A_BOLD | curses.color_pair(num + 1) 
                                if num == 0:
                                    num = ' '
                                else:
                                    num = str(num)
                                self.win.addstr(y, x, num, attr) 
                                self.win.addch(y, x + 1, ' ', attr) 
                                self.win.addch(y, x - 1, ' ', attr)

        self.win.refresh()
        return end_time

    def drawPokedMineField(self):
        fieldHeight, fieldWidth = self.win.getmaxyx()
        xend = fieldWidth
        yend = fieldHeight 

        halfx = (Consts.numhlines + 1) / 2
        halfy = (Consts.numvlines + 1) / 2

        for x in range (0, xend):
            for y in range (0, yend):
                if (x % halfx == 0) and (x / halfx) % 2 != 0:
                    if (y % halfy == 0) and (y / halfy) % 2 != 0:
                        fieldx = int((x / halfx - 1) / 2)
                        fieldy = int((y / halfy - 1) / 2)
                        if self.shell.field.opened[fieldy][fieldx] == True:
                            number = self.shell.field.status[fieldy][fieldx]
                            attr = curses.A_BOLD | curses.color_pair(number + 1) 
                            if number == 0:
                                number = ' '
                            else:
                                number = str(number)
                            self.win.addstr(y, x, number, attr) 
                            self.win.addch(y, x - 1, ord(' '), attr)
                            self.win.addch(y, x + 1, ord(' '), attr)
                        elif self.shell.field.flagged[fieldy][fieldx] == True:
                            attr = curses.A_BOLD | curses.color_pair(7) | curses.A_REVERSE
                            self.win.addstr(y, x, '$', attr)
                            self.win.addch(y, x - 1, ord(' '), attr)
                            self.win.addch(y, x + 1, ord(' '), attr)
        self.win.refresh()

    def peekMineField(self, y, x):
        starty, startx = self.win.getbegyx()
        unitx = Consts.numhlines + 1
        unity = Consts.numvlines + 1
        y, x = y - starty, x - startx
        if x % (unitx)  == 0 or y % (unity) == 0:
            return
        fieldx = (int)(x / unitx)
        fieldy = (int)(y / unity)
        peek = 'peek' + ' ' + str(fieldx) + ' ' + str(fieldy)
        num = self.shell.getInput(peek)
        wx = fieldx * unitx + Consts.numhlines - 1
        wy = fieldy * unity + Consts.numvlines
        self.shell.addstr(wy, wx, num)
        self.shell.addch(wy, wx - 1, ord(' '))
        self.shell.addch(wy, wx + 1, ord(' '))
        self.shell.refresh()

    def drawBorder(self, color):
        attr = color | curses.A_BOLD
        ls, rs = attr | curses.ACS_VLINE, attr | curses.ACS_VLINE
        ts, bs = attr | curses.ACS_HLINE, attr | curses.ACS_HLINE
        tl = attr | curses.ACS_ULCORNER
        tr = attr | curses.ACS_URCORNER
        bl = attr | curses.ACS_LLCORNER
        br = attr | curses.ACS_LRCORNER
        self.win.border(ls, rs, ts, bs, tl, tr, bl, br)
