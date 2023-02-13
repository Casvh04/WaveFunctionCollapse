from tiles import Tile

class Cell:
    
    collapsed: bool
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.collapsed = False
        self.x = x
        self.y = y

    def Collapse(self, tile: Tile):
        self.collapsed = True
        self.tile = tile