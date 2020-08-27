from game_server.client import Client
from .base_warrior import BaseWarrior
from app.dynamic_weapons.bullet import Bullet
from app.game.game import Game

from app.services_for_game.camera import Camera
from app.services_for_game.music import Music

from app.configurations.modes_configuration import LEFT, RIGHT
from time import time
import pygame

from ..screen_drawers.shooting_warrior_info import ShootingWarriorInfo


class ShootingWarrior(BaseWarrior):
    def __init__(self, login: str, warrior_name: str, camera: Camera, game: Game, music: Music,
                 init_side: str = 'right', client: Client = None):
        super(ShootingWarrior, self).__init__(login, warrior_name, camera, game, music, init_side, client)

        self.magazine_capacity = self.conditions['attack']['magazine_capacity'] = self.data["magazine_capacity"]
        self.reloading_speed = self.conditions['attack']['reloading_speed'] = self.data["reloading_speed"]
        self.bullet_speed = self.conditions['attack']['bullet_speed'] = self.data["bullet_speed"]
        self.delta_shooting = self.conditions['attack']['delta_shooting'] = self.data["delta_shooting"]
        self.bullet_distance = self.conditions['attack']['bullet_distance'] = self.data["bullet_distance"]

        self.bullets: pygame.sprite.Group = pygame.sprite.Group()
        self.active_bullets: pygame.sprite.Group = pygame.sprite.Group()
        self._reload_magazine()

        self.last_bullet_adding_time = time()
        self.last_trying_to_shoot_time = time()

        self.info = ShootingWarriorInfo(self)

    def _attack(self) -> None:
        self.deactivate('attack')

        if time() - self.last_trying_to_shoot_time < self.delta_shooting:
            return
        self.last_trying_to_shoot_time = time()

        if not self.bullets:
            self.music.play_empty_magazine_sound()
            return

        self.music.play_bullet_shooting_sound()
        self.active_bullets.add(self.prepare_new_active_bullet())

    def update(self) -> None:
        self.check_for_new_bullets()
        super().update()

    def check_for_new_bullets(self):
        if time() - self.last_bullet_adding_time >= self.reloading_speed and len(self.bullets) < self.magazine_capacity:
            self.last_bullet_adding_time = time()
            self.bullets.add(Bullet(self, self.game, self.power, self.bullet_distance))

    def _reload_magazine(self):
        for _ in range(self.magazine_capacity):
            self.bullets.add(Bullet(self, self.game, self.power, self.bullet_distance))

    def prepare_new_active_bullet(self) -> Bullet:
        bullet: Bullet = self.bullets.sprites()[0]
        self.bullets.remove(bullet)

        bullet.set_direction_x(self.last_side)
        bullet.set_bullet_speed_x(self.bullet_speed)
        bullet.set_bullet_speed_y(0)
        bullet.set_coord((self.rect.x if self.last_side == LEFT else self.rect.x + self.rect.width,
                          self.rect.y + self.rect.height // 2))
        bullet.start()

        return bullet
