import tkinter as tk
import map_factory


class BoardVisualization(tk.Tk):
    def __init__(self, x_tiles, y_tiles, tile_map):
        tk.Tk.__init__(self)
        self.tile_map = tile_map
        self.colors = ['green2', 'blue', 'forest green', 'sienna4']


        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = x_tiles
        self.columns = y_tiles
        self.tiles = {}
        self.canvas.bind("<Configure>", self.redraw)
        self.status = tk.Label(self, anchor="w")
        self.status.pack(side="bottom", fill="x")

    def redraw(self, event=None):
        self.canvas.delete("rect")
        cellwidth = int(self.canvas.winfo_width()/self.columns)
        cellheight = int(self.canvas.winfo_height()/self.columns)
        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column*cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                tile = self.canvas.create_rectangle(x1,y1,x2,y2, fill=self.colors[int(self.tile_map[row][column])], tags="rect")
                self.tiles[row,column] = tile


if __name__ == "__main__":
    map_factory = map_factory.OutdoorMapFactory(10, 15, 10, 15)
    tile_map, number_tile_map = map_factory.generate_map()
    app = BoardVisualization(tile_map.x, tile_map.y, number_tile_map)
    app.mainloop()