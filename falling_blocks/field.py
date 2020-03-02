import random

import pygame


class Field:
    def __init__(self, config=None):
        self.config = config

    def drawFigure(self, display, figureInfo):
        for blockPosition, colour in figureInfo:
            pixels = self.translatePositionToPixels(blockPosition)
            pygame.draw.rect(display, colour, pygame.Rect(pixels))

    def fillActiveField(self, display):
        display.fill((0, 0, 0), rect=pygame.Rect(self.config.field_start_x, self.config.field_start_y,
                                                 self.config.field_end_x-self.config.field_start_x,
                                                 self.config.field_end_y-self.config.field_start_y))

    def translatePositionToPixels(self, position):
        xStart = self.config.field_start_x + position[0] * self.config.block_side_size
        yStart = self.config.field_start_y + position[1] * self.config.block_side_size
        return xStart, yStart, self.config.block_side_size, self.config.block_side_size

    def drawFieldBorders(self, display):
        # x, y, x_thickness, y_thickness
        leftBorder = (self.config.field_start_x-self.config.border_thickness, self.config.field_start_y, self.config.border_thickness,
                      self.config.field_end_y-self.config.field_start_y+self.config.border_thickness)
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(leftBorder))
        rightBorder = (self.config.field_end_x, self.config.field_start_y, self.config.border_thickness,
                       self.config.field_end_y-self.config.field_start_y+self.config.border_thickness)
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(rightBorder))
        bottomBorder = (self.config.field_start_x, self.config.field_end_y, self.config.field_end_x-self.config.field_start_x, self.config.border_thickness)
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(bottomBorder))

    def getRandomFigurePositions(self):

        figure_type = random.choice(list(self.config.figure_positions.keys()))
        return (figure_type, 1), self.config.figure_positions.get(figure_type).get(1)

    def get_random_figure_name(self, figure_config: dict) -> str:
        return random.choice(sorted(list(figure_config.keys())))

    def get_first_figure_positions(
        self, 
        figure_name: str, 
        figure_config: dict
        ) -> list:
        pos = figure_config.get_figure(figure_name).get(1)
        return pos



