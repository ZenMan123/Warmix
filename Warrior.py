import pygame
from os import listdir
from json import load
from configurations import *
from typing import List, Dict, Tuple


class Warrior(pygame.sprite.Sprite):
    def __init__(self, warrior_name: str, camera, init_side: str = 'right'):
        super(Warrior, self).__init__()

        self.warrior_name = warrior_name
        self.current_directory = f'Warriors/{self.warrior_name}'
        self.last_side = init_side
        self.camera = camera

        self._load_features_data()
        self.conditions = {
            'attack': {
                'status': False,
                'func': self._attack,
            },
            'jump': {
                'jumping_count': JUMPING_COUNT,
                'status': False,
                'func': self._jump
            },
            'hurt': {
                'status': False,
                'func': None
            },
            'die': {
                'status': False,
                'func': None
            },
            'walk': {
                'directions': set(),
                'func': self._walk,
                'status': False
            },
            'run': {
                'directions': set(),
                'func': self._run,
                'status': False
            },
            'idle': {
                'func': self._idle,
                'status': True
            }

        }

        self.mode_to_images: Dict[str, Dict[str, List[pygame.Surface]]] = {
            'left': {
                'attack': list(),
                'die': list(),
                'hurt': list(),
                'idle': list(),
                'jump': list(),
                'run': list(),
                'walk': list(),
            },
            'right': {
                'attack': list(),
                'die': list(),
                'hurt': list(),
                'idle': list(),
                'jump': list(),
                'run': list(),
                'walk': list(),
            }
        }
        self.mode_to_frame_number: Dict[str, Dict[str, int]] = {
            'left': {
                'attack': 0,
                'die': 0,
                'hurt': 0,
                'idle': 0,
                'jump': 0,
                'run': 0,
                'walk': 0,
            },
            'right': {
                'attack': 0,
                'die': 0,
                'hurt': 0,
                'idle': 0,
                'jump': 0,
                'run': 0,
                'walk': 0,
            }
        }

        self._load_images()

        self.image: pygame.Surface = self.mode_to_images[init_side]['idle'][0]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, HEIGHT - self.rect.height

    def _load_features_data(self):
        with open(f'{self.current_directory}/features.json') as data:
            self.data = load(data)
        self.health = self.data["health"]
        self.power = self.data["power"]

    def _load_images(self):
        for side in ('left', 'right'):
            for mode in self.mode_to_images[side].keys():
                temp_directory = f'{self.current_directory}/photos/{mode}/{side}'
                loaded_images: List[pygame.Surface] = [
                    self._transform_warrior_image(pygame.image.load(f'{temp_directory}/{i}'))
                    for i in sorted(listdir(temp_directory))]
                self.mode_to_images[side][mode] = loaded_images

    def _walk(self):
        if self.last_side == 'left' and self.rect.x > WALKING_SPEED:
            self.rect.x -= WALKING_SPEED
        if self.last_side == 'right' and self.rect.x < WIDTH - WARRIOR_WIDTH - WALKING_SPEED:
            self.rect.x += WALKING_SPEED

    def _run(self):
        if self.last_side == 'left' and self.rect.x > RUNNING_SPEED:
            self.rect.x -= RUNNING_SPEED
        if self.last_side == 'right' and self.rect.x < WIDTH - WARRIOR_WIDTH - RUNNING_SPEED:
            self.rect.x += RUNNING_SPEED

    def _jump(self):
        jumping_count = self.conditions['jump']['jumping_count']

        if jumping_count == -(JUMPING_COUNT + 1):
            self.deactivate('jump')
            self.conditions['jump']['jumping_count'] = JUMPING_COUNT
            return

        sign = 1 if jumping_count >= 0 else -1
        self.rect.y -= round((jumping_count ** 2) * JUMPING_K * sign)
        self.conditions['jump']['jumping_count'] -= 1

    def _attack(self):
        pass

    def _idle(self):
        pass

    def activate(self, mode, direction=None):
        self.conditions[mode]['status'] = True
        if direction:
            self.conditions[mode]['directions'].add(direction)

    def change_last_side(self, pos):
        delta_x, delta_y = self.camera.get_delta()
        if pos[0] - delta_x <= self.rect.x + WARRIOR_WIDTH / 2:
            self.last_side = 'left'
        else:
            self.last_side = 'right'

    def deactivate(self, mode, direction=None):
        if direction:
            self.conditions[mode]['directions'].remove(direction)
            if not self.conditions[mode]['directions']:
                self.conditions[mode]['status'] = False
            else:
                self.last_side = list(self.conditions[mode]['directions'])[0]
        else:
            self.conditions[mode]['status'] = False

    def update(self) -> None:
        modes = list()
        for mode in self.conditions.keys():
            if self.conditions[mode]['status']:
                if (mode == 'run' and self.check_for('walk')) or (mode != 'run'):
                    self.conditions[mode]['func']()
                    modes.append(mode)

        mode = sorted(modes, key=lambda x: MODE_IMPORTANCE[x], reverse=True)[0]
        self._update_image(mode)
        self.camera.update(self)

    def check_for(self, *modes):
        return any(self.conditions[mode]['status'] for mode in modes)

    def _update_image(self, mode: str) -> None:
        self.mode_to_frame_number[self.last_side][mode] = (self.mode_to_frame_number[self.last_side][mode] + 1) % 7
        self.image = self.mode_to_images[self.last_side][mode][self.mode_to_frame_number[self.last_side][mode]]

    @staticmethod
    def _transform_warrior_image(image: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(image, (WARRIOR_WIDTH, WARRIOR_HEIGHT))

    def __str__(self):
        result = [f'<Warrior> {self.warrior_name}', f'Здоровье: {self.health}, Урон: {self.power}',
                  f'Позиция: {self.rect.x, self.rect.y}']
        return '\n'.join(result)
