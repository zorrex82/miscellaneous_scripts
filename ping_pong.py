# Game Ping-Pong
# Author: Edinor Junior

# Imports
from tkinter import *
import random
import time

# Variable to receive value for game level
level = int(input("Choose a game level? 1/2/3/4/5 \n"))

# Variabel to determine the size according game level
length = 500 / level

# Object instance Tk
root = Tk()
root.title("Ping Pong")
root.resizable(0, 0)
root.wm_attributes("-topmost", -1)

# Variable to receive Canvas function
canvas = Canvas(root, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
root.update()

# variable to count score
count = 0

# Variable to determine the game over
lost = False


# Definition of class ball
class Ball:
    def __init__(self, canvas, Bar, color):

        # Variables to build a ball
        self.canvas = canvas
        self.Bar = Bar
        self.id = canvas.create_oval(0, 0, 15, 15, fill=color)
        self.canvas.move(self.id, 245, 200)

        # Lists to determine positions
        starts_x = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts_x)

        # Variables to determine size of ball
        self.x = starts_x[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    # Function to draw the sphere
    def draw(self):

        # Variables to move a ball
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = 3

        if pos[3] >= self.canvas_height:
            self.y = -3

        if pos[0] <= 0:
            self.x = 3

        if pos[2] >= self.canvas_width:
            self.x = -3

        self.Bar_pos = self.canvas.coords(self.Bar.id)

        if pos[2] >= self.Bar_pos[0] and pos[0] <= self.Bar_pos[2]:
            if pos[3] >= self.Bar_pos[1] and pos[3] <= self.Bar_pos[3]:
                self.y = -3
                global count
                count += 1

                score()

        if pos[3] <= self.canvas_height:

            self.canvas.after(10, self.draw)
        else:

            game_over()

            global lost
            lost = True


# Class to determine bar
class Bar:
    def __init__(self, canvas, color):

        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, length, 10, fill=color)
        self.canvas.move(self.id, 200, 400)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)

    def draw(self):

        self.canvas.move(self.id, self.x, 0)

        self.pos = self.canvas.coords(self.id)

        if self.pos[0] <= 0:
            self.x = 0

        if self.pos[2] >= self.canvas_width:
            self.x = 0

        global lost

        if lost == False:
            self.canvas.after(10, self.draw)

    def move_left(self, event):

        if self.pos[0] >= 0:
            self.x = -3

    def move_right(self, event):

        if self.pos[2] <= self.canvas_width:
            self.x = 3


# Function to initialize the game
def start_game(event):
    global lost, count
    lost = False
    count = 0

    score()

    canvas.itemconfig(game, text=" ")

    time.sleep(1)
    Bar.draw()
    Ball.draw()

# function to determine the score
def score():
    canvas.itemconfig(score_now, text="Score: " + str(count))


# function to determine the end game
def game_over():
    canvas.itemconfig(game, text="Game over!")


Bar = Bar(canvas, "orange")
Ball = Ball(canvas, Bar, "purple")

score_now = canvas.create_text(430, 20, text="Pontos: " + str(count), fill="green", font=("Arial", 16))
game = canvas.create_text(400, 300, text=" ", fill="red", font=("Arial", 40))
canvas.bind_all("<Button-1>", start_game)

root.mainloop()

