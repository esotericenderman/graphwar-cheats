import sys
import tkMessageBox # type: ignore

from pymouse import PyMouse, PyMouseEvent
from pykeyboard import PyKeyboard

game_width, game_height = 50, 30 # Width and height of the game board in game coordinates.

mouse = PyMouse()
keyboard = PyKeyboard()

formula_modes = {
    "graphwar": "graphwar",
    "axis": "axis"
}

formula_mode = formula_modes["graphwar"]

mouse = {
    "left_click": 1,
    "right_click": 2
}

class PointMouseSelector(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)
        self.x, self.y = None, None

    def click(self, x, y, button, press):
        if press: return # Handle only button-up events.

        if button == mouse["left_click"]:
            self.x, self.y = x, y
            self.stop()
        elif button == mouse["right_click"]:
            self.stop()

def select_point():
    S = PointMouseSelector()
    S.run()

    return (S.x, S.y)

def calculate_formula_axis(point_list):
    start = point_list[0]
    x1, y1 = 0, 0
    result = ""

    normalize = lambda x: str(x) if "-" in str(x) else "+" + str(x)

    for point in points[1:]:
        x2, y2 = point[0] - start[0], point[1] - start[1]
        if x2 == x1: # Jump discontinuity.
            pass
        else:
            slope = (y2 - y1) / (x2 - x1)
            result += "+(sign(x{0})-sign(x{1}))*({2}*x{3})/2".format(normalize(-x1), normalize(-x2), str(-slope), normalize(-(y1 - slope * x1))) # Add a line segment.
        x1, y1 = x2, y2

    result = result[1:] + "+0.5*sin(800*x)" # Remove the leading +.
    return result

def calculate_formula_graphwar(point_list):
    start = point_list[0]
    x1, y1 = start[0], 0
    result = ""
    
    normalize = lambda x: str(x) if "-" in str(x) else "+" + str(x)

    for point in points[1:]:
        x2, y2 = point[0], point[1] - start[1]

        if x2 == x1: # Jump discontinuity.
            raise Exception("Can't divide by 0.")
        else:
            slope = (y2 - y1) / (x2 - x1)
            result += "+(1/(1+exp(-1000*(x{0})))-1/(1+exp(-1000*(x{1}))))*({2}*x{3})".format(normalize(-x1), normalize(-x2), str(-slope), normalize(-(y1 - slope * x1))) # Add a line segment.

        x1, y1 = x2, y2

    result = result[1:] + "+0.1*sin(60*x)" # Remove the leading +.
    return result

tkMessageBox.showinfo("Specify Window Dimensions", "Press 'OK' and left-click on the top-left corner, and then the bottom-right corner of the plane. Right-click to cancel.")

top_left = select_point()
if top_left[0] == None: sys.exit()

bottom_right = select_point()
if bottom_right[0] == None: sys.exit()

scale_width, scale_height = (bottom_right[0] - top_left[0]) / game_width, (bottom_right[1] - top_left[1]) / game_height

while True:
    tkMessageBox.showinfo("Game Start", "Press 'OK' and left-click points that the function should follow, starting with the player position. Right-click to complete point entry and copy the result to your clipboard. If no points were selected, the program will exits.")

    # Get start point.
    start = select_point()
    start = (start[0] - top_left[0], start[1] - top_left[1])
    if start[0] == None: sys.exit()
    
    # Get path points.
    points = [(start[0] / scale_width - game_width / 2, start[1] / scale_height - game_height / 2)]
    current_x = start[0]

    while True:
        point = select_point()

        if point[0] == None: break # Completed selecting points.

        point = (point[0] - top_left[0], point[1] - top_left[1])

        if point[0] <= current_x: # The point is to the left of the current one, which means jump down.
            points.append((current_x / scale_width - game_width / 2, point[1] / scale_height - game_height / 2))
        else: # Normal line segment.
            points.append((point[0] / scale_width - game_width / 2, point[1] / scale_height - game_height / 2))
            current_x = point[0]
    
    if formula_mode == formula_modes["axis"]:
        formula = calculate_formula_axis(points)
    elif formula_mode == formula_modes["graphwar"]:
        formula = calculate_formula_graphwar(points)

    try:
        import win32clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(formula, win32clipboard.CF_TEXT)
        win32clipboard.CloseClipboard()
    except ImportError: pass
