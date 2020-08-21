from app.game.game import Game
from .base_warrior_info import BaseWarriorInfo
from app.warriors.base_warrior import BaseWarrior
from app.services_for_game.camera import Camera
import pygame


class Drawer:
    def __init__(self, screen, game: Game, camera: Camera, main_warrior: BaseWarrior, main_warrior_info: BaseWarriorInfo):
        self.screen = screen
        self.game = game
        self.camera = camera
        self.main_warrior = main_warrior
        self.main_warrior_info = main_warrior_info

    def draw(self):
        self.main_warrior_info.form_and_set_warrior_info()

        self.screen.fill((255, 255, 255))
        for group in self.game.groups:
            for obj in group:
                if obj == self.main_warrior:
                    continue
                self.screen.blit(obj.image, self.camera.apply(obj))

        for i in self.main_warrior_info.get_data():
            self.screen.blit(i.image, i.coords)
        self.screen.blit(self.main_warrior.image, self.camera.apply(self.main_warrior))

        pygame.display.flip()
