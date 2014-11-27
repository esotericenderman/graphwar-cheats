#!usr/bin/env python3

import sys, time
from tkinter import messagebox, Tk

game_w, game_h = 50, 30 # total width and height of the game board in game coordinates
formula_mode = "axis"

from pymouse import PyMouse, PyMouseEvent
from pykeyboard import PyKeyboard, PyKeyboardEvent
m = PyMouse()
k = PyKeyboard()
class PointMouseSelector(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)
        self.x, self.y = None, None

    def click(self, x, y, button, press):
        if press: return # only handle button up events
        if button == 1: # left click
            print("selecting", x, y)
            self.x, self.y = x, y
            self.stop()
        elif button == 2: # right click
            self.stop()
def select_point():
    S = PointMouseSelector()
    try: S.run()
    except: pass
    return (S.x, S.y)

def calculate_formula_axis(point_list):
    sorted_points = sorted(points, key=lambda x: x[0])
    start = point_list[0]
    x1, y1 = 0, 0
    result = ""
    normalize = lambda x: str(x) if "-" in str(x) else "+" + str(x)
    for point in points[1:]:
        x2, y2 = point[0] - start[0], point[1] - start[1]
        if x2 == x1: # jump discontinuity, skip to get a jump
            pass
        else:
            slope = (y2 - y1) / (x2 - x1)
            result += "+(sign(x{0})-sign(x{1}))*({2}*x{3})/2".format(normalize(-x1), normalize(-x2), str(round(-slope, 3)), normalize(round(-(y1 - slope * x1), 3))) # add a line segment with correct slope
        x1, y1 = x2, y2
    result = result[1:] + "+0.5*sin(800*x)" # remove the leading plus sign
    return result

def calculate_formula_graphwar(point_list):
    sorted_points = sorted(points, key=lambda x: x[0])
    start = point_list[0]
    x1, y1 = start[0], 0
    result = ""
    normalize = lambda x: str(x) if "-" in str(x) else "+" + str(x)
    for point in points[1:]:
        x2, y2 = point[0], point[1] - start[1]
        if x2 == x1: # jump discontinuity, skip to get a jump
            raise Exception("bad thing happen")
        else:
            slope = (y2 - y1) / (x2 - x1)
            result += "+(1/(1+exp(-1000*(x{0})))-1/(1+exp(-1000*(x{1}))))*({2}*x{3})".format(normalize(round(-x1)), normalize(round(-x2)), str(round(-slope, 3)), normalize(round(-(y1 - slope * x1), 3))) # add a line segment with correct slope
        x1, y1 = x2, y2
    result = result[1:] + "+0.1*sin(60*x)" # remove the leading plus sign
    return result

messagebox.showinfo("Select Point", "Press OK and left click on the top left corner and then the bottom right corner of the game axes. Right click to cancel.")
top_left = select_point()
if top_left[0] == None: sys.exit()
bottom_right = select_point()
if bottom_right[0] == None: sys.exit()
scale_w, scale_h = (bottom_right[0] - top_left[0]) / game_w, (bottom_right[1] - top_left[1]) / game_h
print("window size", bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])

while True:
    messagebox.showinfo("Game Start", "Press OK and left click path points when your turn starts, starting with the player. Right click to complete point entry and copy result to clipboard. If no points selected, program exits.")
    
    # get start point
    start = select_point()
    start = (start[0] - top_left[0], start[1] - top_left[1])
    if start[0] == None: sys.exit()
    
    # get path points
    points = [(start[0] / scale_w - game_w / 2, start[1] / scale_h - game_h / 2)]
    current_x = start[0]
    while True:
        point = select_point()
        if point[0] == None: break # completed
        point = (point[0] - top_left[0], point[1] - top_left[1])
        
        if point[0] <= current_x: # left or same as current one, which means jump down
            points.append((current_x / scale_w - game_w / 2, point[1] / scale_h - game_h / 2))
        else: # normal line segment
            points.append((point[0] / scale_w - game_w / 2, point[1] / scale_h - game_h / 2))
            current_x = point[0]
    print("selected points ", points)
    if formula_mode == "axis": # axisthgame style formulas
        formula = calculate_formula_axis(points)
    elif formula_mode == "graphwar": # graphwar style formulas
        formula = calculate_formula_graphwar(points)
    else: raise Exception("bad thing happen")
    
    print(formula)
    try:
        import win32clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(formula, win32clipboard.CF_TEXT)
        win32clipboard.CloseClipboard()
    except ImportError: pass
