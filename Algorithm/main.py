import glob
import random    
from PIL import Image
from Classes.tiles import Tile
from Classes.cell import Cell

tiles: list[Tile] = []
tileImages: list[Image.Image] = []
options: list[list[list[int]]] = [
[[2,4],[0,2,3],[1,2,3],[0,2,3]], #tile1
[[0,1,3],[1,4],[1,2,3],[1,4]], #tile2
[[0,1,3],[0,2,3],[0,4],[0,2,3]], #tile3
[[0,1,3],[0,2,3],[1,2,3],[0,2,3]], #tile4
[[2,4],[1,4],[0,4],[1,4]] #tile5
]
Size = 4

def LoadImages():
    for path in glob.glob('../SpriteAssets/Sprites/*.png'):
        tileImages.append(Image.open(path))

def Create2DList(Size):
    list2d: list[list[Cell]] = []
    for _ in range(Size):
        list2d.append([])
    for i in range(len(list2d)):
        for j in range(Size):
            list2d[i].append(Cell(i,j))
    return list2d  

def GetCell(x: int, y: int, Grid: list[list[Cell]]) -> Cell | None:
    if x >= Size or x < 0:
        return None
    elif y >= Size or y < 0:
        return None
    else:
        return Grid[x][y]

def FindOptions(cell: Cell, Grid: list[list[Cell]]):
    OptionsList: list[int] = []
    top_cell = GetCell(cell.x, cell.y - 1, Grid)
    if top_cell != None and top_cell.collapsed:
        if len(OptionsList) == 0:
            OptionsList = top_cell.tile.options[2]
        else:
            OptionsList = [tile for tile in OptionsList if tile in top_cell.tile.options[2]]
    right_cell = GetCell(cell.x+1, cell.y, Grid)
    if right_cell != None and right_cell.collapsed:
        if len(OptionsList) == 0:
            OptionsList = right_cell.tile.options[3]
        else:
            OptionsList = [tile for tile in OptionsList if tile in right_cell.tile.options[3]]
    bottom_cell = GetCell(cell.x, cell.y+1, Grid)
    if bottom_cell != None and bottom_cell.collapsed:
        if len(OptionsList) == 0:
            OptionsList = bottom_cell.tile.options[0]
        else:
            OptionsList = [tile for tile in OptionsList if tile in bottom_cell.tile.options[0]]
    left_cell = GetCell(cell.x-1, cell.y, Grid)
    if left_cell != None and left_cell.collapsed:
        if len(OptionsList) == 0:
            OptionsList = left_cell.tile.options[1]
        else:
            OptionsList = [tile for tile in OptionsList if tile in left_cell.tile.options[1]]
    
    return OptionsList

def SolveGrid(Grid, canvas):
    for x in range(Size):
        for y in range(Size):
            cell = Grid[x][y]
            if cell.collapsed:
                continue
            top_cell = GetCell(x,y-1,Grid)
            Direction = random.randint(0,3)
            if top_cell != None and not top_cell.collapsed and Direction == 0:
                AvailableOptions = FindOptions(top_cell,Grid)
                if len(AvailableOptions) != 0:
                    tile = tiles[random.choice(AvailableOptions)]
                    top_cell.Collapse(tile)
                    canvas.paste(tile.sprite,(top_cell.x*40,top_cell.y*40))
                    return
            right_cell = GetCell(x+1,y,Grid)
            if right_cell != None and not right_cell.collapsed and Direction == 1:
                AvailableOptions = FindOptions(right_cell,Grid)
                if len(AvailableOptions) != 0:
                    tile = tiles[random.choice(AvailableOptions)]
                    right_cell.Collapse(tile)
                    canvas.paste(tile.sprite,(right_cell.x*40,right_cell.y*40))
                    return
            bottom_cell = GetCell(x,y+1,Grid)
            if bottom_cell != None and not bottom_cell.collapsed and Direction == 2:
                AvailableOptions = FindOptions(bottom_cell,Grid)
                if len(AvailableOptions) != 0:
                    tile = tiles[random.choice(AvailableOptions)]
                    bottom_cell.Collapse(tile)
                    canvas.paste(tile.sprite,(bottom_cell.x*40,bottom_cell.y*40))
                    return
            left_cell = GetCell(x-1,y,Grid)
            if left_cell != None and not left_cell.collapsed and Direction == 3:
                AvailableOptions = FindOptions(left_cell,Grid)
                if len(AvailableOptions) != 0:
                    tile = tiles[random.choice(AvailableOptions)]
                    left_cell.Collapse(tile)
                    canvas.paste(tile.sprite,(left_cell.x*40,left_cell.y*40))
                    return

def Setup():
    canvas: Image.Image = Image.new('RGB', (40 * Size, 40 * Size))
    LoadImages()
    for i, image in enumerate(tileImages):
        tiles.append(Tile(image, options[i]))
    Grid: list[list[Cell]] = Create2DList(Size)

    #First choice
    x = random.randint(0,Size-1)
    y = random.randint(0,Size-1)
    if len(tiles) > 0:
        tile = random.choice(tiles)
    else:
        print("Error: No available sprites found.")
        return
    canvas.paste(tile.sprite,(x*40,y*40))
    Grid[x][y].Collapse(tile)
    
    solved: bool = False
    i = 0
    
    while not solved:
        SolveGrid(Grid,canvas)
        solved = True
        for x in range(Size):
            for y in range(Size):
                if not Grid[x][y].collapsed:
                    solved = False
                    break
        i += 1
        if i >= (Size*Size):
            solved = True
    canvas.show()
Setup()

#Rework tile options
#instead of check which tiles are possible
#check if a side is a blank or has a connection