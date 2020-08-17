import pygame
from os import listdir
from json import load
from configurations import WARRIOR_WIDTH, WIDTH, HEIGHT, WARRIOR_HEIGHT
from typing import List, Dict, Tuple


class Warrior(pygame.sprite.Sprite):
    def __init__(self, warrior_name: str, init_side: str = 'right'):
        super(Warrior, self).__init__()

        self.warrior_name = warrior_name
        self.current_directory = f'Warriors/{self.warrior_name}'
        self.last_side = init_side

        self._load_features_data()

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

    def _update_coord(self, mode: str, side: str):
        self.last_side = side
        if side == 'left' and self.rect.x > 5:
            if mode == 'run':
                self.rect.x -= 5
            if mode == 'walk':
                self.rect.x -= 2
        if side == 'right' and self.rect.x < WIDTH - 5 - WARRIOR_WIDTH:
            if mode == 'run':
                self.rect.x += 5
            if mode == 'walk':
                self.rect.x += 2

    def update(self, mode: str, side: str) -> None:
        self._update_image(mode, side)
        self._update_coord(mode, side)

    @staticmethod
    def _transform_warrior_image(image: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(image, (WARRIOR_WIDTH, WARRIOR_HEIGHT))

    def __str__(self):
        result = [f'<Warrior> {self.warrior_name}', f'Здоровье: {self.health}, Урон: {self.power}',
                  f'Позиция: {self.position}']
        return '\n'.join(result)
