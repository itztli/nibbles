#!/usr/bin/env python3

import sys, termios, tty, os, time
import select
import numpy as np

A = 80
B = 25

LOST = False
old_settings = termios.tcgetattr(sys.stdin)
board = np.zeros((A,B))
board[39,13]=3
board[40,13]=3
board[41,13]=3

head = [41,13]
tail = [39,13]
direction= 3
growUp = 0

# 1:UP, 2:DOWN, 3:RIGHT, 4:LEFT

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
 

def printStars(n_stars):
    for i in range(n_stars):
        print("*", end='')
    print("")

def printVerticalStars(width,heightUp):
    blankSpace=""
    for i in range(width-2):
        blankSpace = blankSpace+" "
    for i in range(heightUp):
        print("*"+blankSpace+"*")

def printBox(width,height,message):
    heightUp=int(height/2)
    printStars(width)
    printVerticalStars(width,heightUp)
    left= int(( (width-2) - len(message)) /2)
    right = int(width-2-left-len(message))
    blankSpace=""
    for i in range(left):
        blankSpace = blankSpace+" "
    left_blank=blankSpace
    blankSpace=""
    for i in range(right):
        blankSpace = blankSpace+" "
    right_blank=blankSpace
    print("*"+left_blank+message+right_blank+"*")
    printVerticalStars(width,heightUp)
    printStars(width)
    
    while True:
        char = getch()
        return char
    
        #if (char == "k"):
        #    print("Let's go!")

def ClearScreen():
    os.system('clear')  # on linux / os x


def UpdateHead():
    if direction == 1:
        head[1] -= 1
    if direction == 2:
        head[1] += 1

    
#button_delay = 0.2    
c = printBox(40,6,"Nibbles ver 0.0.0.0.1")
print(c)


try:
    tty.setcbreak(sys.stdin.fileno())

    i = 0
    while not LOST:
        #print(i)
        #i += 1

        ClearScreen()

        #READ
        if isData():
            c = sys.stdin.read(1)
            print(c)
            #if c == '\x1b':         # x1b is ESC
            #    break

        UpdateHead()
        UpdateTail()
        AddFood()
        PrintScreen()
        Wait()        

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

#while not LOST:
#    ClearScreen()
#    Read()
#    UpdateHead()
#    UpdateTail()
#    AddFood()
#    PrintScreen()
#    Wait()
    



#printBox(10,4,"OK")
#printBox(10,4,"CANCEL")









