from turtle import *
import tkinter as _
from PIL import ImageGrab, Image
import os


_.ROUND=_.BUTT

running = True
FRAMES_PER_SECOND = 10
image_list = []

def grab_canvas():
    "Returns an Image of the turtle screen, accounting for Mac Retina Pixel Doubling"
    canvas = getscreen().getcanvas()
    x0 = canvas.winfo_rootx() + canvas.winfo_x()
    y0 = canvas.winfo_rooty() + canvas.winfo_y()
    x1 = x0 + canvas.winfo_width()
    y1 = y0 + canvas.winfo_height()
    return ImageGrab.grab(bbox=(x0*2 + 15, y0*2 + 15, x1*2 - 15, y1*2 -15)) #due to pixel doubling on Mac Retina Screen

def draw(your_drawing_function):
    "Executes the selected animation"
    your_drawing_function()
    stop()

def stop():
    "Flags the running variable to stop"
    global running
    running = False

def record_screen():
    "while the drawing is running, PIL to take screenshots and append to list"
    curr_image = grab_canvas()
    image_list.append(curr_image)
    if running:
        ontimer(record_screen, int(1000 / FRAMES_PER_SECOND))

def makegif(your_drawing_function, gif_name=None, gif_path=None):
    """Takes the name of the animation function and a name for the gif file. 
    Returns a gif of the animation in current directory.
    If gif_path is given, saves the gif there instead"""
    speed(0)
    hideturtle()
    record_screen()  # start the recording
    draw(your_drawing_function) # start drawing
    path_name = gif_path or os.getcwd() + '/' + gif_name + '.gif'
    image_list[0].save(path_name, format='GIF', save_all=True, append_images=image_list[1:], optimize=False, duration=40, loop=0)

#
# For each student:
# Import their draw function from their module
# 


if __name__ == '__main__':
    from animation import main # to be changed to a dynamic import statement
    makegif(main, 'test')
