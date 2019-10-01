#!/usr/bin/env python3

import sys, termios, tty, os, time
import select

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
           
#button_delay = 0.2    
c = printBox(40,6,"Nibbles ver 0.0.0.0.1")
print(c)

LOST = False
old_settings = termios.tcgetattr(sys.stdin)

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









