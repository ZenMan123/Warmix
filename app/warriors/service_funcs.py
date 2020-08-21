from app.configurations.files_configurations import *
from app.configurations.modes_configuration import *
from app.configurations.size_configurations import WARRIOR_SIZE

import pygame

from typing import List, Dict

from json import load
from os import listdir


def load_features_data(obj):
    with open(get_warrior_features_path(obj.warrior_name)) as data:
        obj.data = load(data)
    obj.health = obj.MAX_HEALTH = obj.data["health"]
    obj.power = obj.MAX_POWER = obj.data["power"]
    obj.WALKING_SPEED = obj.data["walking_speed"]
    obj.RUNNING_SPEED = obj.data["running_speed"]
    obj.JUMPING_COUNT = obj.data["jumping_count"]
    obj.JUMPING_K = obj.data["jumping_k"]
    obj.FALLING_ACCELERATION = obj.data["falling_acceleration"]


def set_mode_to_images_dict(obj):
    obj.mode_to_images: Dict[str, Dict[str, List[pygame.Surface]]] = {}
    for i in DIRECTIONS:
        obj.mode_to_images[i] = {}
        for mode in MODES:
            obj.mode_to_images[i][mode] = list()

    for side in DIRECTIONS:
        for mode in obj.mode_to_images[side].keys():
            try:
                path_to_images = get_warrior_photos_path(obj.warrior_name, side, mode)
                loaded_images: List[pygame.Surface] = [
                    transform_warrior_image(pygame.image.load(f'{path_to_images}/{i}'))
                    for i in sorted(listdir(path_to_images))]
                obj.mode_to_images[side][mode] = loaded_images
            except FileNotFoundError:
                continue


def set_mode_to_frame_number_dict(obj):
    obj.mode_to_frame_number: Dict[str, Dict[str, int]] = {}
    for i in DIRECTIONS:
        obj.mode_to_frame_number[i] = {}
        for mode in MODES:
            obj.mode_to_frame_number[i][mode] = 0


def transform_warrior_image(image: pygame.Surface) -> pygame.Surface:
    """Принимаем в качестве аргумента картинку и возвращает её с измененным размером
    :param image: Картинка
    :type image: pygame.Surface

    :return image
    :rtype pygame.Surface
        """

    return pygame.transform.scale(image, WARRIOR_SIZE)
