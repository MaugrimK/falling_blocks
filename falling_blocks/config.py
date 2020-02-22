FPS = 10
# fps is 60 and then define another variable how fall the figures fall

DISPLAY_SIZE = (600, 700)
FALLING_SPEED = 2

BLOCK_SIDE_SIZE = 20

FIELD_START_X = 200
FIELD_START_Y = 300

FIELD_END_X = 500
FIELD_END_Y = 600

NUMBER_OF_COLS = (FIELD_END_X - FIELD_START_X) / BLOCK_SIDE_SIZE
NUMBER_OF_ROWS = (FIELD_END_Y - FIELD_START_Y) / BLOCK_SIDE_SIZE
BORDER_THICKNESS = 10

FIGURE_POSITIONS = {'zFigure': {1: [(0, 1), (1, 1), (1, 0), (2, 0)],
                                2: [(0, 0), (0, 1), (1, 1), (1, 2)]},

                    'oFigure': {1: [(0, 0), (1, 0), (0, 1), (1, 1)]},

                    'lFigure': {1: [(0, 0), (1, 0), (2, 0), (0, 1)],
                                2: [(0, 0), (0, 1), (0, 2), (1, 2)],
                                3: [(2, 0), (0, 1), (1, 1), (2, 1)],
                                4: [(0, 0), (1, 0), (1, 1), (1, 2)]},
                                
                    'iFigure': {1: [(0, 0), (1, 0), (2, 0), (3, 0)],
                                2: [(0, 0), (0, 1), (0, 2), (0, 3)]}, }