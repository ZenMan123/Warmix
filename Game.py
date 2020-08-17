import pygame
from configurations import SIZE


class Game:
    def __init__(self, path_to_map_image: str, warriors_first: pygame.sprite.Group,
                 warriors_second: pygame.sprite.Group, screen: pygame.Surface):

        self.path_to_map_image = path_to_map_image
        self.map_image: pygame.Surface = pygame.transform.scale(pygame.image.load(f'Maps/{self.path_to_map_image}'), SIZE)
        self.warriors_first = warriors_first
        self.warriors_second = warriors_second
        self.screen = screen

    def draw(self):
        self.screen.blit(self.map_image, (0, 0))
        self.warriors_first.draw(self.screen)
        self.warriors_second.draw(self.screen)
        pygame.display.flip()
