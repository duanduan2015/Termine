#!/usr/bin/env python3

from MineShell.MineShell import MineShell
#from MineShell import MineShell

def Main():
    s = MineShell()
    #s.getInput('minefield 3 3 2')
    while True:
        a = input("termine> ")
        out = s.getInput(a)
        if (isinstance(out, str)):
            print('out: %s' % out)
        else:
            for o in out:
                print('out: %s' %o)

if __name__ == '__main__':
    Main()
