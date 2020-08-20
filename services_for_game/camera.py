import pygame
from configurations.size_configurations import SCREEN_WIDTH, SCREEN_HEIGHT


def camera_configure(camera, target_rect):
    delta_x, delta_y = target_rect[:2]
    w, h = camera[2:]
    delta_x, delta_y = SCREEN_WIDTH / 2 - delta_x - target_rect.width // 2, \
                       SCREEN_HEIGHT / 2 - delta_y - target_rect.height // 2

    delta_x = min(0, delta_x)
    delta_x = max(SCREEN_WIDTH - camera.width, delta_x)
    delta_y = max(SCREEN_HEIGHT - camera.height, delta_y)
    delta_y = min(0, delta_y)

    return pygame.Rect(delta_x, delta_y, w, h)


class Camera(object):
    def __init__(self, width, height, camera_func=camera_configure):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def get_delta(self):
        return self.state.topleft

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
