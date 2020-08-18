import pygame
from configurations import PART_OF_MAP_WIDTH, PART_OF_MAP_HEIGHT, SCHEMA_LETTER_TO_BLOCK
from levels import LEVELS


class MapPart(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, level: int):
        super(MapPart, self).__init__()

        self.symbol = LEVELS[level][y][x]
        self.path_to_image = SCHEMA_LETTER_TO_BLOCK[self.symbol]
        self.image = pygame.transform.scale(pygame.image.load(f'Textures/blocks/{self.path_to_image}'),
                                            (PART_OF_MAP_WIDTH, PART_OF_MAP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x * PART_OF_MAP_WIDTH
        self.rect.y = y * PART_OF_MAP_HEIGHT

    def is_obstacle(self):
        return False if self.symbol == '.' else True
