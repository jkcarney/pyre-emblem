import tkinter as tk
import map_factory
import unit


class BoardVisualization(tk.Tk):
    def __init__(self, x_tiles, y_tiles, tile_map, fe_game):
        tk.Tk.__init__(self)
        self.tile_map = tile_map
        self.colors = ['green2', 'blue', 'forest green', 'sienna4']
        self.canvas = tk.Canvas(self, width=800, height=800, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = x_tiles
        self.columns = y_tiles
        self.tiles = {}
        self.ovals = {}
        self.status = tk.Label(self, anchor="w")
        self.status.pack(side="bottom", fill="x")

        self.game = fe_game

    def draw_units(self, event=None):
        self.canvas.delete("rect")
        self.canvas.delete("blueteam")
        self.canvas.delete("redteam")
        cellwidth = int(self.canvas.winfo_width()/self.columns/1.2)
        cellheight = int(self.canvas.winfo_height()/self.columns/1.2)
        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column * cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                tile = self.canvas.create_rectangle(x1,y1,x2,y2, fill=self.colors[int(self.tile_map[row][column])], tags="rect")
                self.tiles[row, column] = tile

        for blue_unit in self.game.allies:
            x, y = blue_unit.x, blue_unit.y
            x1 = x * cellwidth
            x2 = x1 + cellwidth
            y1 = y * cellheight
            y2 = y1 + cellheight
            oval = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="navy", fill="cyan", tags="blueteam")
            self.ovals[x, y] = oval

        for red_unit in self.game.enemies:
            x, y = red_unit.x, red_unit.y
            x1 = x * cellwidth
            x2 = x1 + cellwidth
            y1 = y * cellheight
            y2 = y1 + cellheight
            oval = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="maroon", fill="red", tags="redteam")
            self.ovals[x, y] = oval

        if self.game.loss_condition_encountered or self.game.win_condition_encountered:
            self.after(15, self.draw_units)

