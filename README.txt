Read me:

A naughts and crosses game, using pygame graphics, and a minimax algorithm for playing against the computer.

Prerequisites:

Pygame:
$ pip install pygame / $ py -m pip install pygame

To play, run the "naughts_and_crosses.py" in the scripts folder.


Read this if you are having trouble with running it:

You are getting the error because the interpreter is ignoring the "/local_lib" and "/image_folder" folders.
Go to the root folder ('/naughts and crosses'), and enter;
$ export PYTHONPATH=. 
into the console (if you're in an ide, you will have to do this in the cli, or built in console idk).
Yay, you fixed it.
