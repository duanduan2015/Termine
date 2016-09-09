import curses
import Consts
class Window:
    def __init__(self, stdscr):
        self.scr = stdscr

    def drawLayout(self, fwidth, fheight):
        height, width = self.scr.getmaxyx()
        mineFieldWidth = Consts.numhlines * fwidth + fwidth + 1
        mineFieldHeight = Consts.numvlines * fheight + fheight + 1
        if mineFieldWidth + Consts.logWindowWidth >= width:
            return None 
        if mineFieldHeight + Consts.controlBarHeight >= height:
            return None 
        starty = (int)((height - Consts.controlBarHeight - mineFieldHeight) / 2) 
        startx = (int)((width - Consts.logWindowWidth - mineFieldWidth) / 2)
        mineWin = curses.newwin(mineFieldHeight, mineFieldWidth, starty, startx)
        recordBeginx = startx + mineFieldWidth // 2 - Consts.recordWinWidth // 2 
        recordBeginy = starty + mineFieldHeight // 2 - Consts.recordWinHeight // 2 - 2 
        recordWin = curses.newwin(Consts.recordWinHeight, Consts.recordWinWidth, recordBeginy, recordBeginx) 
        logWin = curses.newwin(height - Consts.controlBarHeight, Consts.logWindowWidth, 0, width - Consts.logWindowWidth)
        self.drawBorder(logWin, curses.color_pair(6))
        logWin.refresh()
        controlBar = curses.newwin(Consts.controlBarHeight, width, height - Consts.controlBarHeight, 0)
        self.drawBorder(controlBar, curses.color_pair(5))
        controlBar.refresh()
        return mineWin, logWin, controlBar, recordWin

    def drawBorder(self, win, color):
        attr = color | curses.A_BOLD
        ls, rs = attr | curses.ACS_VLINE, attr | curses.ACS_VLINE
        ts, bs = attr | curses.ACS_HLINE, attr | curses.ACS_HLINE
        tl = attr | curses.ACS_ULCORNER
        tr = attr | curses.ACS_URCORNER
        bl = attr | curses.ACS_LLCORNER
        br = attr | curses.ACS_LRCORNER
        win.border(ls, rs, ts, bs, tl, tr, bl, br)