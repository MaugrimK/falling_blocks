import random
from falling_blocks.field import Field


def test_get_random_figure(monkeypatch):
    monkeypatch.setattr(random, 'choice', lambda x: x[0])
    figure_config = {'fig_1': 'a', 'fig_2': 'b', 'fig_3': 'c'}
    field = Field()
    res = field.get_random_figure_name(figure_config)
    assert 'fig_1' == res