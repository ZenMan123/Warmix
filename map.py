import pygame
from configurations import PART_OF_MAP_WIDTH, PART_OF_MAP_HEIGHT, SCHEMA_LETTER_TO_BLOCK, \
    ICON_SIZE, ICON_WIDTH
from levels import LEVELS


class MapPart(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, level: int, symbol: str = None):
        super(MapPart, self).__init__()

        self.symbol = LEVELS[level][y][x] if symbol is None else symbol
        self.path_to_image = SCHEMA_LETTER_TO_BLOCK[self.symbol]

        self.full_path = None
        self.size = None
        if self.is_obstacle():
            self.full_path = 'Textures/blocks'
            self.size = (PART_OF_MAP_WIDTH, PART_OF_MAP_HEIGHT)
        elif self.is_background():
            self.full_path = 'Textures/backgrounds'
            self.size = (PART_OF_MAP_WIDTH, PART_OF_MAP_HEIGHT)
        elif self.is_icon():
            self.full_path = 'Textures/icons'
            self.size = ICON_SIZE

        self.image = pygame.transform.scale(pygame.image.load(f'{self.full_path}/{self.path_to_image}'),
                                            self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x * PART_OF_MAP_WIDTH
        self.rect.y = y * PART_OF_MAP_HEIGHT

        if self.is_icon():
            self.rect.x += (PART_OF_MAP_WIDTH - ICON_WIDTH) // 2
            self.rect.y += PART_OF_MAP_HEIGHT - self.rect.height - 5

    def is_obstacle(self):
        return True if self.symbol in ['G', 'P', 'U', 'W'] else False

    def is_background(self):
        return self.symbol == '.'

    def is_icon(self):
        return True if self.symbol in ['A', 'S', 'T'] else False

    def get_icon_type(self):
        if self.symbol == 'A':
            return 'apple'
        if self.symbol == 'S':
            return 'shield'
        if self.symbol == 'T':
            return 'potion'
