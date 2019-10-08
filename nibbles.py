#!/usr/bin/env python3

import sys, termios, tty, os, time
import select
import numpy as np
from time import sleep

from random import random

A = 80
B = 25

LOST = False
old_settings = termios.tcgetattr(sys.stdin)
board = np.zeros((A,B))
board[39,13]=3
board[40,13]=3
board[41,13]=3
board[42,13]=3
board[43,13]=3

head = [43,13]
tail = [39,13]
direction= 3
growUp = 0

Food = False
countFood = -1

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


def UpdateHead(Food):

    x = head[0]
    y = head[1]
    
    #conditions to check the borders of the board
    if direction == 1:
        head[1] -= 1
        if head[1] < 0:
            return True, Food
            
    if direction == 2:
        head[1] += 1
        if head[1] > B-1:
            return True, Food

    if direction == 3:
        head[0] += 1
        if head[0] > A-1:
            return True, Food

    if direction == 4:
        head[0] -= 1
        if head[0] < 0:
            return True, Food

    if board[head[0],head[1]] > 0:
        return True, Food

    #check for food
    if board[head[0],head[1]] < 0:
        Food = False
    
    #updating board
    board[head[0],head[1]] = direction
    board[x,y] = direction
    
    return False, Food

def UpdateTail():
    backup_tail_direction = board[tail[0],tail[1]]
    board[tail[0],tail[1]] = 0

    if backup_tail_direction == 1:
        tail[1] -= 1

    if backup_tail_direction == 2:
        tail[1] += 1

    if backup_tail_direction == 3:
        tail[0] += 1

    if backup_tail_direction == 4:
        tail[0] -= 1
        



def PrintScreen():
    for y in range(B):
        for x in range(A):
            if board[x,y] > 0:
                print("$", end='')
            elif board[x,y] < 0:
                print(str(int(-1*board[x,y])),end="")
            else:
                print(" ",end='')
        print("");
    print(tail, str(Food))

def Wait():
    sleep(0.5)

def AddFood(countFood, Food):
    if not Food:
        x_food = int(random()*A)
        y_food = int(random()*B)
        board[x_food,y_food] = countFood
        countFood = countFood - 1
        Food = True
    return countFood, Food


    
#button_delay = 0.2    
c = printBox(40,6,"Nibbles ver 0.0.0.0.1")
print(c)


try:
    tty.setcbreak(sys.stdin.fileno())

    i = 0
    while not LOST:
        #print(i)
        #i += 1
        #READ
        if isData():
            c = sys.stdin.read(1)
            #print(c)
            if c == '\x1b':         # x1b is ESC
                break
            if c == 'w':   
                direction=1
            if c == 's':   
                direction=2
            if c == 'd':   
                direction=3
            if c == 'a':   
                direction=4
                
        LOST, Food = UpdateHead(Food)

        if LOST:
            break
        
        UpdateTail()
        countFood, Food = AddFood(countFood, Food)
        ClearScreen()
        PrintScreen()
        Wait()        

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


print("Game over!!!")

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









