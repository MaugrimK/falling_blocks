from falling_blocks.block import Block

class Figure:
    def __init__(self):
        self.blocks = []

    def add_blocks(self, blocks: list):
        '''
        Args:
            blocks: list of Block objects
        '''
        self.blocks.extend(blocks)

    def move(self, dx: int = 0, dy: int = 0):
        '''
        Top left corner is 0, 0; bottom right corner is x, y
        '''
        for block in self.blocks:
            block.move(dx, dy)

    def get_block_positions(self) -> list:
        '''
        Returns: list of tuples with x, y coordinates
        '''
        return [block.position for block in self.blocks]

    def get_block_info(self) -> list:
        return [(block.position, block.colour) for block in self.blocks]


class StaticFigure(Figure):
    def __init__(self, config=None):
        super(StaticFigure, self).__init__()
        self.config = config

    def get_filled_rows(self) -> list:
        '''Return y positions rows that are filled with blocks'''
        filled_rows = []
        blocks_positions = self.get_block_positions()
        y_positions = [y for x, y in blocks_positions]
        for y_position in set(y_positions):
            if y_positions.count(y_position) == self.config.number_of_cols:
                # the whole row is filled
                filled_rows.append(y_position)
        return filled_rows

    def delete_rows(self, rows: list):
        '''
        Args:
            rows: y positions of the rows to delete
        '''       
        blocks_to_keep = []
        for block in self.blocks:
            _x, y = block.position
            if y not in rows:
                blocks_to_keep.append(block)
        self.blocks = blocks_to_keep

    def move_all_rows(self, filled_rows: list):
        '''
        Move all rows down after filled rows were deleted. Handles case if 
        multiple rows were removed.
        Args:
            filled_rows: y positions of the deleted filled rows
        '''
        blocks_to_move = []
        for y_pos in sorted(filled_rows):
            for block in self.blocks:
                _x, y = block.position
                if y < y_pos:
                    blocks_to_move.append(block)

        for block in blocks_to_move:
            block.move(dy=1)


class FallingFigure(Figure):
    def __init__(self, config=None):
        self.config = config
        self.figure_name = None
        self.figure_orientation = None
        self.colour = None
        super(FallingFigure, self).__init__()

    def add_blocks_from_positions(
        self, 
        block_positions: list, 
        colour: list, 
        figure_type: list
        ):
        self.figure_type = figure_type
        self.colour = colour
        for block_position in block_positions:
            self.blocks.append(Block(position=block_position, colour=colour))

    def get_next_positions(self, dx: int = 0, dy: int = 0):
        return [(x + dx, y + dy) for x, y in self.get_block_positions()]

    def flip(self):
        figure_name, new_type_number = self.get_next_figure_type_number()
        ref_position = self.get_reference_point()
        new_positions = self.get_flipped_figure_positions(
            figure_name, 
            new_type_number, 
            ref_position
            )
        self.destroy_blocks()
        self.add_blocks_from_positions(
            block_positions=new_positions, 
            colour=self.colour, 
            figure_type=(figure_name, new_type_number)
            )

    def get_next_figure_type_number(self):
        figure_name, type_number = self.figure_type[0], self.figure_type[1]
        possible_types = len(self.config.figure_positions.get(figure_name).keys())
        if type_number + 1 > possible_types:
            new_type_number = 1
        else:
            new_type_number = type_number + 1

        return figure_name, new_type_number

    def get_reference_point(self):
        positions = self.get_block_positions()
        min_x_position = min([x for x, y in positions])
        min_y_position = min([y for x, y in positions])
        return min_x_position, min_y_position

    def get_flipped_figure_positions(self, figure_name, new_type_number, ref_position):
        relative_positions = self.config.figure_positions.get(figure_name).get(new_type_number)
        true_positions = [(x + ref_position[0], y + ref_position[1]) for x, y in relative_positions]
        return true_positions

    def destroy_blocks(self):
        self.blocks = []
        self.figure_type = None
