import random
import time

import pygame

from field import Field
from figure import FallingFigure, StaticFigure


class GameController:
    def __init__(self, config):
        self.config = config
        self.field = Field(config)
        self.falling_figure = FallingFigure(config)
        self.static_figure = StaticFigure(config)
        self.falling_speed_counter = 0

    def startGame(self):
        self.display = pygame.display.set_mode(self.config.display_size)
        self.field.draw_field_borders(self.display)
        self.spawn_falling_figure()

    def doNextStep(self, movement=None, flip=False):
        """ Perform next steps """
        if self.falling_figure_reached_bottom() or \
            self.falling_figure_reached_static_figure():

            self.add_falling_figure_to_static_figure()
            self.redraw_all_figures()

        if movement and self.falling_figure.blocks:
            if self.is_movement_possible(movement):
                self.falling_figure.move(dx=movement)
                self.redraw_all_figures()

        if flip and self.falling_figure.blocks:
            self.falling_figure.flip()
            self.redraw_all_figures()

        if self.falling_speed_counter > self.config.falling_speed:
            self.falling_speed_counter = 0
            self.falling_figure.move(dy=1)
            self.redraw_all_figures()

        self.falling_speed_counter += 1

    def isGameOver(self):
        """ Check if game is over """
        if self.static_figure_reached_top():
            return True
        return False

    def redraw_all_figures(self):
        self.field.fill_active_field(self.display)
        self.field.draw_figure(self.display, self.static_figure.get_block_info())
        if self.falling_figure.blocks:
            self.field.draw_figure(self.display, self.falling_figure.get_block_info())

    def spawn_falling_figure(self):
        figure_type, block_positions = self.get_random_figure_positions()
        colour = [
            random.randint(10, 256),
            random.randint(10, 256),
            random.randint(10, 256)
        ]
        self.falling_figure.add_blocks_from_positions(
            block_positions=block_positions, 
            colour=colour, 
            figure_type=figure_type
            )

    def add_falling_figure_to_static_figure(self):
        self.static_figure.add_blocks(self.falling_figure.blocks)
        self.falling_figure.destroy_blocks()
        # check if a row needs to be destroyed
        filled_rows = self.static_figure.get_filled_rows()
        if filled_rows:
            print('filled_rows', filled_rows)
            self.static_figure.delete_rows(filled_rows)
            self.static_figure.move_all_rows(filled_rows)

        self.spawn_falling_figure()
        self.redraw_all_figures()

    def falling_figure_reached_bottom(self):
        bottom_row = self.config.number_of_rows - 1
        for _x, y in self.falling_figure.get_block_positions():
            if y == bottom_row:
                return True
        return False

    def falling_figure_reached_static_figure(self):
        next_positions = self.falling_figure.get_next_positions(dy=1)
        current_positions = self.static_figure.get_block_positions()
        if set(current_positions).intersection(set(next_positions)):
            return True
        return False

    def static_figure_reached_top(self):
        y_positions = [y for x, y in self.static_figure.get_block_positions()]
        if y_positions and min(y_positions) <= 2: # bug but this works
            return True
        return False


    def is_movement_possible(self, movement):
        if self.is_movement_clipping_borders(movement) or \
           self.is_movement_clipping_static_figure(movement):
            return False
        return True

    def is_movement_clipping_borders(self, movement):
        new_positions = self.falling_figure.get_next_positions(dx=movement)
        if any([x < 0 or x > self.config.number_of_cols-1 for x, y in new_positions]):
            return True
        return False

    def is_movement_clipping_static_figure(self, movement):
        static_positions = self.static_figure.get_block_positions()
        falling_positions = self.falling_figure.get_next_positions(dx=movement)
        if set(static_positions).intersection(falling_positions):
            return True
        return False

    def endGame(self):
        self.message_display('Game Over')

    def message_display(self, text):
        large_text = pygame.font.Font('freesansbold.ttf', 90)
        text_surf, text_rect = self._text_objects(text, large_text)
        text_rect.center = (
            (self.config.display_size[0]/2), 
            (self.config.display_size[1]/2)
            )
        self.display.blit(text_surf, text_rect)
        pygame.display.update()
        time.sleep(5)

    def _text_objects(self, text, font):
        text_surface = font.render(text, True, (255, 10, 255))
        return text_surface, text_surface.get_rect()

    def get_random_figure_positions(self):
        figure_type = random.choice(list(self.config.figure_positions.keys()))
        return (figure_type, 1), self.config.figure_positions.get(figure_type).get(1)