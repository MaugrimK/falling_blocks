import random
import time

import pygame

from field import Field
from figure import FallingFigure, StaticFigure


class GameController:
    def __init__(self, config):
        self.config = config
        self.field = Field(config)
        self.fallingFigure = FallingFigure(config)
        self.staticFigure = StaticFigure(config)
        self.fallingSpeedCounter = 0

    def startGame(self):
        self.display = pygame.display.set_mode(self.config.display_size)
        self.field.drawFieldBorders(self.display)
        self.spawnFallingFigure()

    def doNextStep(self, movement=None, flip=False):
        """ Perform next steps """
        if self.fallingFigureReachedBottom() or self.fallingFigureReachedStaticFigure():
            self.addFallingFigureToStaticFigure()
            self.reDrawAllFigures()

        if movement and self.fallingFigure.blocks:
            if self.isMovementPossible(movement):
                self.fallingFigure.move(dx=movement)
                self.reDrawAllFigures()

        if flip and self.fallingFigure.blocks:
            self.fallingFigure.flip()
            self.reDrawAllFigures()

        if self.fallingSpeedCounter > self.config.falling_speed:
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
        self.field.drawFigure(self.display, self.staticFigure.get_block_info())
        if self.fallingFigure.blocks:
            self.field.drawFigure(self.display, self.fallingFigure.get_block_info())

    def spawnFallingFigure(self):
        #figure_name = self.field.get_random_figure_name()
        figure_type, block_positions = self.field.getRandomFigurePositions()
        colour = random.choice(list(pygame.color.THECOLORS.values()))
        self.fallingFigure.add_blocks_from_positions(block_positions=block_positions, colour=colour, figure_type=figure_type)

    def destroyFigure(self):
        self.fallingFigure.destroyBlocks()

    def addFallingFigureToStaticFigure(self):
        self.staticFigure.add_blocks(self.fallingFigure.blocks)
        self.fallingFigure.destroyBlocks()
        # check if a row needs to be destroyed
        filledRows = self.staticFigure.get_filled_rows()
        if filledRows:
            print('filledRows', filledRows)
            self.staticFigure.delete_rows(filledRows)
            self.staticFigure.move_all_rows(filledRows)

        self.spawnFallingFigure()
        self.reDrawAllFigures()

    def fallingFigureReachedBottom(self):
        if any([y == self.config.number_of_rows-1 for x, y in self.fallingFigure.get_block_positions()]):
            return True
        return False

    def fallingFigureReachedStaticFigure(self):
        if set(self.staticFigure.get_block_positions()).intersection(set(self.fallingFigure.get_next_positions(dy=1))):
            return True
        return False

    def staticFigureReachedTop(self):
        yPositions = [y for x, y in self.staticFigure.get_block_positions()]
        if yPositions and min(yPositions) <= 2: # bug but this works
            return True
        return False


    def isMovementPossible(self, movement):
        if self.isMovementClippingBorders(movement) or \
           self.isMovementClippingStaticFigure(movement):
            return False
        return True

    def isMovementClippingBorders(self, movement):
        newPositions = self.fallingFigure.get_next_positions(dx=movement)
        if any([x < 0 or x > self.config.number_of_cols-1 for x, y in newPositions]):
            return True
        return False

    def isMovementClippingStaticFigure(self, movement):
        staticPositions = self.staticFigure.get_block_positions()
        fallingPositions = self.fallingFigure.get_next_positions(dx=movement)
        if set(staticPositions).intersection(fallingPositions):
            return True
        return False

    def endGame(self):
        self.message_display('Game Over')

    def message_display(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = self._text_objects(text, largeText)
        TextRect.center = (
            (self.config.display_size[0]/2), 
            (self.config.display_size[1]/2)
            )
        self.display.blit(TextSurf, TextRect)
        pygame.display.update()
        time.sleep(5)

    def _text_objects(self, text, font):
        textSurface = font.render(text, True, (255, 10, 255))
        return textSurface, textSurface.get_rect()
