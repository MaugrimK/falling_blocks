import time

import pygame

from config import DISPLAY_SIZE, FALLING_SPEED, NUMBER_OF_COLS
from field import Field
from figure import FallingFigure, StaticFigure


class GameController:
    def __init__(self):
        self.field = Field()
        self.fallingFigure = FallingFigure()
        self.staticFigure = StaticFigure()
        self.fallingSpeedCounter = 0

    def startGame(self):
        self.display = pygame.display.set_mode(DISPLAY_SIZE)
        self.field.drawFieldBorders(self.display)
        self.spawnFallingFigure()

    def doNextStep(self, movement=None, flip=False):
        """ Perform next steps """
        if self.fallingFigureReachedBottom() or self.fallingFigureReachedStaticFigure():
            self.addFallingFigureToStaticFigure()
            self.reDrawAllFigures()

        if movement and self.fallingFigure.hasBlocks():
            if self.isMovementPossible(movement):
                self.fallingFigure.move(dx=movement)
                self.reDrawAllFigures()

        if flip and self.fallingFigure.hasBlocks():
            self.fallingFigure.flip()
            self.reDrawAllFigures()

        if self.fallingSpeedCounter > FALLING_SPEED:
            self.fallingSpeedCounter = 0
            self.fallingFigure.move(dy=1)
            self.reDrawAllFigures()

        self.fallingSpeedCounter += 1

    def isGameOver(self):
        """ Check if game is over """
        if self.staticFigureReachedTop():
            return True
        return False

    def reDrawAllFigures(self):
        self.field.fillActiveField(self.display)
        self.field.drawFigure(self.display, self.staticFigure.getAllBlocksInfo())
        if self.fallingFigure.hasBlocks():
            self.field.drawFigure(self.display, self.fallingFigure.getAllBlocksInfo())

    def spawnFallingFigure(self):
        figureType, blockPositions = self.field.getRandomFigurePositions()
        colour = self.field.getRandomColour()
        self.fallingFigure.addBlocksFromPositions(blockPositions=blockPositions, colour=colour, figureType=figureType)

    def destroyFigure(self):
        self.fallingFigure.destroyBlocks()

    def addFallingFigureToStaticFigure(self):
        self.staticFigure.addBlocks(self.fallingFigure.getBlocks())
        self.fallingFigure.destroyBlocks()
        # check if a row needs to be destroyed
        filledRows = self.staticFigure.getFilledRows()
        if filledRows:
            print('filledRows', filledRows)
            self.staticFigure.removeRows(filledRows)
            self.staticFigure.moveRows(filledRows)

        self.spawnFallingFigure()
        self.reDrawAllFigures()

    def fallingFigureReachedBottom(self):
        if any([y == self.field.numberOfRows-1 for x, y in self.fallingFigure.getAllBlocksPositions()]):
            return True
        return False

    def fallingFigureReachedStaticFigure(self):
        if set(self.staticFigure.getAllBlocksPositions()).intersection(set(self.fallingFigure.getNextPositions(dy=1))):
            return True
        return False

    def staticFigureReachedTop(self):
        yPositions = [y for x, y in self.staticFigure.getAllBlocksPositions()]
        if yPositions and min(yPositions) <= 2: # bug but this works
            return True
        return False


    def isMovementPossible(self, movement):
        if self.isMovementClippingBorders(movement) or \
           self.isMovementClippingStaticFigure(movement):
            return False
        return True

    def isMovementClippingBorders(self, movement):
        newPositions = self.fallingFigure.getNextPositions(dx=movement)
        if any([x < 0 or x > NUMBER_OF_COLS-1 for x, y in newPositions]):
            return True
        return False

    def isMovementClippingStaticFigure(self, movement):
        staticPositions = self.staticFigure.getAllBlocksPositions()
        fallingPositions = self.fallingFigure.getNextPositions(dx=movement)
        if set(staticPositions).intersection(fallingPositions):
            return True
        return False

    def endGame(self):
        self.message_display('Game Over')

    def message_display(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = self._text_objects(text, largeText)
        TextRect.center = ((DISPLAY_SIZE[0]/2), (DISPLAY_SIZE[1]/2))
        self.display.blit(TextSurf, TextRect)
        pygame.display.update()
        time.sleep(5)

    def _text_objects(self, text, font):
        textSurface = font.render(text, True, (255, 10, 255))
        return textSurface, textSurface.get_rect()
