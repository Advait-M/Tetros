import cx_Freeze
import sys
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import random
import math
import time
import cmath
import copy
import winsound

os.environ['TCL_LIBRARY'] = "C:\\Users\\advai\\AppData\\Local\\Programs\\Python\\Python35\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\advai\\AppData\\Local\\Programs\\Python\\Python35\\tcl\\tk8.6"

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

execu = [cx_Freeze.Executable("Tetros.py", base=base)]
opt = {'build_exe': {"packages": ["tkinter", "random", "time", "math", "cmath", "copy", "sys", "winsound"], "include_files":["0%.wav", "50%.wav", "100%.wav", "150%.wav", "200%.wav", "background.gif", "Down.gif", "End.gif", "Left.gif", "LICENSE.md", "README.md", "P.gif", "Q.gif", "R.gif", "rewind.wav", "Right.gif", "Tetris theme song.wav", "Tetros Small.gif", "Tetros.gif", "Up.gif", "X.gif", "Z.gif", "C:\\Users\\advai\\AppData\\Local\\Programs\\Python\\Python35\\DLLs\\tcl86t.dll", "C:\\Users\\advai\\AppData\\Local\\Programs\\Python\\Python35\\DLLs\\tk86t.dll"]}}

cx_Freeze.setup(
    name="Tetros",
    options=opt,
    version="19.0",
    description="A game similar to Tetris.",
    executables=execu
)

