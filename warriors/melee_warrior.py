from .base_warrior import BaseWarrior
from configurations.size_configurations import ANIMATIONS_COUNT, WARRIOR_WIDTH
from configurations.modes_configuration import LEFT, RIGHT
from services_for_game.camera import Camera
from game.game import Game

import pygame


class MeleeWarrior(BaseWarrior):
    def __init__(self, warrior_name: str, camera: Camera, game: Game, init_side: str = 'right'):
        super().__init__(warrior_name, camera, game, init_side)
        self.conditions['attack']['attack_count'] = -1

    def _attack(self) -> None:
        if self.conditions['attack']['attack_count'] == ANIMATIONS_COUNT - 1:
            self.deactivate('attack')
            self.conditions['attack']['attack_count'] = -1

            self.rect.y = self.rect.y - WARRIOR_WIDTH // 5 if LEFT else self.rect.y + WARRIOR_WIDTH // 5

            res = pygame.sprite.spritecollide(self, self.game.warriors, False)
            if res:
                for obj in res:
                    if obj == self:
                        continue
                    else:
                        obj.receive_damage(self.power)
                        break

            self.rect.y = self.rect.y + WARRIOR_WIDTH // 5 if LEFT else self.rect.y - WARRIOR_WIDTH // 5
        else:
            self.conditions['attack']['attack_count'] += 1






