from tkinter import messagebox
import mouse
import win32clipboard
import sympy as sp

# Define plane dimensions
plane_width = 50
plane_height = 30

half_plane_width = plane_width / 2
half_plane_height = plane_height / 2

minimum_plane_x = -half_plane_width
maximum_plane_x = half_plane_width

minimum_plane_y = -half_plane_height
maximum_plane_y = half_plane_height

# Get the derivative level input
derivative_level_string = input("Enter the derivative level: ")
derivative_level = int(derivative_level_string) if derivative_level_string.isnumeric() else 0

messagebox.showinfo("Specify Window Dimensions", "Press 'OK' and left-click on the top-right corner, and then the bottom-left corner of the plane. Right-click to cancel.")

# Function to select pixel positions using mouse
def select_pixel():
    mouse.wait(mouse.LEFT, (mouse.UP))
    return mouse.get_position()

# Get the points for the plane
top_right_point = select_pixel()
bottom_left_point = select_pixel()

minimum_pixel_x = bottom_left_point[0]
maximum_pixel_x = top_right_point[0]

minimum_pixel_y = top_right_point[1]
maximum_pixel_y = bottom_left_point[1]

# Calculate window dimensions
window_width = maximum_pixel_x - minimum_pixel_x
window_height = maximum_pixel_y - minimum_pixel_y

# Function to select points and scale them to plane coordinates
def select_point():
    pixel = select_pixel()

    x_difference = pixel[0] - minimum_pixel_x
    x_scale = x_difference / window_width

    y_difference = maximum_pixel_y - pixel[1]
    y_scale = y_difference / window_height

    return (minimum_plane_x + (plane_width  * x_scale), minimum_plane_y + (plane_height * y_scale))

# Function to calculate symbolic function for the points using sympy
def calculate_function(points):
    x = sp.symbols('x')  # Define x symbol for sympy
    function = 0  # Initialize the function

    point_count = len(points)
    is_line = point_count == 2

    for point_index in range(1, point_count):
        current_point = points[point_index]
        previous_point = points[point_index - 1]

        current_x = current_point[0]
        previous_x = previous_point[0]

        current_y = current_point[1]
        previous_y = previous_point[1]

        x_difference = current_x - previous_x
        y_difference = current_y - previous_y

        slope = y_difference / x_difference
        constant = previous_y - slope * previous_x

        if is_line:
            function = slope * x + constant  # Equation of the line
            return function

        # For multi-point, add absolute value term (this is an approximation)
        function += (slope * x + constant)

    return function if function != 0 else 0

# Main loop to select points and calculate function
while True:
    messagebox.showinfo("Game Start", "Press 'OK' and left-click points that the function should follow, starting with the player position. Left-click outside the plane to complete point entry and copy the result to your clipboard. If no points were selected, the program will exit.")

    start = select_point()
    points = [start]

    while True:
        next_point = select_point()

        next_point_x = next_point[0]
        next_point_y = next_point[1]

        if next_point_x >= maximum_plane_x or next_point_x <= minimum_plane_x or next_point_y >= maximum_plane_y or next_point_y <= minimum_plane_y:
            break

        points.append(next_point)

    if len(points) == 1:
        exit()

    function = calculate_function(points)  # Generate the symbolic function

    # Differentiate the function if needed
    if derivative_level > 0:
        derivative = sp.diff(function, sp.symbols('x'), derivative_level)
    else:
        derivative = function

    # Convert the result to a string
    derivative_str = str(derivative)

    # Copy the result to the clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(derivative_str, win32clipboard.CF_TEXT)
    win32clipboard.CloseClipboard()

    print(derivative_str)  # Print the derivative to the console
