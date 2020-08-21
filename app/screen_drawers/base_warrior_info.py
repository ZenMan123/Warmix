import pygame

from app.configurations.files_configurations import PATH_TO_ICONS, HEALTH_ICON_NAME, BULLET_ICON_NAME, POWER_ICON_NAME, \
    TIME_ICON_NAME
from app.configurations.colors_configuration import RED, BLUE, GRAY, PURPLE
from app.configurations.position_configurations import WARRIOR_INFO_DELTA_X, WARRIOR_INFO_DELTA_Y, WARRIOR_INFO_POSITION

from app.warriors.base_warrior import BaseWarrior
from .banners import BannerIcon, BannerText

from time import time


class BaseWarriorInfo:
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

    def form_and_set_warrior_info(self):
        self.info['health'][1].update_text(self.warrior.health)
        self.info['power'][1].update_text(self.warrior.power)

        seconds_from_init = int(time() - self.warrior.game.init_time)
        minutes = seconds_from_init // 60
        seconds = seconds_from_init % 60
        self.info['time'][1].update_text(f'{str(minutes).rjust(2, "0")}:{str(seconds).rjust(2, "0")}')

    def get_data(self):
        # TODO correct it
        return list(value[0] for value in self.info.values()) + list(value[1] for value in self.info.values())
