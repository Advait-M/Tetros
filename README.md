# Tetros
## Game description
Tetros is an entertaining arcade game in which the user tries to fit as many tetrominoes, shapes made of four blocks, as they can on the designated screen area. The game ends when the user cannot place a tetromino without overlapping any tetromino that has already been placed. The goal of the game is to get the highest score before the tetrominoes stack up to the top. The user can clear a row if it is entirely filled with blocks. If the user is certain in their tetromino placement they can accelerate its speed by pressing the down key.  

To begin, the user must read the instructions screen that pops up. At the bottom of this screen the user can customize the speed at which tetrominoes should fall (a lower number means tetrominoes fall faster). Next, the user must click the “Begin!” button or press the enter key. This will lead them to the game screen. This screen contains the box in which tetrominoes will be placed, a sidebar to the right that contains buttons and shows the controls of the game, and an indicator that shows what the next tetromino is. The user may accelerate, move or rotate the tetromino as they wish as long as it stays within the box and it does not overlap any tetrominoes already placed. 

## Scoring
The scoring is as follows:
New tetromino = 8 points
Cleared row = 20 points  
Accelerating the tetromino = 1 point (each time)

## Instructions for play
Open the game file by opening the Python file “Tetros.py” (this file is located inside the “Tetros” folder). Next, to launch the game, push F5 or press “Run module” under the “Run” menu located at the top left of the window.

After a short delay, the initial instructions screen will appear. Read over the instructions and decide on the speed at which tetrominoes should fall (a smaller number means the tetrominoes fall faster). Approximate difficulties for different speeds our given above the text box, namely easy = 0.5, medium = 0.3, and hard = 0.1 (all numbers in seconds). The tempo of the background music is also dependent on this speed. Type in the desired time interval between tetrominoes and hit the enter key or the “Begin!” button beside the text box. If the given number is non-negative, then the user will be led to the main game screen. Otherwise, the user will have to enter a non-negative number. 

Once the user has proceeded onto the next screen, they will see the controls on the bottom right which are:
LEFT arrow key to move tetromino to the left
RIGHT arrow key to move tetromino to the right 
DOWN arrow key to accelerate tetromino 
UP arrow key or X key to rotate tetromino clockwise
Z key to rotate tetromino anti-clockwise 
P key to pause/unpause the game
Q key to quit the game 
There are also two buttons located above the controls which the user can use to pause/unpause or quit the game (these buttons are labeled according to the action they perform). Try to clear rows and not stack the tetrominoes to the top of the screen! 

Once the user has quit the game or cannot place any more tetrominoes a new screen will appear. This screen will contain the logo of the game and the user’s final statistics which include the score and the amount of rows cleared, if more than one row has been cleared then the user will receive a “Nice job!” comment. Next, the user may click the “Quit Tetros” button which will exit the game.


# Screenshots
![Tetros Entry Screen](/Screenshots/entry.PNG?raw=true "Tetros Entry Screen")
![Tetros Main Interface](/Screenshots/main_interface.PNG?raw=true "Tetros Main Interface")
![Tetros End screen](/Screenshots/end_screen.PNG?raw=true "Tetros End screen")

# Running the Game
The easiest way to run the game is to download the "Tetros-19.0-amd64.msi" file and run the installer. Install the game into the desired location, then locate the Tetros.exe file to run the game.

It is also possible to download the build.zip, then unzip the file and navigate to build\exe.win-amd64-3.5\Tetros.exe. From there, just run the Tetros.exe.

In order to run the game from source code, download all files into a directory and then run Tetros.py (includes new features such saving/loading game functionality) or Tetros Original.py (the original version).
