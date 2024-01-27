from PIL import Image

class Tile:
    def __init__(self, sprite: Image.Image, options: list[list[int]]):
        self.sprite = sprite
        self.options = options