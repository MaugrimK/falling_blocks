from falling_blocks.config import NUMBER_OF_COLS, FIGURE_POSITIONS
from falling_blocks.block import Block

class Figure:
    def __init__(self):
        self.blocks = []

    def addBlocks(self, blockObjects):
        self.blocks.extend(blockObjects)

    def getBlocks(self):
        return self.blocks

    def hasBlocks(self):
        return True if self.blocks else False

    def move(self, dx=0, dy=0):
        for block in self.blocks:
            block.move(dx, dy)

    def getAllBlocksPositions(self):
        return [block.position for block in self.blocks]

    def getAllBlocksInfo(self):
        return [(block.position, block.colour) for block in self.blocks]


class StaticFigure(Figure):
    def getFilledRows(self):
        """Find rows that are filled with blocks"""
        filledRows = []
        yPositions = set(y for x, y in self.getAllBlocksPositions())
        for yPos in yPositions:
            positions = [(x, y) for x, y in self.getAllBlocksPositions() if y == yPos]
            if len(positions) == NUMBER_OF_COLS:  # the whole row is filled
                filledRows.append(yPos)
        return filledRows

    def removeRows(self, filledRows):
        blocks = self.getBlocks()
        blocksToKeep = [block for block in blocks if block.position[1] not in filledRows]
        self.blocks = blocksToKeep

    def moveRows(self, filledRows):
        blocks = self.getBlocks()
        blocksToMove = []
        for yPos in sorted(filledRows):
            blocksToMove.extend([block for block in blocks if block.position[1] < yPos])

        for blockToMove in blocksToMove:
            blockToMove.move(dy=1)


class FallingFigure(Figure):
    def __init__(self):
        self.figureType = None
        self.colour = None
        super(FallingFigure, self).__init__()

    def addBlocksFromPositions(self, blockPositions, colour, figureType):
        self.figureType = figureType
        self.colour = colour
        for blockPosition in blockPositions:
            self.blocks.append(Block(position=blockPosition, colour=colour))

    def getNextPositions(self, dx=0, dy=0):
        return [(x + dx, y + dy) for x, y in self.getAllBlocksPositions()]

    def flip(self):
        figureName, newTypeNumber = self.getNextFigureTypeNumber()
        refPosition = self.getReferencePoint()
        newPositions = self.getFlippedFigurePositions(figureName, newTypeNumber, refPosition)
        self.destroyBlocks()
        self.addBlocksFromPositions(blockPositions=newPositions, colour=self.colour,
                                    figureType=(figureName, newTypeNumber))

    def getNextFigureTypeNumber(self):
        figureName, typeNumber = self.figureType[0], self.figureType[1]
        possibleTypes = len(FIGURE_POSITIONS.get(figureName).keys())
        if typeNumber + 1 > possibleTypes:
            newTypeNumber = 1
        else:
            newTypeNumber = typeNumber + 1

        return figureName, newTypeNumber

    def getReferencePoint(self):
        positions = self.getAllBlocksPositions()
        minXPosition = min([x for x, y in positions])
        minYPosition = min([y for x, y in positions])
        return minXPosition, minYPosition

    def getFlippedFigurePositions(self, figureName, newTypeNumber, refPosition):
        relativePositions = FIGURE_POSITIONS.get(figureName).get(newTypeNumber)
        truePositions = [(x + refPosition[0], y + refPosition[1]) for x, y in relativePositions]
        return truePositions

    def destroyBlocks(self):
        self.blocks = []
        self.figureType = None
