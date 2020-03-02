import pytest

from falling_blocks.block import Block
from falling_blocks.figure import Figure, StaticFigure, FallingFigure


def test_figure_add_blocks():
    fig = Figure()
    assert [] == fig.blocks

    block1 = Block((1, 2), [1, 2, 3])
    fig.add_blocks([block1])
    assert [block1] == fig.blocks


def test_figure_move():
    fig = Figure()
    block1 = Block((1, 2), [1, 2, 3])
    block2 = Block((3, 4), [1, 2, 3])
    fig.add_blocks([block1, block2])

    fig.move(2, 4)
    assert [(3, 6), (5, 8)] == fig.get_block_positions()

    fig.move(1, 4)
    assert [(4, 10), (6, 12)] == fig.get_block_positions()
    fig.move(1)
    assert [(5, 10), (7, 12)] == fig.get_block_positions()
    fig.move(0, 1)
    assert [(5, 11), (7, 13)] == fig.get_block_positions()

    res = [
        ((5, 11), [1, 2, 3]), 
        ((7, 13), [1, 2, 3])
        ]
    assert res == fig.get_block_info()


class Config:
    number_of_cols = 4

@pytest.fixture
def static_figure():
    fig = StaticFigure(Config)
    c = [0, 0, 0]
    # Add the following static figure
    # 1111
    # 1001
    # 1111
    # 1010
    # 1111

    fig.add_blocks([
        Block((0, 0), c), Block((1, 0), c), Block((2, 0), c), Block((3, 0), c),
        Block((0, 1), c), Block((3, 1), c),
        Block((0, 2), c), Block((1, 2), c), Block((2, 2), c), Block((3, 2), c),
        Block((0, 3), c), Block((2, 3), c),
        Block((0, 4), c), Block((1, 4), c), Block((2, 4), c), Block((3, 4), c),
    ])
    return fig

@pytest.fixture
def falling_figure():
    fig = FallingFigure()
    fig.add_blocks_from_positions(
        [(0, 0), (0, 1)], 
        [1, 2, 3], 
        'iFigure'
        )
    return fig


def test_static_figure_get_filled_rows(static_figure):
    filled_rows = static_figure.get_filled_rows()
    assert [0, 2, 4] == filled_rows
    

def test_static_figure_delete_rows(static_figure):
    static_figure.delete_rows([0, 2, 4])
    pos = static_figure.get_block_positions()
    assert [(0, 1), (3, 1), (0, 3), (2, 3)] == pos


def test_static_figure_move_all_rows(static_figure):
    static_figure.delete_rows([0, 2, 4])
    static_figure.move_all_rows([0, 2, 4])
    pos = static_figure.get_block_positions()
    assert [(0, 3), (3, 3), (0, 4), (2, 4)] == pos


def test_falling_figure_add_blocks_from_posisions(falling_figure):
    pos = falling_figure.get_block_positions()
    assert [(0, 0), (0, 1)] == pos

def test_falling_figure_get_next_positions(falling_figure):
    pos = falling_figure.get_next_positions(2, 2)
    assert [(2, 2), (2, 3)] == pos

def test_falling_figure_flip():
    pass