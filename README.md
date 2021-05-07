# Curses_Hangman
Hangman game in Terminal made with Python/curses module

Made by Daan van Berkel.

To run the script python 3.8 or later is needed for use of the 'walrus' operator in the script.
Latest version of python can be found here: https://www.python.org/downloads/

The curses module is part of the standard library with python, as are all other imported modules.
Threfore no extra installations are required.

the script creates two small text (json) files in the same directory as the script itself,
they are for saving the users settings and highscores. These can be safely deleted at any time.

To run the script, open your terminal of choice (for example cmd.exe on windows)
navigate to the folder where you have saved the script using the 'cd' command

for example: type 'cd C:\Users\d.vanberkel\Documents\Hangman' and hit [ENTER]
then run the script typing: 'python hangman.py' and hitting [ENTER]

You should see the main menu and be able to navigate now.

![](https://github.com/PancakeFear/Curses_Hangman/blob/main/Hangman.jpg)

the how to play is included in the game, but I will include it here as well:

in menu's:
Use the [ARROW] keys to navigate.
Pressing [ENTER] will advance to the underlaying menu or function.
Pressing [ESCAPE] will allow you to move back to a previous menu, or quit the current process.

On screen might be more instructions on keys that can be used.

in game:
Pressing any alphabetical key wil instantly interpret this as your next guess.
Points will be giving for every right letter.

Pressing the [ENTER] key will bring up a popup window, where you can type out the complete word.
Guessing this way can give a huge bonus in points, but also deducts points for being wrong.
Pressing [ESCAPE] allows you to cancel this proces. Pressing [ENTER] again wil commit your input as a guess.

