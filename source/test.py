#!/usr/bin/env python3

from MineShell.MineShell import MineShell
def Main():
    s = MineShell()
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
