from tkinter import messagebox
import mouse
import win32clipboard

plane_width = 50
plane_height = 30

half_plane_width = plane_width / 2
half_plane_height = plane_height / 2

minimum_plane_x = -half_plane_width
maximum_plane_x = half_plane_width

minimum_plane_y = -half_plane_height
maximum_plane_y = half_plane_height

messagebox.showinfo("Specify Window Dimensions", "Press 'OK' and left-click on the top-right corner, and then the bottom-left corner of the plane. Right-click to cancel.")

def select_pixel():
    mouse.wait(mouse.LEFT, (mouse.UP))
    return mouse.get_position()

top_right_point = select_pixel()
bottom_left_point = select_pixel()

minimum_pixel_x = bottom_left_point[0]
maximum_pixel_x = top_right_point[0]

minimum_pixel_y = top_right_point[1]
maximum_pixel_y = bottom_left_point[1]

window_width = maximum_pixel_x - minimum_pixel_x
window_height = maximum_pixel_y - minimum_pixel_y

def select_point():
    pixel = select_pixel()

    x_difference = pixel[0] - minimum_pixel_x
    x_scale = x_difference / window_width

    y_difference = maximum_pixel_y - pixel[1]
    y_scale = y_difference / window_height

    result = (minimum_plane_x + (plane_width  * x_scale), minimum_plane_y + (plane_height * y_scale))

    print(result)

    return result

def calculate_function(points):
    function = ""

    print(points)

    for point_index in range(1, len(points)):
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

        function += f'+ ({slope}x + {constant}) / (1 + e^(-10(x - ({previous_x})))) - ({slope}x + {constant}) / (1 + e^(-10(x - ({current_x}))))'

    return function

while True:
    messagebox.showinfo("Game Start", "Press 'OK' and left-click points that the function should follow, starting with the player position. Right-click to complete point entry and copy the result to your clipboard. If no points were selected, the program will exit.")

    start = select_point()

    points = [start]

    while True:
        next_point = select_point()

        if next_point[0] >= maximum_plane_x:
            break

        points.append(next_point)

    function = calculate_function(points)

    print(function)

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(function, win32clipboard.CF_TEXT)
    win32clipboard.CloseClipboard()