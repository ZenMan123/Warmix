import pygame
from configurations.size_configurations import INFO_SIZE


class BannerIcon:
    def __init__(self, path, coords):
        self.image = pygame.transform.scale(pygame.image.load(path), INFO_SIZE)
        self.coords = coords


class BannerText:
    def __init__(self, font: pygame.font.Font, string: str, color: tuple, coords):
        self.font = font
        self.string = string
        self.color = color
        self.coords = coords
        self.image = self.font.render(self.string, 1, self.color)

    def update_text(self, string):
        self.string = string
        self.image = self.font.render(str(self.string), 1, self.color)

    def update_color(self, color):
        self.color = color
        self.image = self.font.render(self.string, 1, self.color)