import pygame

from configurations.size_configurations import *
from configurations.files_configurations import *
from configurations.colors_configuration import *
from configurations.size_configurations import *
from configurations.position_configurations import *

from map.map_part import MapPart, create_map_part
from map.block import Block
from map.icon import Icon
from map.background import Background

from services_for_game.camera import Camera
from services_for_game.music import Music

from warriors.base_warrior import BaseWarrior

from time import time

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()


class Game:
    def __init__(self, warrior: BaseWarrior, enemies: pygame.sprite.Group,
                 camera: Camera, screen: pygame.Surface, level: int):

        self.level = level
        self.map_background_group = pygame.sprite.Group()
        self.map_blocks_group = pygame.sprite.Group()
        self.map_icons_group = pygame.sprite.Group()

        for x in range(AMOUNT_OF_PARTS_IN_ROW):
            for y in range(AMOUNT_OF_PARTS_IN_COL):
                self.create_map_part(x, y)


        self.warrior = warrior
        self.warrior.game = self
        self.enemies = enemies

        self.screen = screen
        self.camera = camera
        self.font = pygame.font.Font(None, 36)

        self.music = Music()
        self.music.start()

        self.load_warrior_info_images_and_texts()
        self.init_time = time()

    def load_warrior_info_images_and_texts(self):
        self.warrior_health = pygame.transform.scale(pygame.image.load(f'{PATH_TO_ICONS}/{HEALTH_ICON_NAME}'),
                                                     INFO_SIZE)
        self.warrior_power = pygame.transform.scale(pygame.image.load(f'{PATH_TO_ICONS}/{POWER_ICON_NAME}'), INFO_SIZE)
        self.warrior_time = pygame.transform.scale(pygame.image.load(f'{PATH_TO_ICONS}/{TIME_ICON_NAME}'), INFO_SIZE)

        self.warrior_health_text = self.font.render(str(self.warrior.health), 1, RED)
        self.warrior_power_text = self.font.render(str(self.warrior.power), 1, BLUE)
        self.warrior_time_text = self.font.render('00:00', 1, GRAY)

    def create_map_part(self, x, y):
        map_image = create_map_part(x, y, self.level)
        if type(map_image) == Block:
            self.map_blocks_group.add(map_image)
        elif type(map_image) == Icon:
            self.map_icons_group.add(map_image)
            self.map_background_group.add(Background(x, y, self.level, '.'))
        else:
            self.map_background_group.add(map_image)

    def draw(self):
        self.form_and_set_time_string()
        self.form_and_set_warrior_info()

        self.screen.fill((255, 255, 255))
        for group in [self.map_background_group, self.map_blocks_group, self.enemies, self.map_icons_group]:
            for obj in group:
                self.screen.blit(obj.image, self.camera.apply(obj))

        self.draw_warrior_info()
        self.screen.blit(self.warrior.image, self.camera.apply(self.warrior))

        pygame.display.flip()

    def draw_warrior_info(self):
        self.screen.blit(self.warrior_health, WARRIOR_HEALTH_POSITION)
        self.screen.blit(self.warrior_health_text,
                         (WARRIOR_HEALTH_POSITION[0] + WARRIOR_INFO_DELTA, WARRIOR_HEALTH_POSITION[1]))

        self.screen.blit(self.warrior_power, WARRIOR_POWER_POSITION)
        self.screen.blit(self.warrior_power_text,
                         (WARRIOR_POWER_POSITION[0] + WARRIOR_INFO_DELTA, WARRIOR_POWER_POSITION[1]))

        self.screen.blit(self.warrior_time, WARRIOR_TIME_POSITION)
        self.screen.blit(self.warrior_time_text,
                         (WARRIOR_TIME_POSITION[0] + WARRIOR_INFO_DELTA, WARRIOR_TIME_POSITION[1]))

    def set_time(self, time: str):
        self.warrior_time_text = self.font.render(time, 1, GRAY)

    def set_health(self, health: str):
        self.warrior_health_text = self.font.render(health, 1, RED)

    def set_power(self, power: str):
        self.warrior_power_text = self.font.render(power, 1, BLUE)

    def form_and_set_time_string(self):
        seconds_from_init = int(time() - self.init_time)
        minutes = seconds_from_init // 60
        seconds = seconds_from_init % 60
        self.set_time(f'{str(minutes).rjust(2, "0")}:{str(seconds).rjust(2, "0")}')

    def form_and_set_warrior_info(self):
        self.set_health(str(self.warrior.health))
        self.set_power(str(self.warrior.power))
