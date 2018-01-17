Augmented reality games

Requirments to use these codes:
  Take a full A4 size printouts of the images attached.
 Modules required :
  Pygame
  cv2
  numpy
  
The first image is used for calibration if the camera that we are using and the second image is used to interprit the 3d positions from a 2D image.

The 2 game in this folder are Snake & Pong

Snake is a one player game.
Pong is a two player game.

Follow this process to play the game:

Run python3 snake.py 
or
    python3 pong.py
    
place the checks sheet(from printouts)
![Checks board](checks.jpg?raw=true "Checks board")
in front of camera for calibration
once the calibration is over it'll show the second printout image (marker board). Take care that ur printout is alligned upside down to the shown image.
And the press Enter.
Once the game starts press on the Pygame window with your mouse so that the windows is selected and then the code can listen to the comands you
pass through key board.
Now you can play the game.

Controls : 
  Snake game:
    the 4 direction arrows on the key board have their own meaning the snake moves in the direction you press the arrow
  Pong :
    Use left and right arrows to movie the bottom plank
    Use A and D keys  to move top plank.
