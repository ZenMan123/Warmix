import pygame
from app.configurations.files_configurations import PATH_TO_ICONS, RIP_ICON_NAME
from app.configurations.size_configurations import RIP_SIZE


class TombStone(pygame.sprite.Sprite):
    def __init__(self, warrior_dying_rect, game):
        super().__init__()
        self.game = game

        self.path = f'{PATH_TO_ICONS}/{RIP_ICON_NAME}'
        self.image = pygame.transform.scale(pygame.image.load(self.path), RIP_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = warrior_dying_rect.x, warrior_dying_rect.y

        self.game.map_tombstones_group.add(self)

