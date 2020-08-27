import pygame

from app.configurations.levels_configuration import *
from app.configurations.size_configurations import *
from app.levels.levels import LEVELS


class MapPart(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, level: int, symbol: str = None):
        super(MapPart, self).__init__()
        self.x = x
        self.y = y
        self.level = level
        self.symbol = LEVELS[level][y][x] if symbol is None else symbol

    def set_size_and_image(self, size, path):
        self.image = pygame.transform.scale(pygame.image.load(path), size)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * PART_OF_MAP_WIDTH
        self.rect.y = self.y * PART_OF_MAP_HEIGHT


def create_map_part(x, y, level, music, symbol=None):
    from .icon import Icon
    from .block import Block
    from .background import Background

    symbol = LEVELS[level][y][x] if symbol is None else symbol
    part_type = SCHEMA_LETTER_TO_TYPE[symbol]
    if part_type == 'icon':
        return Icon(x, y, level, symbol, music)
    if part_type == 'block':
        return Block(x, y, level, symbol)
    if part_type == 'background':
        return Background(x, y, level, symbol)
