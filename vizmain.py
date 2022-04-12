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
        self.env = environment.Environment(15, 20, 15, 20)
        self.tile_map = self.env.number_map
        self.colors = ['green2', 'blue', 'forest green', 'sienna4']
        self.canvas = tk.Canvas(self, width=700, height=700, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.canvas.bind("<Configure>", self.redraw)
        self.rows = self.env.map.x
        self.columns = self.env.map.y
        self.tiles = {}
        self.ovals = {}
        self.run_name = ''
        self.reset()
        self.current_blue_unit = 0

    def reset(self):
        unit_factory = unit_populator.UnitFactory(5, 6, 15, 18, self.run_name)
        valid = False
        while not valid:
            try:
                self.env.reset()
                self.blue_team = unit_factory.generate_blue_team(self.env.map)
                self.red_team = unit_factory.generate_red_team(self.env.map, self.blue_team)
                valid = True
            except:
                pass

        self.current_blue_unit = 0

    def step(self):
        pass

    def redraw(self, event=None):
        self.canvas.delete("rect")
        self.canvas.delete("blueteam")
        self.canvas.delete("redteam")
        cellwidth = int(self.canvas.winfo_width()/self.columns/1.2)
        cellheight = int(self.canvas.winfo_height()/self.rows/1.2)
        for row in range(self.rows):
            for column in range(self.columns):
                x1 = row * cellwidth
                y1 = column * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                tile = self.canvas.create_rectangle(x1,y1,x2,y2, fill=self.colors[int(self.tile_map[row][column])], tags="rect")
                self.tiles[row, column] = tile

        for red_unit in self.red_team:
            x, y = red_unit.x, red_unit.y
            x1 = x * cellwidth
            x2 = x1 + cellwidth
            y1 = y * cellheight
            y2 = y1 + cellheight
            oval = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="maroon", fill="red", tags="redteam")
            self.ovals[x, y] = oval

        for blue_unit in self.blue_team:
            x, y = blue_unit.x, blue_unit.y
            x1 = x * cellwidth
            x2 = x1 + cellwidth
            y1 = y * cellheight
            y2 = y1 + cellheight
            oval = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="navy", fill="cyan", tags="blueteam")
            self.ovals[x, y] = oval


if __name__ == "__main__":
    board = BoardVisualization()
    board.mainloop()
