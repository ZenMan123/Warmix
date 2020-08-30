import json
from os import listdir
from typing import Dict, List

import pygame
from app.configurations.size_configurations import PART_OF_MAP_HEIGHT, PART_OF_MAP_WIDTH, HEIGHT, ANIMATIONS_COUNT, \
    WARRIOR_SIZE
from ..configurations.files_configurations import PATH_TO_WARRIOR
from ..configurations.modes_configuration import DIRECTIONS, MODES, RIGHT, LEFT
from ..game.game import Game


class AbstractWarrior(pygame.sprite.Sprite):
    def __init__(self, login: str, warrior_name: str, game: Game):
        super().__init__()

        self.login = login  # Уникальный идентификатор игрока
        self.warrior_name = warrior_name
        self.game = game

        # Загружаем информацию из json файлов о персонаже, а также анимации различных состояний
        self.load_features_data()
        self.set_mode_to_images_dict()
        self.set_mode_to_frame_number_dict()

        # Задаём координаты и активное изображение
        self.last_side = RIGHT
        self.image: pygame.Surface = self.mode_to_images[self.last_side]['idle'][0]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = PART_OF_MAP_WIDTH, HEIGHT - self.rect.height - PART_OF_MAP_HEIGHT

    def _update_image(self, mode: str) -> int:
        """Обновляет картинку по заданному состоянию
        :param mode: Состояние
        :type mode: str

        :return Номер кадра в анимации
        :rtype: int
        """

        if mode == 'fall':  # Картинка для падения и прыжка одна и та же
            mode = 'jump'

        # Увеличиваем номер картинки в анимации и обновляем изображение
        self.mode_to_frame_number[self.last_side][mode] = (self.mode_to_frame_number[self.last_side][
                                                               mode] + 1) % ANIMATIONS_COUNT
        self.image = self.mode_to_images[self.last_side][mode][self.mode_to_frame_number[self.last_side][mode]]
        return self.mode_to_frame_number[self.last_side][mode]

    def load_features_data(self):
        with open(f'{PATH_TO_WARRIOR}/{self.warrior_name}/features.json') as data:
            self.data = json.load(data)

        self.health = self.MAX_HEALTH = self.data["health"]
        self.power = self.MAX_POWER = self.data["power"]
        self.WALKING_SPEED = self.data["walking_speed"]
        self.RUNNING_SPEED = self.data["running_speed"]
        self.JUMPING_COUNT = self.data["jumping_count"]
        self.JUMPING_K = self.data["jumping_k"]
        self.FALLING_ACCELERATION = self.data["falling_acceleration"]

    def _near_with_items(self) -> pygame.sprite.Group:
        """Возвращает список задетых предметов
        :return Список спрайтов
        :rtype pygame.sprite.Group
        """

        return pygame.sprite.spritecollide(self, self.game.map_icons_group, False)

    def change_last_side(self, pos) -> None:
        """Меняет сторону, в которую будет смотреть персонаж в зависимости от направления атаки
        :param pos: Позиция клика мышки
        :return: None
        """

        delta_x, delta_y = self.camera.get_delta()  # Получаем сдвиг камеры для правильной обработки координат
        self.last_side = LEFT if pos[0] - delta_x <= self.rect.x + self.rect.width / 2 else RIGHT

    def set_mode_to_images_dict(self):
        self.mode_to_images: Dict[str, Dict[str, List[pygame.Surface]]] = {}
        for i in DIRECTIONS:
            self.mode_to_images[i] = {}
            for mode in MODES:
                self.mode_to_images[i][mode] = list()

        for side in DIRECTIONS:
            for mode in self.mode_to_images[side].keys():
                try:
                    path_to_images = f'{PATH_TO_WARRIOR}/{self.warrior_name}/photos/{mode}/{side}'
                    loaded_images: List[pygame.Surface] = [
                        self.transform_warrior_image(pygame.image.load(f'{path_to_images}/{i}'))
                        for i in sorted(listdir(path_to_images))
                    ]
                    self.mode_to_images[side][mode] = loaded_images
                except FileNotFoundError:
                    continue

    def set_mode_to_frame_number_dict(self):
        self.mode_to_frame_number: Dict[str, Dict[str, int]] = {}
        for i in DIRECTIONS:
            self.mode_to_frame_number[i] = {}
            for mode in MODES:
                self.mode_to_frame_number[i][mode] = 0

    @staticmethod
    def transform_warrior_image(image: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(image, WARRIOR_SIZE)

    def __str__(self) -> str:
        result = [f'<Warrior> {self.warrior_name}', f'Здоровье: {self.health}, Урон: {self.power}',
                  f'Позиция: {self.rect.x, self.rect.y}']
        return '\n'.join(result)
