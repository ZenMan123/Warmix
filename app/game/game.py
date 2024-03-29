from typing import Dict

import pygame

from app.configurations.size_configurations import AMOUNT_OF_PARTS_IN_COL, AMOUNT_OF_PARTS_IN_ROW

from app.map.map_part import create_map_part
from app.map.block import Block
from app.map.icon import Icon
from app.map.background import Background

from time import time

pygame.init()


class Game:
    def __init__(self, warriors: Dict[str, pygame.sprite.Sprite], level: int, music):
        self.level = level
        self.music = music

        self.warriors = warriors
        self.map_tombstones_group = pygame.sprite.Group()
        self.map_background_group = pygame.sprite.Group()
        self.map_blocks_group = pygame.sprite.Group()
        self.map_icons_group = pygame.sprite.Group()
        self.dynamic_weapons_group = pygame.sprite.Group()
        self.groups = [self.map_background_group, self.map_blocks_group, self.map_icons_group, self.map_tombstones_group, self.dynamic_weapons_group]

        for x in range(AMOUNT_OF_PARTS_IN_ROW):
            for y in range(AMOUNT_OF_PARTS_IN_COL):
                self.create_map_part(x, y)

        self.init_time = time()

    def create_map_part(self, x, y):
        map_image = create_map_part(x, y, self.level, self.music)
        if type(map_image) == Block:
            self.map_blocks_group.add(map_image)
        elif type(map_image) == Icon:
            self.map_icons_group.add(map_image)
            self.map_background_group.add(Background(x, y, self.level, '.'))
        else:
            self.map_background_group.add(map_image)

    def update_objects(self):
        for warrior in self.warriors.values():
            warrior.update()
        for weapon in self.dynamic_weapons_group:
            weapon.update()
