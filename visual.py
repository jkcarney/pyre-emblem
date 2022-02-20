import tkinter as tk
import time
import gym
import numpy as np
from PIL import Image, ImageTk

from map_factory import OutdoorMapFactory
from unit import Unit
from game import FireEmblem
from agent import Agent, RandomAgent
import unit_populator


def action_in_valids(action, valid_actions):
    return np.any(np.all(action == valid_actions, axis=1))


class BoardVisualization(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.do_loop = tk.IntVar()
        self.delay_value = tk.StringVar()

        self.advance = tk.Button(self, text="Advance", command=self.advance_button_callback)
        self.advance.pack()
        self.loop_check = tk.Checkbutton(self, text='Loop', variable=self.do_loop)
        self.loop_check.pack()
        self.delay = tk.Spinbox(self, from_=0, to=5, increment=0.1, format='%.2f', textvariable=self.delay_value)
        self.delay.pack()

        self.env = gym.make('fe_env:fe-env-v0')
        self.env.reset()
        self.tile_map = self.env.unwrapped.number_map

        self.colors = ['green2', 'blue', 'forest green', 'sienna4']
        self.canvas = tk.Canvas(self, width=700, height=700, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.canvas.bind("<Configure>", self.redraw)
        self.rows = self.env.unwrapped.map.x
        self.columns = self.env.unwrapped.map.y
        self.tiles = {}
        self.ovals = {}

    def advance_button_callback(self):
        terminal = False
        if self.do_loop.get() == 1:
            while not terminal:
                valid = False
                random_action = self.env.action_space.sample()
                all_valid_actions = self.env.unwrapped.get_valid_actions_in_state()

                while not valid:
                    if action_in_valids(random_action, all_valid_actions):
                        valid = True
                    else:
                        random_action = self.env.action_space.sample()

                _, _, terminal, _ = self.env.step(random_action)

                self.redraw()
                self.update()
                time.sleep(float(self.delay_value.get()))
        else:
            valid = False
            random_action = self.env.action_space.sample()
            all_valid_actions = self.env.unwrapped.get_valid_actions_in_state()

            while not valid:
                if action_in_valids(random_action, all_valid_actions):
                    valid = True
                else:
                    random_action = self.env.action_space.sample()

            _, _, terminal, _ = self.env.step(random_action)
            self.redraw()

        if terminal:
            self.advance.configure(state=tk.DISABLED)

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

        for blue_unit in self.env.unwrapped.blue_team:
            x, y = blue_unit.x, blue_unit.y
            x1 = x * cellwidth
            x2 = x1 + cellwidth
            y1 = y * cellheight
            y2 = y1 + cellheight
            oval = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="navy", fill="cyan", tags="blueteam")
            self.ovals[x, y] = oval

        for red_unit in self.env.unwrapped.red_team:
            x, y = red_unit.x, red_unit.y
            x1 = x * cellwidth
            x2 = x1 + cellwidth
            y1 = y * cellheight
            y2 = y1 + cellheight
            oval = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="maroon", fill="red", tags="redteam")
            self.ovals[x, y] = oval


if __name__ == "__main__":
    board = BoardVisualization()
    board.mainloop()
