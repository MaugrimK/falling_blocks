class Block:
    def __init__(self, position: tuple, colour: list):
        self.position = position
        self.colour = colour

    def move(self, dx: int = 0, dy: int = 0):
            self.position = self.position[0] + dx, self.position[1] + dy
