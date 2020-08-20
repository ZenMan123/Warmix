import pygame
from configurations.files_configurations import PATH_TO_ICONS, HEALTH_ICON_NAME, POTION_ICON_NAME, POWER_ICON_NAME, \
    TIME_ICON_NAME
from configurations.colors_configuration import RED, BLUE, GRAY
from configurations.size_configurations import INFO_SIZE
from configurations.position_configurations import WARRIOR_INFO_DELTA_X, WARRIOR_INFO_DELTA_Y, WARRIOR_INFO_POSITION
from warriors.base_warrior import BaseWarrior
from time import time


class WarriorInfo:
    def __init__(self, warrior: BaseWarrior):
        self.warrior = warrior
        self.font = pygame.font.Font(None, 36)
        self.info_banners = pygame.sprite.Group()
        self.info_categories = [
            ('health', str(self.warrior.health), RED, HEALTH_ICON_NAME),
            ('power', str(self.warrior.power), BLUE, POWER_ICON_NAME),
            ('time', '00:00', GRAY, TIME_ICON_NAME)
        ]
        self.info = {}
        self.delta_y = 0
        self.load_warrior_info()

    def load_warrior_info(self):
        for category in self.info_categories:
            self.add_category(*category)

    def add_category(self, name, text, color, path):
        pos = WARRIOR_INFO_POSITION[0], WARRIOR_INFO_POSITION[1] + self.delta_y
        self.info[name] = [BannerIcon(f'{PATH_TO_ICONS}/{path}', pos),
                           BannerText(self.font, text, color, (pos[0] + WARRIOR_INFO_DELTA_X, pos[1]))]
        self.delta_y += WARRIOR_INFO_DELTA_Y

    def form_and_set_time_string(self):
        seconds_from_init = int(time() - self.warrior.game.init_time)
        minutes = seconds_from_init // 60
        seconds = seconds_from_init % 60
        self.info['time'][1].update_text(f'{str(minutes).rjust(2, "0")}:{str(seconds).rjust(2, "0")}')

    def form_and_set_warrior_info(self):
        self.info['health'][1].update_text(self.warrior.health)
        self.info['power'][1].update_text(self.warrior.power)

    def get_data(self):
        # TODO correct it
        return list(value[0] for value in self.info.values()) + list(value[1] for value in self.info.values())


class BannerIcon:
    def __init__(self, path, coords):
        self.image = pygame.transform.scale(pygame.image.load(path), INFO_SIZE)
        self.coords = coords


class BannerText:
    def __init__(self, font: pygame.font.Font, string: str, color: tuple, coords):
        self.font = font
        self.string = string
        self.color = color
        self.coords = coords
        self.image = self.font.render(self.string, 1, self.color)

    def update_text(self, string):
        self.string = string
        self.image = self.font.render(str(self.string), 1, self.color)

    def update_color(self, color):
        self.color = color
        self.image = self.font.render(self.string, 1, self.color)
