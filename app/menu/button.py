from time import time

from app.configurations.menu_configurations import PATH_TO_MENU, BUTTON_SIZE, \
    TOP_BUTTON_POSITION, REVERSE_IMAGE_SUFFIX, DELTA_Y, TURN_MUSIC_OFF_BUTTON_NAME, TURN_MUSIC_ON_BUTTON_NAME, \
    TURN_SOUND_EFFECTS_OFF_BUTTON_NAME, TURN_SOUND_EFFECTS_ON_BUTTON_NAME, EMPTY_BUTTON_NAME
import pygame


def check_if_pos_inside(pos, button_position):
    return button_position[0] <= pos[0] <= button_position[0] + BUTTON_SIZE[0] and \
           button_position[1] <= pos[1] <= button_position[1] + BUTTON_SIZE[1]


class Button:
    def __init__(self, path_to_image, number_in_col, value):
        self.value = value
        self.normal_image = pygame.transform.scale(pygame.image.load(f'{PATH_TO_MENU}/{path_to_image}'), BUTTON_SIZE)
        self.reversed_image = pygame.transform.scale(
            pygame.image.load(f'{PATH_TO_MENU}/{path_to_image[:-4] + REVERSE_IMAGE_SUFFIX + ".png"}'), BUTTON_SIZE)

        self.image = self.normal_image
        self.position = TOP_BUTTON_POSITION[0], TOP_BUTTON_POSITION[1] + number_in_col * DELTA_Y

    def process_pressing(self, pos):
        if check_if_pos_inside(pos, self.position):
            return self.value

    def process_aiming(self, pos):
        self.image = self.reversed_image if check_if_pos_inside(pos, self.position) else self.normal_image

    def blit(self, screen):
        screen.blit(self.image, self.position)


class ChangingValueButton:
    def __init__(self, number_in_col, init_value='', **values_to_paths):
        self.images = {}
        for value, path in values_to_paths.items():
            self.images[value] = {}
            self.images[value]['normal'] = pygame.transform.scale(pygame.image.load(f'{PATH_TO_MENU}/{path}'),
                                                                  BUTTON_SIZE)
            self.images[value]['reversed'] = pygame.transform.scale(
                pygame.image.load(f'{PATH_TO_MENU}/{path[:-4] + REVERSE_IMAGE_SUFFIX + ".png"}'), BUTTON_SIZE)

        self.values = [
            value for value, path in values_to_paths.items()
        ]
        if init_value:
            self.current_index = self.values.index(init_value)
        else:
            self.current_index = 0

        self.value = self.values[self.current_index]
        print(self.value)
        self.image = self.images[self.value]['normal']
        self.position = TOP_BUTTON_POSITION[0], TOP_BUTTON_POSITION[1] + number_in_col * DELTA_Y

    def process_pressing(self, pos):
        if check_if_pos_inside(pos, self.position):
            self.current_index = (self.current_index + 1) % len(self.images)
            self.value = self.values[self.current_index]
            self.image = self.images[self.value]['normal']
            return self.value

    def process_aiming(self, pos):
        self.image = self.images[self.value]['reversed'] if check_if_pos_inside(pos, self.position) \
            else self.images[self.value]['normal']

    def blit(self, screen):
        screen.blit(self.image, self.position)


class InputValueButton:
    def __init__(self, number_in_col, param, text=''):
        self.font = pygame.font.Font(None, 30)
        self.position = TOP_BUTTON_POSITION[0], TOP_BUTTON_POSITION[1] + number_in_col * DELTA_Y
        self.image = pygame.transform.scale(pygame.image.load(f"{PATH_TO_MENU}/{EMPTY_BUTTON_NAME}"), BUTTON_SIZE)
        self.active = False
        self.param = f'{param}:'
        self.text = self.param + text
        self.text_surface = self.font.render(self.text, 1, (255, 255, 255))

    def process_pressing(self, pos):
        self.active = check_if_pos_inside(pos, self.position)

    def process_pressing_keyboard(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE and self.text and len(self.text) > len(self.param):
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.text_surface = self.font.render(self.text, 1, (255, 255, 255))
            return self.text

    def process_aiming(self, pos):
        pass

    def blit(self, screen):
        screen.blit(self.image, self.position)
        screen.blit(self.text_surface, (self.position[0] + 10, self.position[1] + BUTTON_SIZE[1] // 2 - 8))


