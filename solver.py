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

    return (minimum_plane_x + (plane_width  * x_scale), minimum_plane_y + (plane_height * y_scale))

def calculate_function(points):
    function = ""

    correct_sign = lambda x : f" {"-" if x < 0 else "+"} {abs(x)}" if x != 0 else ""
    opposite_sign = lambda x : correct_sign(-x)

    point_count = len(points)
    is_line = point_count == 2
    sum = 0

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

        zero_slope = slope == 0
        zero_constant = constant == 0

        if zero_slope and zero_constant:
            pass

        if is_line:
            slope_term = "" if zero_slope else f"{slope}x"
            constant_term = constant if zero_slope else correct_sign(constant)

            return f"{slope_term}{constant_term}"

        shifted_absolute_value_term = lambda x : f"abs(x{opposite_sign(x)})"

        first_shifted_absolute_value_term = None
        is_first_pair = point_index == 1

        if is_first_pair:
            first_shifted_absolute_value_term = "x"
            previous_y = constant
        else:
            first_shifted_absolute_value_term = shifted_absolute_value_term(previous_x)

        second_shifted_absolute_value_term = None
        is_last_pair = point_index == point_count - 1

        if is_last_pair:
            second_shifted_absolute_value_term = " + x"
            current_y = constant
        else:
            second_shifted_absolute_value_term = f" - {shifted_absolute_value_term(current_x)}"

        sum += (previous_y + current_y) / 2

        half_slope = slope / 2
        half_slope_term = half_slope if is_first_pair else correct_sign(half_slope)

        function += f"{half_slope_term}({first_shifted_absolute_value_term}{second_shifted_absolute_value_term})"

    return "0" if function == "" else f"{function}{correct_sign(sum)}"

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

    function = calculate_function(points)

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(function, win32clipboard.CF_TEXT)
    win32clipboard.CloseClipboard()