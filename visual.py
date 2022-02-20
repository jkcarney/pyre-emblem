import tkinter as tk
import time

from map_factory import OutdoorMapFactory
from unit import Unit
from game import FireEmblem
from agent import Agent, RandomAgent
import unit_populator


class BoardVisualization(tk.Tk):
    def __init__(self, x_tiles, y_tiles, tile_map, game):
        tk.Tk.__init__(self)

        self.do_loop = tk.IntVar()
        self.delay_value = tk.StringVar()

        self.advance = tk.Button(self, text="Advance", command=self.advance_button_callback)
        self.advance.pack()
        self.loop_check = tk.Checkbutton(self, text='Loop', variable=self.do_loop)
        self.loop_check.pack()
        self.delay = tk.Spinbox(self, from_=0, to=5, increment=0.1, format='%.2f', textvariable=self.delay_value)
        self.delay.pack()

        self.game = game
        self.tile_map = tile_map

        self.colors = ['green2', 'blue', 'forest green', 'sienna4']
        self.canvas = tk.Canvas(self, width=600, height=600, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.canvas.bind("<Configure>", self.redraw)
        self.rows = y_tiles
        self.columns = x_tiles
        self.tiles = {}
        self.ovals = {}

    def advance_button_callback(self):
        if self.do_loop.get() == 1:
            step_result = 0
            while step_result == 0:
                print(f'TURN {self.game.turn_count}')
                step_result = self.game.step()
                self.redraw()
                self.update()
                time.sleep(float(self.delay_value.get()))
        else:
            print(f'TURN {self.game.turn_count}')
            step_result = self.game.step()
            self.redraw()

        if step_result != 0:
            print(f'Game is over: {step_result}')
            self.advance.configure(state=tk.DISABLED)

    def redraw(self, event=None):
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
                tile = self.canvas.create_rectangle(x1,y1,x2,y2, fill=self.colors[int(self.tile_map[column][row])], tags="rect")
                self.tiles[row, column] = tile

        for blue_unit in self.game.blue_team:
            x, y = blue_unit.x, blue_unit.y
            x1 = x * cellwidth
            x2 = x1 + cellwidth
            y1 = y * cellheight
            y2 = y1 + cellheight
            oval = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="navy", fill="cyan", tags="blueteam")
            self.ovals[x, y] = oval

        for red_unit in self.game.red_team:
            x, y = red_unit.x, red_unit.y
            x1 = x * cellwidth
            x2 = x1 + cellwidth
            y1 = y * cellheight
            y2 = y1 + cellheight
            oval = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="maroon", fill="red", tags="redteam")
            self.ovals[x, y] = oval


if __name__ == "__main__":
    map_factory = OutdoorMapFactory(15, 15, 15, 15)
    tile_map,number_tile_map = map_factory.generate_map()

    #lyn = Unit(0xceb4, 0, 0, 2, 0x0204, 17, 6, 8, 10, 6, 2, 0, 0, True, [0x1, 0x6b], True)
    #bandit = Unit(0xe9b8, 0, 1, 2, 0x1410, 21, 4, 1, 4, 0, 3, 0, 0, False, [0x1f], False)

    allies = unit_populator.generate_blue_team(tile_map)
    enemies = unit_populator.generate_red_team(tile_map, allies)

    result = 0

    game = FireEmblem(tile_map, allies, enemies, RandomAgent(), RandomAgent())

    board = BoardVisualization(tile_map.x, tile_map.y, number_tile_map, game)
    board.mainloop()
