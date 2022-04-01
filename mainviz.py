import environment
import unit_populator
from termcolor import colored
import fedata
import sys
from datetime import datetime
import tkinter as tk


class BoardVisualization(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.env = environment.Environment(10, 10, 15, 15)
        self.env.reset()
        self.tile_map = self.env.number_map
        self.colors = ['green2', 'blue', 'forest green', 'sienna4']
        self.canvas = tk.Canvas(self, width=700, height=700, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.canvas.bind("<Configure>", self.redraw)
        self.rows = self.env.map.x
        self.columns = self.env.map.y
        self.tiles = {}
        self.ovals = {}

    def redraw(self, event=None):
        self.canvas.delete("rect")
        self.canvas.delete("blueteam")
        self.canvas.delete("redteam")
        cellwidth = int(self.canvas.winfo_width()/self.columns/1.2)
        cellheight = int(self.canvas.winfo_height()/self.columns/1.2)
        for row in range(self.rows):
            for column in range(self.columns):
                x1 = row * cellwidth
                y1 = column * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                tile = self.canvas.create_rectangle(x1,y1,x2,y2, fill=self.colors[int(self.tile_map[row][column])], tags="rect")
                self.tiles[row, column] = tile


if __name__ == "__main__":
    board = BoardVisualization()
    board.mainloop()
