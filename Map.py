import pygame
from configurations import PART_OF_MAP_WIDTH, PART_OF_MAP_HEIGHT


class MapPart(pygame.sprite.Sprite):
    def __init__(self, path_to_map_image: str, row: int, col: int):
        super(MapPart, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load(f'Textures/backgrounds/{path_to_map_image}'),
                                            (PART_OF_MAP_WIDTH, PART_OF_MAP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = row * PART_OF_MAP_WIDTH
        self.rect.y = col * PART_OF_MAP_HEIGHT
