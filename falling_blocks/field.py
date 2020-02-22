import random

import pygame

from config import (BLOCK_SIDE_SIZE, FIELD_START_X, FIELD_START_Y, 
    FIELD_END_X, FIELD_END_Y, NUMBER_OF_COLS, NUMBER_OF_ROWS, BORDER_THICKNESS,
    FIGURE_POSITIONS)

class Field:
    def __init__(self):
        self.numberOfCols = NUMBER_OF_COLS
        self.numberOfRows = NUMBER_OF_ROWS

    def drawFigure(self, display, figureInfo):
        for blockPosition, colour in figureInfo:
            pixels = self.translatePositionToPixels(blockPosition)
            pygame.draw.rect(display, colour, pygame.Rect(pixels))

    def fillActiveField(self, display):
        display.fill((0, 0, 0), rect=pygame.Rect(FIELD_START_X, FIELD_START_Y,
                                                 FIELD_END_X-FIELD_START_X,
                                                 FIELD_END_Y-FIELD_START_Y))

    def translatePositionToPixels(self, position):
        xStart = FIELD_START_X + position[0] * BLOCK_SIDE_SIZE
        yStart = FIELD_START_Y + position[1] * BLOCK_SIDE_SIZE
        return xStart, yStart, BLOCK_SIDE_SIZE, BLOCK_SIDE_SIZE

    def drawFieldBorders(self, display):
        # x, y, x_thickness, y_thickness
        leftBorder = (FIELD_START_X-BORDER_THICKNESS, FIELD_START_Y, BORDER_THICKNESS,
                      FIELD_END_Y-FIELD_START_Y+BORDER_THICKNESS)
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(leftBorder))
        rightBorder = (FIELD_END_X, FIELD_START_Y, BORDER_THICKNESS,
                       FIELD_END_Y-FIELD_START_Y+BORDER_THICKNESS)
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(rightBorder))
        bottomBorder = (FIELD_START_X, FIELD_END_Y, FIELD_END_X-FIELD_START_X, BORDER_THICKNESS)
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(bottomBorder))

    def getRandomColour(self):
        return [random.randint(40, 250), random.randint(40, 250), random.randint(40, 250)]

    def getRandomFigurePositions(self):

        figureType = random.choice(list(FIGURE_POSITIONS.keys()))
        return (figureType, 1), FIGURE_POSITIONS.get(figureType).get(1)


