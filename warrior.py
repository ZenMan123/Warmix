import pygame
from os import listdir
from json import load
from configurations import *
from camera import Camera
from typing import List, Dict, Tuple


class Warrior(pygame.sprite.Sprite):
    def __init__(self, warrior_name: str, camera: Camera, init_side: str = 'right'):
        super(Warrior, self).__init__()

        self.warrior_name = warrior_name
        self.current_directory = f'Warriors/{self.warrior_name}'
        self.last_side = init_side
        self.camera = camera
        self.game = None

        self._load_features_data()
        self.conditions = {
            'attack': {
                'status': False,
                'func': self._attack,
            },
            'jump': {
                'jumping_count': JUMPING_COUNT,
                'status': False,
                'func': self._jump,
                'just_finished': False,
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
            },
            'fall': {
                'func': self._fall,
                'status': False,
                'falling_speed': FALLING_ACCELERATION
            },
            'collect': {
                'func': self._collect,
                'status': False
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
        self.rect.x, self.rect.y = PART_OF_MAP_WIDTH, HEIGHT - self.rect.height - PART_OF_MAP_HEIGHT

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

    def _walk(self, collided_object=None):
        reverse = 1 if not collided_object else -1
        if self.last_side == 'left':
            self.rect.x -= WALKING_SPEED * reverse
        if self.last_side == 'right':
            self.rect.x += WALKING_SPEED * reverse

    def _run(self, collided_object=None):
        reverse = 1 if not collided_object else -1
        if self.last_side == 'left':
            self.rect.x -= RUNNING_SPEED * reverse
        if self.last_side == 'right':
            self.rect.x += RUNNING_SPEED * reverse

    def _fall(self, collided_object=None):
        falling_speed = self.conditions['fall']['falling_speed']

        if collided_object:
            self.rect.y = collided_object.rect.y - self.rect.height
            self.deactivate('fall', features_dict={'falling_speed': FALLING_ACCELERATION})
            self.reduce_health_from_falling(falling_speed)
        elif self.rect.y + falling_speed >= HEIGHT - self.rect.height - PART_OF_MAP_HEIGHT:
            self.rect.y = HEIGHT - self.rect.height - PART_OF_MAP_HEIGHT
            self.reduce_health_from_falling(falling_speed)
            self.deactivate('fall', features_dict={'falling_speed': FALLING_ACCELERATION})
        else:
            self.rect.y += falling_speed
            self.conditions['fall']['falling_speed'] += FALLING_ACCELERATION

    def _jump(self, collided_object: pygame.sprite.Sprite = None):
        jumping_count = self.conditions['jump']['jumping_count']
        if jumping_count <= -(JUMPING_COUNT + 1):
            self.deactivate('jump', features_dict={'jumping_count': JUMPING_COUNT,
                                                   'just_finished': True})
            return

        if collided_object:
            if collided_object.rect.y < self.rect.y:
                self.rect.y += round((jumping_count + 1) ** 2 * JUMPING_K)
                self.conditions['jump']['jumping_count'] = jumping_count = -1
                if jumping_count <= -(JUMPING_COUNT + 1):
                    self.deactivate('jump', features_dict={'jumping_count': JUMPING_COUNT,
                                                           'just_finished': True})
                    return
            else:
                self.deactivate('jump', features_dict={'jumping_count': JUMPING_COUNT,
                                                       'just_finished': True})
                self.rect.y = collided_object.rect.y - self.rect.height
                return

        sign = 1 if jumping_count >= 0 else -1
        self.rect.y -= round((jumping_count ** 2) * JUMPING_K) * sign
        self.conditions['jump']['jumping_count'] -= 1

    def _attack(self, collided_object=None):
        pass

    def _idle(self, collided_object=None):
        pass

    def _collect(self, collided_object:pygame.sprite.Sprite = None):
        if collided_object and collided_object.is_icon():
            if collided_object.get_icon_type() == 'apple':
                self.health = min(self.health + 20, self.data['health'] * 2)
            if collided_object.get_icon_type() == 'potion':
                self.power = min(self.power + 5, self.data['power'] * 2)
            if collided_object.get_icon_type() == 'power':
                self.power = min(self.power + 10, self.data['power'] * 2)
            if collided_object.get_icon_type() == 'shield':
                self.health = min(self.health + 50, self.data['health'] * 2)
            collided_object.kill()
        self.deactivate('collect')

    def reduce_health_from_falling(self, falling_speed):
        if falling_speed <= 70:
            return
        self.health -= (falling_speed - 50) // 2

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

    def deactivate(self, mode, direction=None, features_dict=None):
        if direction:
            self.conditions[mode]['directions'].remove(direction)
            if not self.conditions[mode]['directions']:
                self.conditions[mode]['status'] = False
            else:
                self.last_side = list(self.conditions[mode]['directions'])[0]
        else:
            self.conditions[mode]['status'] = False
        if features_dict:
            for a, b in features_dict.items():
                self.conditions[mode][a] = b

    def update(self) -> None:
        modes = list()
        for mode in self.conditions.keys():
            if self.conditions[mode]['status']:
                if mode == 'jump' and self.conditions['fall']['status']:
                    self.conditions['jump']['status'] = False
                    continue
                if mode == 'collect':
                    icons_res = pygame.sprite.spritecollide(self, self.game.map_icons_group, False)
                    if icons_res:
                        self.conditions[mode]['func'](collided_object=icons_res[0])
                if (mode == 'run' and self.check_for('walk')) or (mode != 'run'):
                    self.conditions[mode]['func']()
                    obstacle_res = pygame.sprite.spritecollide(self, self.game.map_obstacles_group, False)
                    if obstacle_res:
                        self.conditions[mode]['func'](collided_object=obstacle_res[0])
                    modes.append(mode)

        self.check_for_falling()
        self.conditions['jump']['just_finished'] = False

        mode = sorted(modes, key=lambda x: MODE_IMPORTANCE[x], reverse=True)[0]
        self._update_image(mode)
        self.camera.update(self)

    def check_for(self, *modes):
        return any(self.conditions[mode]['status'] for mode in modes)

    def check_for_falling(self):
        self.rect.y += 1
        if pygame.sprite.spritecollide(self, self.game.map_obstacles_group, False) or self.conditions['jump']['status']:
            self.rect.y -= 1
        else:
            self.rect.y -= 1
            if self.conditions['jump']['just_finished']:
                self.conditions['fall']['falling_speed'] = round(JUMPING_COUNT ** 2 * JUMPING_K)
            self.conditions['fall']['status'] = True

    def _update_image(self, mode: str) -> None:
        if mode == 'fall':
            mode = 'jump'
        self.mode_to_frame_number[self.last_side][mode] = (self.mode_to_frame_number[self.last_side][mode] + 1) % 7
        self.image = self.mode_to_images[self.last_side][mode][self.mode_to_frame_number[self.last_side][mode]]

    @staticmethod
    def _transform_warrior_image(image: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(image, (WARRIOR_WIDTH, WARRIOR_HEIGHT))

    def __str__(self):
        result = [f'<Warrior> {self.warrior_name}', f'Здоровье: {self.health}, Урон: {self.power}',
                  f'Позиция: {self.rect.x, self.rect.y}']
        return '\n'.join(result)
