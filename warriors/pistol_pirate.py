from .base_warrior import BaseWarrior
from services_for_game.camera import Camera
from configurations.modes_configuration import LEFT, RIGHT
from weapons.bullet import Bullet
from typing import List
from time import time
import pygame


class PistolPirate(BaseWarrior):
    def __init__(self, warrior_name: str, camera: Camera, init_side: str = 'right'):
        super(PistolPirate, self).__init__(warrior_name, camera, init_side)

        self.magazine_capacity = self.conditions['attack']['magazine_capacity'] = self.data["magazine_capacity"]
        self.reloading_speed = self.conditions['attack']['reloading_speed'] = self.data["reloading_speed"]
        self.bullet_speed = self.conditions['attack']['bullet_speed'] = self.data["bullet_speed"]

        self.bullets: pygame.sprite.Group = pygame.sprite.Group()
        self.active_bullets: pygame.sprite.Group = pygame.sprite.Group()

        self.last_bullet_adding_time = time()

    def _attack(self) -> None:
        if not self.bullets:
            return

        self.active_bullets.add(self.prepare_new_active_bullet())
        self.deactivate('attack')

    def update(self) -> None:
        for bullet in self.active_bullets:
            bullet.move()
        self.check_for_new_bullets()
        super().update()
        print(f'Bullets: {len(self.bullets)}, Active bullets: {len(self.active_bullets)}')

    def check_for_new_bullets(self):
        if time() - self.last_bullet_adding_time >= self.reloading_speed and len(self.bullets) < self.magazine_capacity:
            self.last_bullet_adding_time = time()
            self.bullets.add(Bullet(self, self.game))

    def _reload_magazine(self):
        for _ in range(self.magazine_capacity):
            self.bullets.add(Bullet(self, self.game))

    def prepare_new_active_bullet(self) -> Bullet:
        bullet: Bullet = self.bullets.sprites()[0]
        self.bullets.remove(bullet)

        bullet.set_direction_x(self.last_side)
        bullet.set_bullet_speed_x(self.bullet_speed)
        bullet.set_bullet_speed_y(0)
        bullet.set_coord((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        bullet.start()

        return bullet
