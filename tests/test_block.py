from falling_blocks.figure import Block

def test_block_init():
    block = Block((0, 0), [1, 2, 3])
    assert (0, 0) == block.position
    assert [1, 2, 3] == block.colour 

def test_block_move():
    block = Block((2, 4), [1, 2, 3])
    block.move(1, 5)
    assert (3, 9) == block.position
