import random

import pygame


class Field:
    def __init__(self, config=None):
        self.config = config

    def draw_figure(self, display, figure_info):
        for block_position, colour in figure_info:
            pixels = self.translate_position_to_pixels(block_position)
            pygame.draw.rect(display, colour, pygame.Rect(pixels))

    def fill_active_field(self, display):
        display.fill((0, 0, 0), rect=pygame.Rect(
            self.config.field_start_x, 
            self.config.field_start_y,
            self.config.field_end_x - self.config.field_start_x,
            self.config.field_end_y - self.config.field_start_y
            ))

    def translate_position_to_pixels(self, position):
        x_start = self.config.field_start_x + position[0] * self.config.block_side_size
        y_start = self.config.field_start_y + position[1] * self.config.block_side_size
        return x_start, y_start, self.config.block_side_size, self.config.block_side_size

    def draw_field_borders(self, display):
        # x, y, x_thickness, y_thickness
        left_border = (
            self.config.field_start_x - self.config.border_thickness, 
            self.config.field_start_y, 
            self.config.border_thickness,
            self.config.field_end_y - self.config.field_start_y + self.config.border_thickness
            )
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(left_border))

        right_border = (
            self.config.field_end_x, 
            self.config.field_start_y, 
            self.config.border_thickness,
            self.config.field_end_y - self.config.field_start_y + self.config.border_thickness
            )
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(right_border))

        bottom_border = (
            self.config.field_start_x, 
            self.config.field_end_y, 
            self.config.field_end_x - self.config.field_start_x, 
            self.config.border_thickness
            )
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(bottom_border))




