import pygame

from app.dynamic_weapons.bullet import Bullet
from app.warriors.abstract_warrior import AbstractWarrior


class NetWarrior(AbstractWarrior):
    def __init__(self, login, warrior_name, game, music, func_when_attack):
        super(AbstractWarrior, self).__init__(login, warrior_name, game)
        self.music = music
        self.func_when_attack = func_when_attack

    def update(self, last_side, mode, frame_number, pos):
        self.func_when_attack()
        self.last_side = last_side
        self._update_image(mode, frame_number)
        self.rect.topleft = int(pos.split('_')[0]), int(pos.split('_')[1])

    def _update_image(self, mode: str, frame_number) -> int:
        self.mode_to_frame_number[mode] = frame_number
        super()._update_image(mode)


def shooting_attack(obj):
    obj.music.play_bullet_shooting_sound()

    bullet = Bullet(obj, obj.game, obj.damage, obj.distance)
    bullet.set_direction_x(self.last_side)
    bullet.set_bullet_speed_x(self.bullet_speed)
    bullet.set_bullet_speed_y(0)
    bullet.set_coord((self.rect.x if self.last_side == LEFT else self.rect.x + self.rect.width,
                      self.rect.y + self.rect.height // 2))
    bullet.start()






