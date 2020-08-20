from warriors.base_warrior import BaseWarrior
from weapons.bullet import Bullet
from services_for_game.camera import Camera
from typing import List


class PistolPirate(BaseWarrior):
    def __init__(self, warrior_name: str, camera: Camera, init_side: str = 'right'):
        super().__init__(warrior_name, camera, init_side)
        self.bullets: List[Bullet] = [Bullet()] * 6

    def _attack(self):
        if not self.bullets:
            return

        bullet = self.bullets.pop()
        bullet.set_coord(self.rect.topleft)
        bullet.set_direction(self.last_side)



