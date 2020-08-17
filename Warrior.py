import pygame
from os import listdir
from json import load
from configurations import *
from typing import List, Dict, Tuple


class Warrior(pygame.sprite.Sprite):
    def __init__(self, warrior_name: str, init_side: str = 'right'):
        super(Warrior, self).__init__()

        self.warrior_name = warrior_name
        self.current_directory = f'Warriors/{self.warrior_name}'
        self.last_side = init_side

        self._load_features_data()
        self.conditions = {
            'attack': {
                'status': False,
                'func': self._attack,
                'moves_left': ATTACK_COUNT
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

    def _update_image(self, mode: str, side: str) -> None:
        self.mode_to_frame_number[side][mode] = (self.mode_to_frame_number[side][mode] + 1) % 7
        self.image = self.mode_to_images[side][mode][self.mode_to_frame_number[side][mode]]

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

    def _update_coord_x(self, mode: str, side: str):
        self.last_side = side
        if side == 'left' and self.rect.x > 5:
            if mode == 'run':
                self.rect.x -= RUNNING_SPEED
            if mode == 'walk':
                self.rect.x -= WALKING_SPEED
        if side == 'right' and self.rect.x < WIDTH - 5 - WARRIOR_WIDTH:
            if mode == 'run':
                self.rect.x += RUNNING_SPEED
            if mode == 'walk':
                self.rect.x += WALKING_SPEED

    def _jump(self):
        jumping_count = self.conditions['jump']['jumping_count']

        if jumping_count == -(JUMPING_COUNT + 1):
            self.conditions['jump']['status'] = False
            self.conditions['jump']['jumping_count'] = JUMPING_COUNT
            return

        sign = 1 if jumping_count >= 0 else -1
        self.rect.y -= round((jumping_count ** 2) * JUMPING_K * sign)
        self.conditions['jump']['jumping_count'] -= 1

    def _attack(self):
        moves_left = self.conditions['attack']['moves_left']

        if moves_left <= 0:
            self.conditions['attack']['status'] = False
            self.conditions['attack']['moves_left'] = ATTACK_COUNT

        self.conditions['attack']['moves_left'] -= 1

    def update(self, mode: str, side: str) -> None:
        if mode in self.conditions.keys():
            if not self.conditions[mode]['status']:
                self.conditions[mode]['status'] = True
        for temp_mode in self.conditions.keys():
            if self.conditions[temp_mode]['status']:
                self.conditions[temp_mode]['func']()

        self._update_image(mode, side)
        self._update_coord_x(mode, side)

    @staticmethod
    def _transform_warrior_image(image: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(image, (WARRIOR_WIDTH, WARRIOR_HEIGHT))

    def __str__(self):
        result = [f'<Warrior> {self.warrior_name}', f'Здоровье: {self.health}, Урон: {self.power}',
                  f'Позиция: {self.rect.x, self.rect.y}']
        return '\n'.join(result)
