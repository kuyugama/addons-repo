from src.util import string


def test_snake_to_pascal(timer):
    assert string.snake_to_pascal("famous_potato") == "FamousPotato"
