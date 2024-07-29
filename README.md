GraphingSolver
==============

Solver script for [GraphWar](https://www.graphwar.com/graphwar_1/index.html)!

GraphWar is a turn-based game where you fire artillery at other players using mathematical functions.

This is a script that generates functions that go through any points you choose. Simply select the points, and it will generate a function that appears as line segments connecting them.

Requirements
------------

This script requires `tkinter`, which is a library for creating and working with windows, as well as `mouse` & `win32clipboard`.

Automatic copying of the formula to the clipboard is only supported on Windows.

Usage
-----

Start the script. A prompt will show up with some instructions. Dismiss the prompt and left click on the top right corner of the graph axes, and then left click on the bottom left of the graph axes. The more precise this is, the better the resulting formulas will be.

Now a prompt will show up with further instructions. Dismiss the prompt and left click on the current player you want to make the function for. Now left click on the points you want the function to go through.

When done, left click outside of the graph. Doing so during player selection exits the script.

On Windows, the formula is now copied to the clipboard and can directly be inserted into the game. On other platforms, copy the function from the program's standard output.
