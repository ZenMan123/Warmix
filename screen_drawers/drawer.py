from game.game import Game
from .warrior_info import WarriorInfo
from warriors.base_warrior import BaseWarrior
from services_for_game.camera import Camera
import pygame


class Drawer:
    def __init__(self, screen, game: Game, camera: Camera, main_warrior: BaseWarrior, main_warrior_info: WarriorInfo):
        self.screen = screen
        self.game = game
        self.camera = camera
        self.main_warrior = main_warrior
        self.main_warrior_info = main_warrior_info

    def draw(self):
        self.main_warrior_info.form_and_set_warrior_info()
        self.main_warrior_info.form_and_set_time_string()

        self.screen.fill((255, 255, 255))
        for group in self.game.groups:
            for obj in group:
                self.screen.blit(obj.image, self.camera.apply(obj))
        for i in self.main_warrior_info.get_data():
            self.screen.blit(i.image, i.coords)
        print(self.main_warrior.image)
        self.screen.blit(self.main_warrior.image, self.camera.apply(self.main_warrior))

        pygame.display.flip()
