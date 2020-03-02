class Config:
    fps = 10
    # fps is 60 and then define another variable how fall the figures fall
    display_size = (600, 700)
    falling_speed = 2
    block_side_size = 20
    field_start_x = 200
    field_start_y = 300
    field_end_x = 500
    field_end_y = 600

    number_of_cols = (field_end_x - field_start_x) / block_side_size
    number_of_rows = (field_end_y - field_start_y) / block_side_size

    border_thickness = 10

    figure_positions = {
        'z_figure': {
            1: [(0, 1), (1, 1), (1, 0), (2, 0)],
            2: [(0, 0), (0, 1), (1, 1), (1, 2)]
            },

        'o_figure': {
            1: [(0, 0), (1, 0), (0, 1), (1, 1)]
            },

        'l_figure': {
            1: [(0, 0), (1, 0), (2, 0), (0, 1)],
            2: [(0, 0), (0, 1), (0, 2), (1, 2)],
            3: [(2, 0), (0, 1), (1, 1), (2, 1)],
            4: [(0, 0), (1, 0), (1, 1), (1, 2)]
            },
                    
        'i_figure': {
            1: [(0, 0), (1, 0), (2, 0), (3, 0)],
            2: [(0, 0), (0, 1), (0, 2), (0, 3)]
            }, 
        }