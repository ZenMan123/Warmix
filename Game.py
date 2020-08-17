import pygame
from configurations import AMOUNT_OF_PARTS_IN_ROW, AMOUNT_OF_PARTS_IN_COL, BACKGROUND_NAME
from Map import MapPart
from Camera import Camera


class Game:
    def __init__(self, warriors_first: pygame.sprite.Group,
                 warriors_second: pygame.sprite.Group, camera: Camera, screen: pygame.Surface):

        self.map_image_group = pygame.sprite.Group()
        for x in range(AMOUNT_OF_PARTS_IN_ROW):
            for y in range(AMOUNT_OF_PARTS_IN_COL):
                map_image = MapPart(BACKGROUND_NAME, x, y)
                self.map_image_group.add(map_image)

        self.warriors_first = warriors_first
        self.warriors_second = warriors_second
        self.screen = screen
        self.camera = camera

    def draw(self):
        self.screen.fill((255, 255, 255))
        for map_image in self.map_image_group:
            self.screen.blit(map_image.image, self.camera.apply(map_image))
        for warrior_first in self.warriors_first:
            self.screen.blit(warrior_first.image, self.camera.apply(warrior_first))
        self.warriors_second.draw(self.screen)
        pygame.display.flip()
