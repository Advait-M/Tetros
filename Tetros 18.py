#!/usr/bin/env python
"""This is a game called Tetros made with Tkinter graphics (quite similar to Tetris)."""
# Import modules
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import random
import math
import time
import cmath
import copy
import sys
import winsound

__author__ = "Advait Maybhate"
__copyright__ = "Copyright 2016, The Final Project"
__credits__ = [
    "Jason Schattman",
    "Huzaifa Arshad",
    "Gaurav Iyer",
    "Leon Fattakhov",
    "Zach Chapman"]
__license__ = "GPL"
__version__ = "18"
__maintainer__ = "Advait Maybhate"
__status__ = "Unstable Release"


# Create root in order to use tkinter
root = Tk()
root.title(string="Tetros")  # Title window with game name
instructions = Canvas(
    root,
    width=800,
    height=600,
    background="white")  # Make instructions canvas
# Make text box for user to enter speed at which tetrominoes should fall
eText = Entry(root, font="Times 20 bold", fg="green")
# Make button for user to click in order to advance to the game screen
okayB = Button(
    root,
    text="Begin!",
    font="Times 12 bold",
    command=lambda: getDifficulty())
screen = Canvas(
    root,
    width=600,
    height=525,
    background="white")  # Make main game canvas
# Make button for quitting Tetros (present in the final game statistics screen)
quitB = Button(
    root,
    text="Quit Tetros",
    font="Times 12 bold",
    command=lambda: endAll())

menubar = Menu(root)
menuB = Menu(menubar, tearoff=0)
menuB.add_command(label="Save Progress", command=lambda: save())
menuB.add_command(label="Load From File", command=lambda: loadSave())
menuB.add_command(label="Restart", command=lambda: restart())
menuB.add_command(label="Exit", command=lambda: exitB())
menubar.add_cascade(label="File", menu=menuB)
root.config(menu=menubar)
string = -1


def exitB():
    global qPressed
    try:
        if qPressed:
            endAll()
        endGame()
        qPressed = True
    except NameError:
        endAll()

def save():
    global length, clearedRows, blocks3d, blockCoords, blocks, paused, predictShape, qPressed, centres, colours, floor, counter, functions, s, score, scoreP, tetrisSong, pShapes
    try:
        temp = blockCoords
        path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[
                ("TetrosSaveFile", ".txt")], title="Save game")
        try:
            sf = open(path, "w")
            sf.write(str(clearedRows)+"\n")
            sf.write(str(len(blockCoords))+"\n")
            for i in range(0, len(blockCoords)):
                sf.write(str(len(blockCoords[i]))+"\n")
            sf.write(" ".join(map(str, blockCoords)))
            sf.write("\n")
            sf.write(" ".join(map(str, centres)))
            sf.write("\n")
            sf.write(" ".join(colours)+"\n")
            sf.write(str(counter)+"\n"+str(s)+"\n"+str(score)+"\n"+tetrisSong)
            sf.write("\n")
            sf.write(" ".join(map(str, blocks)))
            sf.write("\n")
            sf.write(str(pShapes))
        except FileNotFoundError:
            pass
    except NameError:
       messagebox.showwarning(title= 'Save Alert' , message='Sorry but you cannot save at this moment')


def turnList(l):
    x2 = l.replace("[","")
    x3 = x2.replace ("]","")
    final = []
    cur = ""
    for i in range(0, len(x3)):
        if x3[i] == ",":
            try:
                final.append(int(cur))
                cur = ""
            except ValueError:
                final.append(float(cur))
                cur = ""
        else:
            cur += x3[i]
    x3 = list(x3)
    x3.reverse()
    e = x3.index(",")
    new2 = x3[0:e]
    new2.reverse()
    temp = ""
    for i in range(0, len(new2)):
        temp += new2[i]
    try:
        final.append(int(temp))
    except ValueError:
        final.append(float(temp))
    return final

def loadSave():
    global length, clearedRows, blocks3d, blockCoords, blocks, paused, predictShape, qPressed, centres, colours, floor, counter, functions, s, score, scoreP, tetrisSong, pShapes
    try:
        if not qPressed:
            loadGame = filedialog.askopenfilename(
                defaultextension=".txt", filetypes=[
                    ("TetrosSaveFile", ".txt")], title="Load Game") # Returns Path of file
            try:
                lf = open(loadGame, "r")
                lines = lf.read()
                llist = lines.splitlines()
                clearedRows = int(llist[0])
                blockCoords = []
                curlen = int(llist[1])
                for i in range(0, curlen):
                    temp = []
                    for j in range(0, int(llist[i+2])):
                        temp.append([[], [], [], []])
                    blockCoords.append(temp)
                c = llist[curlen+2]
                x = c.replace(",","")
                x2 = x.replace("[","")
                x3 = x2.replace("]","")
                x4 = list(x3)
                nums = []
                temp = ""
                for k in range(0, len(x4)):
                    if x4[k] != " ":
                        temp += x4[k]
                    else:
                        nums.append(temp)
                        temp = ""
                x4.reverse()
                e = x4.index(" ")
                new2 = x4[0:e]
                new2.reverse()
                temp = ""
                for i in range(0, len(new2)):
                    temp += new2[i]
                nums.append(temp)
                cur = 0

                for a in range(0, len(blockCoords)):
                    if nums[cur] == "":
                        cur += 1
                        continue
                    for b in range(0, len(blockCoords[a])):
                        for c in range(0, len(blockCoords[a][b])):
                            blockCoords[a][b][c].append(float(nums[cur]))
                            cur += 1
                            blockCoords[a][b][c].append(float(nums[cur]))
                            cur += 1
                cens = llist[curlen+3]
                scens = cens.split("] [")
                centres = []
                for i in range(0, len(scens)):
                    centres.append(turnList(scens[i]))
                col = llist[curlen+4]
                newcol = col.split()
                colours = []
                for i in range(0, len(newcol)):
                    colours.append(newcol[i])
                counter = int(llist[curlen+5])
                s = float(llist[curlen+6])
                score = int(llist[curlen+7])
                tetrisSong = llist[curlen+8]
                winsound.PlaySound(tetrisSong, winsound.SND_FILENAME |
                                   winsound.SND_ASYNC | winsound.SND_LOOP)  # Loop the background music

                blockies = llist[curlen+9]
                sblocks = blockies.split("] [")
                blocks = []
                for i in range(0, len(sblocks)):
                    blocks.append(turnList(sblocks[i]))

                snext = llist[curlen+10]
                pShapes = []
                for i in range(0, len(snext)-2):
                    if snext[i] == "[":
                        pShapes.append(snext[i+2])
                    elif snext[i] == ",":
                        pShapes.append(snext[i+3])

                makeWholeCoords()
                overlay()
                showNext()
                makeTetrisRectangle()
                sidebar()
            except FileNotFoundError:
                pass

        else:
            messagebox.showwarning(title= 'Load Alert' , message='Sorry but you cannot load a save file at this moment')
    except NameError:
        try:
            loadGame = filedialog.askopenfilename(
                defaultextension=".txt", filetypes=[
                ("TetrosSaveFile", ".txt")], title="Load Game") # Returns Path of file
            lf = open(loadGame, "r")
            eText.destroy()
            okayB.destroy()
            instructions.destroy()

            # Pack screen and start the runGame proceduress
            screen.pack()
            screen.focus_set()
            s = 0
            setInitialValues()  # Set up initial values

            lines = lf.read()
            llist = lines.splitlines()
            clearedRows = int(llist[0])
            blockCoords = []
            curlen = int(llist[1])
            for i in range(0, curlen):
                temp = []
                for j in range(0, int(llist[i+2])):
                    temp.append([[], [], [], []])
                blockCoords.append(temp)
            c = llist[curlen+2]
            x = c.replace(",","")
            x2 = x.replace("[","")
            x3 = x2.replace("]","")
            x4 = list(x3)
            nums = []
            temp = ""
            for k in range(0, len(x4)):
                if x4[k] != " ":
                    temp += x4[k]
                else:
                    nums.append(temp)
                    temp = ""
            x4.reverse()
            e = x4.index(" ")
            new2 = x4[0:e]
            new2.reverse()
            temp = ""
            for i in range(0, len(new2)):
                temp += new2[i]
            nums.append(temp)
            cur = 0

            for a in range(0, len(blockCoords)):
                if nums[cur] == "":
                    cur += 1
                    continue
                for b in range(0, len(blockCoords[a])):
                    for c in range(0, len(blockCoords[a][b])):
                        blockCoords[a][b][c].append(float(nums[cur]))
                        cur += 1
                        blockCoords[a][b][c].append(float(nums[cur]))
                        cur += 1
            cens = llist[curlen+3]
            scens = cens.split("] [")
            centres = []
            for i in range(0, len(scens)):
                centres.append(turnList(scens[i]))
            col = llist[curlen+4]
            newcol = col.split()
            colours = []
            for i in range(0, len(newcol)):
                colours.append(newcol[i])
            counter = int(llist[curlen+5])
            s = float(llist[curlen+6])
            score = int(llist[curlen+7])
            tetrisSong = llist[curlen+8]
            winsound.PlaySound(tetrisSong, winsound.SND_FILENAME |
                               winsound.SND_ASYNC | winsound.SND_LOOP)  # Loop the background music

            blockies = llist[curlen+9]
            sblocks = blockies.split("] [")
            blocks = []
            for i in range(0, len(sblocks)):
                blocks.append(turnList(sblocks[i]))

            snext = llist[curlen+10]
            pShapes = []
            for i in range(0, len(snext)-2):
                if snext[i] == "[":
                    pShapes.append(snext[i+2])
                elif snext[i] == ",":
                    pShapes.append(snext[i+3])

            makeWholeCoords()
            overlay()
            showNext()
            makeTetrisRectangle()
            sidebar()
            coreGame()
        except FileNotFoundError:
            pass
def setInitialValues():
    """Initializes many variables used later on in the game."""
    global length, clearedRows, blocks3d, blockCoords, blocks, paused, predictShape, qPressed, centres, colours, floor, counter, functions, s, score, scoreP, tetrisSong
    counter = -1  # Keeps track of how many pieces have been dropped
    length = 25  # Length of a single block
    blockCoords = []  # List that holds all block coordinates
    blocks = []  # List that holds all block objects (using create_polygon)
    qPressed = False  # Keeps track of whether q/Q/quit button has been pressed
    centres = []  # List that holds all of the centres to the tetrominoes
    colours = []  # List that holds all of the colours of the tetrominoes
    floor = 500  # The y coordinate of the bottom side of the Tetros box
    score = 0  # Keeps track of the score
    scoreP = 0  # Actual text object of the score being displayed on the screen

    # Adjust background song tempo according to difficulty
    if 0.2 <= s:
        tetrisSong = "0%.wav"
    elif 0.1 < s < 0.2:
        tetrisSong = "50%.wav"
    elif s == 0.1:
        tetrisSong = "100%.wav"
    elif 0.05 <= s < 0.1:
        tetrisSong = "150%.wav"
    else:
        tetrisSong = "200%.wav"

    # List of functions to make tetrominoes
    functions = [makei, makej, makel, makeo, makes, maket, makez]
    # Initializing a variable to assign to the next shape tetromino (top right
    # of the interface)
    predictShape = 0
    paused = False  # Keeps track of whether the pause button has been pressed
    clearedRows = 0  # Keeps track of how many rows have been cleared
    blocks3d = PhotoImage(file="End.gif")  # Final game screen background image


def hexadecimal():
    hexadecimals = "#"
    for i in range(0, 6):
        a = random.randint(48, 70)
        while 58 <= a <= 64:
            a = random.randint(48, 70)
        hexadecimals += chr(a)
    return hexadecimals

# MAKE GRID OVERLAY (only enable if developing)


def overlay():
    """Makes a grid or dot overlay."""
    global gridOverlay, dotOverlay
    # Boolean that controls whether grid overlay should be present (used for
    # developing)
    gridOverlay = False

    if gridOverlay:
        spacing = 25  # Spacing between grid lines
        for x in range(0, 600, spacing):  # Draw vertical lines
            screen.create_line(x, 10, x, 800, fill="black")
            screen.create_text(
                x,
                0,
                text=str(x),
                font="Times 8",
                anchor=N)  # Label lines with coordinates

        for y in range(0, 525, spacing):  # Draw horizontal lines
            screen.create_line(20, y, 800, y, fill="black")
            screen.create_text(
                4,
                y,
                text=str(y),
                font="Times 8",
                anchor=W)  # Label lines with coordinates

    dotOverlay = True  # Boolean that controls whether dot overlay should be present

    if dotOverlay:
        spacing = 25  # Spacing between dots
        # Draw dot grid on Tetros box
        for x in range(25, 300, spacing):
            for y in range(0, 525, spacing):
                screen.create_oval(x - 1, y - 1, x + 1, y + 1, fill="black")

        # Draw dot grid on "Next Shape" box
        for x in range(400, 525, spacing):
            for y in range(125, 200, spacing):
                screen.create_oval(x - 1, y - 1, x + 1, y + 1, fill="black")


# COMPLEX NUMBER METHOD
def rotatePoint(point, centre, thetaDegrees):
    """Rotates given point around the given centre by the given angle."""
    x = point[0]  # Pull out x coordinate
    y = point[1]  # Pull out y coordinate
    thetaRadians = math.radians(thetaDegrees)  # Convert degrees to radians
    # Express angle as a complex number (for calculations)
    thetac = cmath.exp(thetaRadians * 1j)
    centreX = centre[0]  # Pull out x coordinate of centre
    centreY = centre[1]  # Pull out y coordinate of centre

    # Create a complex expression to represent the centre
    centrec = complex(centreX, centreY)
    # v consists of the x and y values of the rotated coordinate in its real
    # and imaginary parts respectively
    v = thetac * (complex(x, y) - centrec) + centrec
    newX = v.real  # Pull out new x coordinate (rotated)
    newY = v.imag  # Pull out new y coordinate (rotated)

    return [newX, newY]  # Return list of the rotated coordinates


def makeWholeCoords():
    """Deletes all objects on screen and redraws them using the coordinates list."""
    global blockCoords, blocks, colours
    # Delete all objects on the screen (to make sure all objects get updated)
    screen.delete(ALL)
    # Go through blockCoords and redraw all the blocks that it contains the
    # coordinates for
    for i in range(0, len(blockCoords) - 1):
        for g in range(0, len(blockCoords[i])):
            coords = []
            for p in range(0, 4):
                coords.append(blockCoords[i][g][p])
            blocks[i][g] = screen.create_polygon(coords, fill=colours[i], outline="black", width="2")

# ROTATE WHOLE POLYGON


def rotatePolygon(polygon, centre, angleDegrees):
    """Rotates given polygon around given centre by given angle."""
    # Rotate all points in the polygon using the rotatePoint function
    for i in range(0, len(polygon)):
        polygon[i] = rotatePoint(polygon[i], centre, angleDegrees)
    return polygon  # Return the new polygon coordinates


def makeCoords(x, y):
    """Returns the coordinates of a block with the given coordinates as its top left corner."""
    return [[x, y], [x + 25, y], [x + 25, y + 25], [x, y + 25]]


def makePolygon(coords, colour):
    """Draws four blocks using given coordinates and given colour."""
    block1 = screen.create_polygon(
        coords[0],
        fill=colour,
        outline="black",
        width="2")
    block2 = screen.create_polygon(
        coords[1],
        fill=colour,
        outline="black",
        width="2")
    block3 = screen.create_polygon(
        coords[2],
        fill=colour,
        outline="black",
        width="2")
    block4 = screen.create_polygon(
        coords[3],
        fill=colour,
        outline="black",
        width="2")
    return [block1, block2, block3, block4]  # Return the four blocks in a list


def makei(x, y, real=True):
    """Makes an I shape tetromino."""
    global blockCoords, blocks, length, centres, colours, predictShape
    if real:  # If real is true information is added to the arrays, otherwise it is to be made for the "Next Shape" box
        coords = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        coords.append(makeCoords(x - length * 2, y - length))
        coords.append(makeCoords(x - length, y - length))
        coords.append(makeCoords(x, y - length))
        coords.append(makeCoords(x + length, y - length))
        # Append the coordinates to the main blockCoords list
        blockCoords.append(coords)
        # Create the polygon on the screen
        blocks.append(makePolygon(coords, "cyan"))
        # Append the centre of the polygon to the centres list
        centres.append([x, y])
        # Append the colour of the polygon to the colours list
        colours.append("cyan")
    else:
        c = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        c.append(makeCoords(x - length * 2, y - length))
        c.append(makeCoords(x - length, y - length))
        c.append(makeCoords(x, y - length))
        c.append(makeCoords(x + length, y - length))
        # Create polygon on the screen and assign it to predictShape
        predictShape = makePolygon(c, "cyan")


def makej(x, y, real=True):
    """Makes an J shape tetromino."""
    global blockCoords, blocks, length, centres, colours, predictShape
    if real:  # If real is true information is added to the arrays, otherwise it is to be made for the "Next Shape" box
        coords = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        coords.append(makeCoords(x - length * 3 / 2, y - length * 3 / 2))
        coords.append(makeCoords(x - length * 3 / 2, y - length / 2))
        coords.append(makeCoords(x - length / 2, y - length / 2))
        coords.append(makeCoords(x + length / 2, y - length / 2))
        # Append the coordinates to the main blockCoords list
        blockCoords.append(coords)
        # Create the polygon on the screen
        blocks.append(makePolygon(coords, "blue"))
        # Append the centre of the polygon to the centres list
        centres.append([x, y])
        # Append the colour of the polygon to the colours list
        colours.append("blue")
    else:
        c = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        c.append(makeCoords(x - length * 3 / 2, y - length * 3 / 2))
        c.append(makeCoords(x - length * 3 / 2, y - length / 2))
        c.append(makeCoords(x - length / 2, y - length / 2))
        c.append(makeCoords(x + length / 2, y - length / 2))
        # Create polygon on the screen and assign it to predictShape
        predictShape = makePolygon(c, "blue")


def makel(x, y, real=True):
    """Makes an L shape tetromino."""
    global blockCoords, blocks, length, centres, colours, predictShape
    if real:  # If real is true information is added to the arrays, otherwise it is to be made for the "Next Shape" box
        coords = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        coords.append(makeCoords(x - length * 3 / 2, y - length / 2))
        coords.append(makeCoords(x - length / 2, y - length / 2))
        coords.append(makeCoords(x + length / 2, y - length / 2))
        coords.append(makeCoords(x + length / 2, y - length * 3 / 2))
        # Append the coordinates to the main blockCoords list
        blockCoords.append(coords)
        # Create the polygon on the screen
        blocks.append(makePolygon(coords, "orange"))
        # Append the centre of the polygon to the centres list
        centres.append([x, y])
        # Append the colour of the polygon to the colours list
        colours.append("orange")
    else:
        c = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        c.append(makeCoords(x - length * 3 / 2, y - length / 2))
        c.append(makeCoords(x - length / 2, y - length / 2))
        c.append(makeCoords(x + length / 2, y - length / 2))
        c.append(makeCoords(x + length / 2, y - length * 3 / 2))
        # Create polygon on the screen and assign it to predictShape
        predictShape = makePolygon(c, "orange")


def makeo(x, y, real=True):
    """Makes an O shape tetromino."""
    global blockCoords, blocks, length, centres, colours, predictShape
    if real:  # If real is true information is added to the arrays, otherwise it is to be made for the "Next Shape" box
        coords = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        coords.append(makeCoords(x - length, y - length))
        coords.append(makeCoords(x, y - length))
        coords.append(makeCoords(x - length, y))
        coords.append(makeCoords(x, y))
        # Append the coordinates to the main blockCoords list
        blockCoords.append(coords)
        # Create the polygon on the screen
        blocks.append(makePolygon(coords, "yellow"))
        # Append the centre of the polygon to the centres list
        centres.append([x, y])
        # Append the colour of the polygon to the colours list
        colours.append("yellow")
    else:
        c = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        c.append(makeCoords(x - length, y - length))
        c.append(makeCoords(x, y - length))
        c.append(makeCoords(x - length, y))
        c.append(makeCoords(x, y))
        # Create polygon on the screen and assign it to predictShape
        predictShape = makePolygon(c, "yellow")


def makes(x, y, real=True):
    """Makes an S shape tetromino."""
    global blockCoords, blocks, length, centres, colours, predictShape
    if real:  # If real is true information is added to the arrays, otherwise it is to be made for the "Next Shape" box
        coords = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        coords.append(makeCoords(x - length * 3 / 2, y - length / 2))
        coords.append(makeCoords(x - length / 2, y - length / 2))
        coords.append(makeCoords(x - length / 2, y - length * 3 / 2))
        coords.append(makeCoords(x + length / 2, y - length * 3 / 2))
        # Append the coordinates to the main blockCoords list
        blockCoords.append(coords)
        # Create the polygon on the screen
        blocks.append(makePolygon(coords, "green"))
        # Append the centre of the polygon to the centres list
        centres.append([x, y])
        # Append the colour of the polygon to the colours list
        colours.append("green")
    else:
        c = []  # Initialize coordinates list
        # Append coordinates to the list according to the shape being created
        c.append(makeCoords(x - length * 3 / 2, y - length / 2))
        c.append(makeCoords(x - length / 2, y - length / 2))
        c.append(makeCoords(x - length / 2, y - length * 3 / 2))
        c.append(makeCoords(x + length / 2, y - length * 3 / 2))
        # Create polygon on the screen and assign it to predictShape
        predictShape = makePolygon(c, "green")


def maket(x, y, real=True):
    """Makes an T shape tetromino."""
    global blockCoords, blocks, length, centres, colours, predictShape
    if real:  # If real is true information is added to the arrays, otherwise it is to be made for the "Next Shape" box
        coords = []  # Initialize coordinates list
        coords.append(makeCoords(x - length * 3 / 2, y - length / 2))
        coords.append(makeCoords(x - length / 2, y - length / 2))
        coords.append(makeCoords(x - length / 2, y - length * 3 / 2))
        coords.append(makeCoords(x + length / 2, y - length / 2))
        # Append the coordinates to the main blockCoords list
        blockCoords.append(coords)
        # Create the polygon on the screen
        blocks.append(makePolygon(coords, "magenta"))
        # Append the centre of the polygon to the centres list
        centres.append([x, y])
        # Append the colour of the polygon to the colours list
        colours.append("magenta")
    else:
        c = []  # Initialize coordinates list
        c.append(makeCoords(x - length * 3 / 2, y - length / 2))
        c.append(makeCoords(x - length / 2, y - length / 2))
        c.append(makeCoords(x - length / 2, y - length * 3 / 2))
        c.append(makeCoords(x + length / 2, y - length / 2))
        # Create polygon on the screen and assign it to predictShape
        predictShape = makePolygon(c, "magenta")


def makez(x, y, real=True):
    """Makes an Z shape tetromino."""
    global blockCoords, blocks, length, centres, colours, predictShape
    if real:  # If real is true information is added to the arrays, otherwise it is to be made for the "Next Shape" box
        coords = []  # Initialize coordinates list
        coords.append(makeCoords(x - length * 3 / 2, y - length * 3 / 2))
        coords.append(makeCoords(x - length / 2, y - length * 3 / 2))
        coords.append(makeCoords(x - length / 2, y - length / 2))
        coords.append(makeCoords(x + length / 2, y - length / 2))
        # Append the coordinates to the main blockCoords list
        blockCoords.append(coords)
        # Create the polygon on the screen
        blocks.append(makePolygon(coords, "red"))
        # Append the centre of the polygon to the centres list
        centres.append([x, y])
        # Append the colour of the polygon to the colours list
        colours.append("red")
    else:
        c = []  # Initialize coordinates list
        c.append(makeCoords(x - length * 3 / 2, y - length * 3 / 2))
        c.append(makeCoords(x - length / 2, y - length * 3 / 2))
        c.append(makeCoords(x - length / 2, y - length / 2))
        c.append(makeCoords(x + length / 2, y - length / 2))
        # Create polygon on the screen and assign it to predictShape
        predictShape = makePolygon(c, "red")


def makeScore():
    """Deletes previous score from screen and updates it."""
    global score, scoreP, qPressed
    screen.delete(scoreP)  # Delete previous score that is on the screen
    if not qPressed:  # If the main game is still running
        # Create the new score on the screen
        scoreP = screen.create_text(
            450,
            200,
            text="Score: " +
            str(score),
            font="Times 20 bold")  # Draw new score on the screen


def checkFloor():
    """Checks if tetromino is about to hit the floor, returns True if it is and False otherwise."""
    global blockCoords, floor
    # Go through all the y coordinates in the current falling tetromino and
    # check if any of them are the same as the floor
    for i in range(0, 4):
        for e in range(0, 4):
            if blockCoords[-1][i][e][1] == floor:
                return True  # Return true if any y coordinate is the same as the floor
    return False  # Otherwise, return false


def checkWalls():
    """Checks if tetromino is about to hit a wall, if it is then it will return which wall it is about to hit."""
    global blockCoords
    # Go through all the x coordinates in the current falling tetromino
    for i in range(0, 4):
        for u in range(0, 4):
            # Check if any x coordinate is the same as the left wall
            if blockCoords[-1][i][u][0] < 50:
                return "left"  # Return whic wall it is about to hit

            # Check if any x coordinate is the same as the right wall
            if blockCoords[-1][i][u][0] > 250:
                return "right"  # Return which wall it is about to hit


def crash(coord=1, value=25):
    """Checks if tetromino is about to crash into another tetromino that has been placed."""
    global blockCoords, blocks
    hit = False  # Initialize the hit variable

    if checkFloor():  # If about to hit the floor then return True
        return True

    if len(blockCoords) > 1:  # If this is not the first tetromino
        # Add value to the x or y coordinate (depends on function parameters)
        for n in range(0, 4):
            for m in range(0, 4):
                blockCoords[-1][n][m][coord] += value

        # Check if any block in the falling tetromino has the same exact coordinates as any block that has already been placed
        # In other words, check if any block overlaps a block that has already
        # been placed
        for g in range(0, len(blockCoords) - 1):
            for w in range(0, len(blockCoords[g])):
                for v in range(0, 4):
                    if equalIgnoreOrder(blockCoords[g][w], blockCoords[-1][v]):
                        hit = True  # If it overlaps a block already placed then set hit to true

        # Return the coordinates to their original values
        for j in range(0, 4):
            for k in range(0, 4):
                blockCoords[-1][j][k][coord] -= value

        # Return true if hit is true
        if hit:
            return True

    # If no conditions are met the return false
    return False


def getKey(item):
    """Returns index 1 of the given object."""
    return item[1]


def checkRow():
    """Checks if a row is to be cleared, if it is then it clears it."""
    global blockCoords, score, blocks, clearedRows
    ys = []  # Initialize list to keep track of y coordinates
    addKeys = []
    # Append all y coordinates from the blocks already placed to the ys list
    for i in range(0, len(blockCoords) - 1):
        for u in range(0, len(blockCoords[i])):
            ys.append(min([blockCoords[i][u][0][1], blockCoords[i][u][1][
                      1], blockCoords[i][u][2][1], blockCoords[i][u][3][1]]))
    # Make a dictionary of the frequency of y values
    yds = dict((i, ys.count(i)) for i in ys)
    for e in yds:  # Loop through yds
        toDel = []  # Initialize list to keep track of blocks to delete
        explodeCentres = []
        if yds[e] == 10:
            for p in range(0, len(blockCoords) - 1):
                for k in range(0, len(blockCoords[p])):
                    # Check if block is part of row being deleted using its top
                    # y coordinate
                    if e == min([blockCoords[p][k][0][1], blockCoords[p][k][1][
                                1], blockCoords[p][k][2][1], blockCoords[p][k][3][1]]):
                        centreY = e + 12.5  # Calculate the block's centre y coordinate
                        topX = min([blockCoords[p][k][0][0], blockCoords[p][k][1][0], blockCoords[p][
                                   k][2][0], blockCoords[p][k][3][0]])  # Find its left x coordinate
                        centreX = topX + 12.5  # Calculate the block's centre x coordinate
                        # Add centre coordinates to explodeCentres array
                        explodeCentres.append([centreX, centreY])
                        toDel.append([p, k])  # Add its information to toDel
                    # Check if the block is above the row being deleted
                    if e > min([blockCoords[p][k][0][1], blockCoords[p][k][1][
                               1], blockCoords[p][k][2][1], blockCoords[p][k][3][1]]):
                        for b in range(0, 4):
                            # Update dictionary value for that y coordinate key
                            # (decrease its frequency count by 1)
                            yds[blockCoords[p][k][b][1]] -= 1
                            # Make block fall down by 25 pixels
                            blockCoords[p][k][b][1] += 25
                            try:
                                # Update dictionary value for that y coordinate
                                # key (increase its frequency count by 1)
                                yds[blockCoords[p][k][b][1]] += 1
                            except KeyError:
                                pass  # If key is not in dictionary then pass

            # Create a deep copy of blockCoords (this one will not be edited to
            # avoid indexing errors)
            blockCoords2 = copy.deepcopy(blockCoords)

            # Sort toDel by the second value in each nested list
            toDel2 = sorted(toDel, key=getKey)
            # Reverse toDel2 (delete the highest indices first to avoid
            # indexing errors)
            toDel3 = toDel2[::-1]

            # Initialize variables for the mini explosions
            xP = []  # Array to store particle x coordinates
            yP = []  # Array to store particle y coordinates
            # Array to store particle objects (being displayed on screen)
            particles = []
            # The angle that they move in (relative to the point they explode
            # from)
            angles = []
            xSizes = []  # How wide the particles are (half of their width)
            ySizes = []  # How tall the particles are (half of their height)
            r = []  # Radius of particles (from the point they explode from)
            rSpeeds = []  # Speed of particles

            # Fill up the arrays for all 10 blocks being deleted
            for blockNum in range(0, 10):
                # Use temporary arrays so the entire list can be appended to
                # the main array later (better for indexing)
                rTemp = []
                xSizesTemp = []
                ySizesTemp = []
                rSpeedsTemp = []
                particlesTemp = []
                anglesTemp = []
                xPTemp = []
                yPTemp = []

                # Make information for 25 particles for each block
                for particleNum in range(0, 25):
                    xPTemp.append(0)
                    yPTemp.append(0)
                    dAngle = random.randint(1, 360)
                    rAngle = math.radians(dAngle)
                    anglesTemp.append(rAngle)
                    rTemp.append(random.randint(-15, 15))
                    xSizesTemp.append(random.randint(1, 4))
                    ySizesTemp.append(random.randint(1, 4))
                    rSpeedsTemp.append(random.randint(-15, 15))
                    while rSpeedsTemp[particleNum] == 0:
                        rSpeedsTemp[particleNum] = random.randint(-15, 15)
                    particlesTemp.append(0)

                # Append temporary arrays to the main array
                r.append(rTemp)
                xSizes.append(xSizesTemp)
                ySizes.append(ySizesTemp)
                rSpeeds.append(rSpeedsTemp)
                particles.append(particlesTemp)
                angles.append(anglesTemp)
                xP.append(xPTemp)
                yP.append(yPTemp)

            for w in range(0, 5):  # Show explosion for 5 frames
                for i in range(
                        0, 10):  # Loop through the 10 explosions, one for each block being deleted
                    for q in range(
                            0, 25):  # Loop through the particles in each explosion (25)
                        # Use trigonometry to calculate te x and y position of
                        # the specific particle
                        xP[i][q] = explodeCentres[i][0] + r[i][q] * math.cos(angles[i][q])
                        yP[i][q] = explodeCentres[i][1] - r[i][q] * math.sin(angles[i][q])
                        # Increase the particles radius by whatever speed it is
                        # going at
                        r[i][q] = r[i][q] + rSpeeds[i][q]
                        # Draw the particle on the screen
                        particles[i][q] = screen.create_oval(
                            xP[i][q] - xSizes[i][q],
                            yP[i][q] - ySizes[i][q],
                            xP[i][q] + xSizes[i][q],
                            yP[i][q] + ySizes[i][q],
                            fill=hexadecimal())

                # Update screen and sleep for a bit (for animation effect)
                screen.update()
                time.sleep(0.02)

                for i in range(
                        0, 10):  # Loop through the 10 explosions, one for each block being deleted
                    for q in range(
                            0, 25):  # Loop through the particles in each explosion (25)
                        # Delete the particle (for animation effect)
                        screen.delete(particles[i][q])

            # Remove the specific block coordinates from blockCoords using
            # toDel3 and blockCoords2
            for r in range(0, len(toDel3)):
                blockCoords[
                    toDel3[r][0]].remove(
                    blockCoords2[
                        toDel3[r][0]][
                        toDel3[r][1]])

            makeWholeCoords()  # Update the graphics of all the blocks
            showNext()  # Show the next shape (it got deleted in makeWholeCoords)
            overlay()  # Show the dot overlay (it got deleted in makeWholeCoords)
            makeTetrisRectangle()  # Show the Tetros box (it got deleted in makeWholeCoords)
            sidebar()  # Show sidebar (it got deleted in makeWholeCoords)

            score += 20  # Increase score by 20
            clearedRows += 1  # Increase amount of rows cleared by 1


def endAll():
    """Destroys the game and plays an exit sound"""
    # Destroy root
    root.destroy()

    # Play exit sound
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    sys.exit()  # Raise SystemExit exception to exit the program


def endGame():
    """Shows the user a screen with their final statistics and then destroys the game."""
    global qPressed, screen, tetros, clearedRows, score, blocks3d
    qPressed = True  # Make sure qPressed is true so game does not run

    screen.delete(ALL)  # Delete all items on the screen

    # Create background
    screen.create_image(300, 300, image=blocks3d)

    # Show user final score
    # Create white rectangle behind text to make sure text is legible
    screen.create_rectangle(-10, 225, 610, 275, fill="white", outline="white")
    screen.create_text(
        300,
        250,
        text="Your final score is: " +
        str(score) +
        ". Thank you for playing Tetros!",
        font="Times 18 bold")

    comment = ""  # Initialize comment

    # Depending on amount of rows cleared make rowForm (plural or singular)
    if clearedRows == 1:
        rowForm = " row. "
    else:
        rowForm = " rows. "

    # If the user cleared more than one row then say "Nice job!"
    if clearedRows > 0:
        comment = "Nice job!"

    # Display amount of rows cleared and maybe a comment to the user
    # Create white rectangle behind text to make sure text is legible
    screen.create_rectangle(-10, 375, 610, 425, fill="white", outline="white")
    screen.create_text(
        300,
        400,
        text="You cleared " +
        str(clearedRows) +
        rowForm +
        comment,
        font="Times 18 bold")

    # Display Tetros logo
    screen.create_image(300, 100, image=tetros)

    # Display "Quit Tetros" button
    quitB.config(bd=5)
    quitB_window = screen.create_window(300, 470, window=quitB)

    # Refresh screen
    screen.update()


def equalIgnoreOrder(a, b):
    """Checks if objects in list a are the same as in list b considering order does not matter."""
    if len(a) != len(
            b):  # If the lengths of the lists are not equal then their elements are not equal for sure
        return False
    unmatched = list(b)  # Create a list of b (so the original b stays intact)

    for element in a:  # Loop through list a
        try:
            # Try to remove the current element in list a from unmatched
            unmatched.remove(element)
        except ValueError:  # If the element cannot be removed then return False
            return False
    # Else return the opposite of unmatched (returns True when list is empty
    # which it will be)
    return not unmatched


def makeTetrisRectangle():
    """Makes the Tetros box in which tetrominoes are placed."""
    screen.create_rectangle(25, 0, 275, 500, fill=None,
                            outline="black", width="3")


def coverNext():
    """Covers the previous 'next' shape."""
    global length
    screen.create_polygon(
        450 - length * 2,
        150 - length,
        450 + length * 2,
        150 - length,
        450 + length * 2,
        150 + length * 3 / 2,
        450 - length * 2,
        150 + length * 3 / 2,
        fill="white",
        outline="white",
        width=2)


def showNext():
    """Draws the next shape that is coming."""
    global pShapes, counter, functions, predictShape
    if not qPressed:  # If the main game is still running
        coverNext()  # Cover previous "next shape"
        screen.create_text(
            450,
            100,
            text="Next Shape:",
            font="Times 20 bold")  # Create "next shape" text
        shapeN = pShapes[counter % 7 + 1]  # Get the next shape name
        call = "make" + shapeN  # Set call to the function name

        # Loop through the functions list
        for p in range(0, len(functions)):
            # If it is the function we want then make the next shape object
            if call == functions[p].__name__:
                # An I-shape tetromino or O-shape tetromino require different x
                # and y coordinates when compared to the others (they have
                # different centres)
                if shapeN == "i" or shapeN == "o":
                    functions[p](450, 150, real=False)
                else:
                    functions[p](462.5, 162.5, real=False)
                # Break the for loop for efficiency (don't need to loop for no
                # reason)
                break

        overlay()  # Redraw dot overlay


def getRandomShape():
    """Draws a random tetromino above the screen (there are two hidden rows above the Tetros box)."""
    global counter, pShapes, blocks, score, nextShape, functions
    # If this is not the first tetromino being created then make sure the current tetromino is updated according to its position in blockCoords
    # This is needed because blockCoords may have been updated and a crash may
    # have been detected but the graphical tetromino may not have been updated
    if len(blocks) > 1:
        for j in range(0, 4):
            screen.delete(blocks[-1][j])
        blocks[-1] = makePolygon(blockCoords[-1], colours[-1])

    # Increment counter
    counter += 1

    if counter == 0:  # If it is the first shape
        pShapes = ["i", "j", "l", "o", "s", "t", "z"]  # Possible shapes array
        random.shuffle(pShapes)  # Randomize pShapes array
        showNext()  # Show the next tetromino in the "next shape" area

    if (counter + 1) % 7 == 0:  # Just before reaching the last element of the pShapes list (every time it reaches the sixth element)
        # Create a temporary array of possible shapes
        tempShapes = ["i", "j", "l", "o", "s", "t", "z"]
        # Assign nextShape to the last element in the current pShapes array
        nextShape = pShapes[-1]
        # Remove the last element from the tempShapes array
        tempShapes.remove(nextShape)
        # Create a tempStart array that just has one element which is nextShape
        tempStart = [nextShape]
        random.shuffle(tempShapes)  # Randomize the tempShapes array
        # Add the tempShapes array to the end of the tempStart array
        tempStart.extend(tempShapes)
        pShapes = tempStart  # Assign pShapes to the tempStart array
        counter = 7  # Set counter to 7

    # Choose a shape from pShapes (using modulus to make sure that there are
    # no index errors)
    shape = pShapes[counter % 7]
    call = "make" + shape  # Call is a string that is a function name
    for p in range(0, len(functions)):  # Go through the list of functions
        if call == functions[
                p].__name__:  # If call matches with the current function's name
            # Depending on the shape, call the function with x and y
            # coordinates (I and O tetrominoes has different centres compared
            # to the rest)
            if shape == "i" or shape == "o":
                functions[p](150, -length * 2)
            else:
                functions[p](162.5, -length * 3 / 2)

    if crash():  # If the shape that has just spawned cannot move
        endGame()  # End the game
    else:
        score += 8  # Otherwise increase the score by 8 (2 points per block)


def animateShape():
    """Animates current tetromino as it falls (if it is about to crash then it stops it)."""
    global blockCoords, blocks, qPressed, centres, colours, floor, crashed

    checkRow()  # Checks if a row is to be deleted

    if crash():  # If the current shape has crashed then it gets the next tetromino to fall
        getRandomShape()
        showNext()
    else:
        for i in range(0, 4):
            for u in range(0, 4):
                # Make tetromino fall by 25 pixels
                blockCoords[-1][i][u][1] += 25

        # Increase the y coordinate of the centre of tetromino by 25 pixels
        centres[-1][1] += 25

        for j in range(0, 4):
            screen.delete(blocks[-1][j])  # Delete previous frame
        # Create updated tetromino on the screen
        blocks[-1] = makePolygon(blockCoords[-1], colours[-1])

def ascendSky():
    global blockCoords, blocks, centres, colours
    rewindSound = "rewind.wav"
    winsound.PlaySound(rewindSound, winsound.SND_FILENAME|winsound.SND_ASYNC)
    for r in range(0, 20):
        for a in range(0, len(blockCoords)):
            for b in range(0, len(blockCoords[a])):
                for c in range(0, len(blockCoords[a][b])):
                    blockCoords[a][b][c][1] -= 25
        for i in range(0, len(centres)):
            centres[i][1] -= 25
        for h in range(0, len(blocks)):
            for j in range(0, 4):
                screen.delete(blocks[h][j])
        for w in range(0, len(blocks)):
            blocks[w] = makePolygon(blockCoords[w], colours[w])
        screen.update()
        time.sleep(0.1)

def makeInstructions():
    """Draws images and text on the instructions screen."""
    global instructions, tetros, background
    # Create background image
    instructions.create_image(400, 300, image=background)
    instructions.create_image(400, 100, image=tetros)  # Create Tetros logo
    # Create white rectangle background for text
    instructions.create_rectangle(40, 200, 750, 560, fill="white")

    # Create instructions for the user
    instructions.create_text(
        400,
        230,
        text="WELCOME TO TETROS!",
        font="Times 20 bold underline",
        fill="#008855")
    instructions.create_text(
        400,
        275,
        text="INSTRUCTIONS",
        font="Times 18 bold")
    instructions.create_text(
        400,
        300,
        text="Objective: Try to fit as many tetrominoes as possible on the screen by clearing rows!",
        font="Times 11 bold")
    instructions.create_text(
        400,
        325,
        text="Press the UP key or X to rotate the tetromino clockwise.",
        font="Times 11 bold")
    instructions.create_text(
        400,
        350,
        text="Press Z to rotate the tetromino anti-clockwise.",
        font="Times 11 bold")
    instructions.create_text(
        400,
        375,
        text="Press the DOWN key to accelerate the current tetromino.",
        font="Times 11 bold")
    instructions.create_text(
        400,
        400,
        text="Press the LEFT or RIGHT keys to move the tetromino in their respective directions.",
        font="Times 11 bold")
    instructions.create_text(
        400,
        425,
        text="Press Q to quit the game.",
        font="Times 11 bold")
    instructions.create_text(
        400,
        450,
        text="Press P to pause/unpause the game.",
        font="Times 11 bold")
    instructions.create_text(
        400,
        475,
        text="Scoring: 8 points for a new tetromino, 20 points for a cleared row, and 1 point for accelerating the tetromino.",
        font="Times 11 bold")
    instructions.create_text(
        400,
        500,
        text="Tip: Accelerate a tetromino if you are confident it is in the right column for free points!",
        font="Times 10 bold")

    # Instruct user to enter speed that they want tetrominoes to fall at
    instructions.create_text(
        400,
        525,
        text="Enter speed at which tetrominoes should fall (in seconds) - must be non-negative:",
        font="Times 14 bold underline")
    instructions.create_text(
        400,
        550,
        text="Approximate difficulty for different speeds (in seconds): Easy - 0.5 Medium - 0.3 Hard - 0.1",
        font="Times 12 bold")


def getDifficulty():
    """Gets the difficulty from the user. If they have not entered a non-negative number it does nothing."""
    global s, string
    string = eText.get()  # Get the text the user has entered

    try:
        s = float(string)  # Try to make the string entered a float
        if s >= 0:  # If it is  non-negative
            # Destroy the instructions screen, the text box and the "Next"
            # button
            eText.destroy()
            okayB.destroy()
            instructions.destroy()

            # Pack screen and start the runGame proceduress
            screen.pack()
            screen.focus_set()
            root.after(1, runGame)

    except ValueError:  # If it is not a float then pass
        pass

def restart():
    global scoreP
    if string == -1:
        messagebox.showwarning(title= 'Restart Alert' , message='You currently do not have a game to restart')
    try:
        s = float(string)  # Try to make the string entered a float
        ascendSky()
        if s >= 0:  # If it is  non-negative
            screen.delete(scoreP)
            screen.delete(ALL)

            # Start the runGame proceduress
            root.after(1, runGame)

    except ValueError:  # If it is not a float then pass
        pass


def sidebar():
    """Draws the side panel in the main game screen, specifically the controls."""
    global left, tetrosSmall, right, up, down, xImage, zImage, pImage, qImage, rImage
    screen.create_text(
        440,
        275,
        text="CONTROLS",
        font="Times 13 bold underline")  # Create "CONTROLS" headline

    # Create images of the controls
    screen.create_image(300, 375, image=left)
    screen.create_image(300, 325, image=right)
    screen.create_image(300, 425, image=up)
    screen.create_image(300, 475, image=down)
    screen.create_image(470, 375, image=pImage)
    screen.create_image(470, 425, image=qImage)
    screen.create_image(470, 325, image=zImage)
    screen.create_image(350, 425, image=xImage)
    screen.create_image(470, 475, image=rImage)

    # Explain what each control does
    screen.create_text(535, 315, text="Rotate", font="Times 10 bold")
    screen.create_text(535, 335, text="Anti-clockwise", font="Times 10 bold")
    screen.create_text(535, 375, text="Pause/Unpause", font="Times 10 bold")
    screen.create_text(535, 425, text="Quit Game", font="Times 10 bold")
    screen.create_text(350, 375, text="Move Left", font="Times 10 bold")
    screen.create_text(360, 325, text="Move Right", font="Times 10 bold")
    screen.create_text(410, 415, text="Rotate", font="Times 10 bold")
    screen.create_text(410, 435, text="Clockwise", font="Times 10 bold")
    screen.create_text(385, 475, text="Accelerate Tetromino",font="Times 10 bold")
    screen.create_text(535, 475, text="Restart Game", font= "Times 10 bold")

    # Create Tetros logo
    screen.create_image(440, 45, image=tetrosSmall)
    # Redraw interface buttons (pause and quit)
    interfaceButtons()


def coreGame():
    """Calls the core functions of the game."""
    global s, paused, qPressed
    while not qPressed and not paused:  # Run while not paused and not quitted
        animateShape()  # Animate shape falling down
        makeScore()  # Update score
        screen.update()  # Update screen
        time.sleep(s)  # Sleep for animation effect


def keyDownHandler(event):
    """Handles any key being pressed by the user during the game. It operates according to the key pressed and the state of the current tetromino."""
    global blockCoords, blocks, paused, qPressed, centres, colours, score
    # Make sure game is not paused, tetromino is not about to crash and that
    # the key pressed is to rotate the tetromino
    if not paused and not crash() and (event.keysym == "Up" or event.keysym ==
                                       "x" or event.keysym == "X" or event.keysym == "z" or event.keysym == "Z"):
        # Initialize hit
        hit = False

        for i in range(0, 4):
            # Depending on the key pressed, rotate tetromino clockwise or
            # anti-clockwise
            if event.keysym == "z" or event.keysym == "Z":
                blockCoords[-1][i] = rotatePolygon(
                    blockCoords[-1][i], centres[-1], -90)
            else:
                blockCoords[-1][i] = rotatePolygon(
                    blockCoords[-1][i], centres[-1], 90)

        # Make sure that the rotated tetromino is not going through the floor
        # or any wall
        if not checkWalls() is None or checkFloor():
            hit = True

        # If this is not the first tetromino and hit is not already true then
        # check to see if rotating it will cause it to overlap already placed
        # blocks
        if len(blockCoords) > 1 and not hit:
            for i in range(0, len(blockCoords) - 1):
                for u in range(0, len(blockCoords[i])):
                    for g in range(0, 4):
                        # Check if the blocks are the same (order of points
                        # does not matter in this case)
                        if equalIgnoreOrder(
                                blockCoords[i][u], blockCoords[-1][g]):
                            hit = True
                            break  # Break for efficiency

        if not hit:  # If the rotating the tetromino will not cause errors
            # Delete previous tetromino from the screen
            for j in range(0, 4):
                screen.delete(blocks[-1][j])

            # Delete previous tetromino from the blocks array
            del blocks[-1]

            # Append the new tetromino to the blocks array (also creates new
            # tetromino on the screen)
            blocks.append(makePolygon(blockCoords[-1], colours[-1]))
        else:  # If rotating the tetromino will cause errors
            # Rotate tetromino back to its original position
            for i in range(0, 4):
                # Rotate block depending on the key that was pressed
                if event.keysym == "z" or event.keysym == "Z":
                    blockCoords[-1][i] = rotatePolygon(
                        blockCoords[-1][i], centres[-1], 90)
                else:
                    blockCoords[-1][i] = rotatePolygon(
                        blockCoords[-1][i], centres[-1], -90)

    # If game is not paused, the left arrow key has been pressed, the
    # tetromino will not crash if it is moved left, the tetromino is not about
    # to crash and the tetromino is not hitting the left wall
    elif not paused and event.keysym == "Left" and not crash(coord=0, value=-25) and not crash() and checkWalls() != "left":
        # Move the tetromino to the left by decreasing its x coordinates
        for i in range(0, 4):
            for e in range(0, 4):
                blockCoords[-1][i][e][0] -= 25
        # Update its centre
        centres[-1][0] -= 25

    # If game is not paused, the right arrow key has been pressed, the
    # tetromino will not crash if it is moved right, the tetromino is not
    # about to crash and the tetromino is not hitting the right wall
    elif not paused and event.keysym == "Right" and not crash(coord=0, value=25) and not crash() and checkWalls() != "right":
        # Move the tetromino to the right by increasing its x coordinates
        for i in range(0, 4):
            for e in range(0, 4):
                blockCoords[-1][i][e][0] += 25
        # Update its centre
        centres[-1][0] += 25

    # If the game is not paused, the down arrow key has been pressed and the
    # tetromino will not crash if it is moved down
    elif not paused and event.keysym == "Down" and not crash():
        # Move tetromino down by increasing its y coordinates
        for i in range(0, 4):
            for e in range(0, 4):
                blockCoords[-1][i][e][1] += 25

        # Update its centre
        centres[-1][1] += 25

        # Delete previous tetromino
        for j in range(0, 4):
            screen.delete(blocks[-1][j])

        # Update the blocks array and create the new tetromino on the screen
        blocks[-1] = makePolygon(blockCoords[-1], colours[-1])

        # Increase the score by 1
        score += 1
    # If q was pressed
    elif event.keysym == "q" or event.keysym == "Q":
        # Make qPressed true
        qPressed = True
        endGame()  # Run the endGame procedure

    # If p was pressed
    elif event.keysym == "p" or event.keysym == "P":
        changePause()  # Change the state of the paused variable; also will resume the game if the game was alrady paused

    elif event.keysym == "r" or event.keysym == "R":
        restart()


def images():
    """Assigns images to many variables."""
    global tetros, background, left, right, tetrosSmall, up, down, xImage, zImage, pImage, qImage, rImage
    tetros = PhotoImage(file="Tetros.gif")
    background = PhotoImage(file="background.gif")
    left = PhotoImage(file="left.gif")
    right = PhotoImage(file="right.gif")
    tetrosSmall = PhotoImage(file="Tetros Small.gif")
    up = PhotoImage(file="Up.gif")
    down = PhotoImage(file="Down.gif")
    xImage = PhotoImage(file="X.gif")
    zImage = PhotoImage(file="Z.gif")
    pImage = PhotoImage(file="P.gif")
    qImage = PhotoImage(file="Q.gif")
    rImage = PhotoImage(file="R.gif")


def changePause():
    """Changes the state of the variable paused (switches it boolean value) and resumes the game if needed."""
    global paused
    if paused:
        paused = False
        coreGame()  # Call core game to resume the game
    else:
        paused = True


def callDifficulty(event):
    """Calls the getDifficulty function."""
    getDifficulty()


def initialScreen():
    images()  # Assign images to variables
    makeInstructions()  # Make the instructions screen
    instructions.pack()  # Pack the instructions screen
    # Put the text box in the instructions screen
    eText_window = instructions.create_window(400, 580, window=eText)
    eText.focus_set()  # Focus automatically to the text box
    okayB.config(bd=5)
    # Put the "Begin!" button on the instructions screen
    okayB_window = instructions.create_window(580, 580, window=okayB)


def interfaceButtons():
    """Creates the pause and quit buttons in the game interface."""
    # Create quit button and assign it to endGame function
    buttonQuit = Button(root, text="Quit Game", command=lambda: endGame())
    buttonQuit.config(bd=5)
    # Create the quit button on the screen
    buttonQuit_window = screen.create_window(335, 240, window=buttonQuit)

    # Create pause button and assign it to the changePause function
    buttonPause = Button(
        root,
        text="Pause Game",
        command=lambda: changePause())
    buttonPause.config(bd=5)
    # Create the pause button on the screen
    buttonPause_window = screen.create_window(435, 240, window=buttonPause)
    # Restart button
    buttonRestart =  Button(root, text="Restart Game", command=lambda: restart())
    buttonRestart.config(bd=5)
    buttonRestart = screen.create_window(535, 240, window=buttonRestart)

def runGame():
    """Runs initializing functions and then runs the core functions of the game."""
    global qPressed, s, paused
    setInitialValues()  # Set up initial values
    makeTetrisRectangle()  # Make Tetros box
    overlay()  # Make dot overlay
    getRandomShape()  # Get a random shape to appear at the top (in the top two hidden rows)
    sidebar()  # Create the sidebar
    winsound.PlaySound(tetrisSong, winsound.SND_FILENAME |
                       winsound.SND_ASYNC | winsound.SND_LOOP)  # Loop the background music
    while not qPressed and not paused:  # Run while not paused and not quitted
        animateShape()  # Animate shape falling down
        makeScore()  # Update score
        screen.update()  # Update screen
        time.sleep(s)  # Sleep for animation effect

initialScreen()  # Create the initial instructions screen (this will go on to call the main runGame procedure)

# Bind the return key press in the instructions screen to callDifficulty
# (allows user to enter input and press enter to progress to the game
# screen)
eText.bind("<Return>", callDifficulty)
# Bind any key pressed in the game screen to keyDownHandler which decides
# what action is to be taken, if any
screen.bind("<Key>", keyDownHandler)

# Start tkinter mainloop
root.mainloop()
