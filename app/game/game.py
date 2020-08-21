import pygame

from app.configurations.size_configurations import AMOUNT_OF_PARTS_IN_COL, AMOUNT_OF_PARTS_IN_ROW

from app.map.map_part import create_map_part
from app.map.block import Block
from app.map.icon import Icon
from app.map.background import Background

from time import time

pygame.init()

# TODO надо сделать отдельный класс для отображения информации о пользователе
# TODO а класс Game о BaseWarrior знать ничего не должен


class Game:
    def __init__(self, warriors: pygame.sprite.Group, level: int):
        self.level = level

        self.warriors = warriors
        self.map_tombstones_group = pygame.sprite.Group()
        self.map_background_group = pygame.sprite.Group()
        self.map_blocks_group = pygame.sprite.Group()
        self.map_icons_group = pygame.sprite.Group()
        self.map_bullets_group = pygame.sprite.Group()
        self.groups = [self.map_background_group, self.map_blocks_group, self.map_icons_group, self.map_tombstones_group, self.map_bullets_group, self.warriors]

        for x in range(AMOUNT_OF_PARTS_IN_ROW):
            for y in range(AMOUNT_OF_PARTS_IN_COL):
                self.create_map_part(x, y)

        self.init_time = time()

    def create_map_part(self, x, y):
        map_image = create_map_part(x, y, self.level)
        if type(map_image) == Block:
            self.map_blocks_group.add(map_image)
        elif type(map_image) == Icon:
            self.map_icons_group.add(map_image)
            self.map_background_group.add(Background(x, y, self.level, '.'))
        else:
            self.map_background_group.add(map_image)