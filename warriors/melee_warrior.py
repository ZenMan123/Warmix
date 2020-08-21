from .base_warrior import BaseWarrior
from configurations.size_configurations import ANIMATIONS_COUNT
from services_for_game.camera import Camera
from game.game import Game


class MeleeWarrior(BaseWarrior):
    def __init__(self, warrior_name: str, camera: Camera, game: Game, init_side: str = 'right'):
        super().__init__(warrior_name, camera, game, init_side)
        self.conditions['attack']['attack_count'] = -1

    def _attack(self) -> None:
        if self.conditions['attack']['attack_count'] == ANIMATIONS_COUNT - 1:
            self.deactivate('attack')
            self.conditions['attack']['attack_count'] = -1
        else:
            self.conditions['attack']['attack_count'] += 1



