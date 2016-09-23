import curses
import sys

class Arguments:
    def __init__(self, args):
        self.args = args

    def parse(self):
        if self.args[1] == 'help':
            curses.endwin()
            self.helpInfo()
        if self.args[1] == 'easy':
            return (8, 8, 10, 'easy')
        if self.args[1] == 'medium':
            return (16, 16, 40, 'medium')
        if self.args[1] == 'hard':
            return (30, 16, 99, 'hard')
        if self.args[1] == 'customized':
            width = int(self.args[2])
            height = int(self.args[3])
            num = int(self.args[4])
            return (width, height, num, 'customized')


    def helpInfo(self):
        print('If you want to play standard mode, please enter:')
        print('python3 Termine.py easy/medium/hard')
        print('If you want to play your own customized mode, pleas enter:')
        print('python3 Termine.py customized <width> <height> <numOfMines>')
        sys.exit(0) 
