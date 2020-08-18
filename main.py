from game import Game
from warrior import Warrior
from camera import Camera
import pygame
from configurations import SCREEN_SIZE, FPS, SIZE
from pprint import pprint


screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
camera = Camera(*SIZE)

warriors1 = pygame.sprite.Group()
w1 = Warrior('1', camera)
warriors1.add(w1)


game = Game(warriors1, pygame.sprite.Group(), camera, screen, 1)
game.draw()

w1.set_textures(game.map_obstacles_group)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                w1.activate('walk', 'left')
                w1.last_side = 'left'
            if event.key == pygame.K_d:
                w1.activate('walk', 'right')
                w1.last_side = 'right'
            if event.key == pygame.K_LSHIFT:
                w1.activate('run')
            if event.key == pygame.K_SPACE:
                w1.activate('jump')

        if event.type == pygame.MOUSEBUTTONDOWN:
            w1.activate('attack')
            w1.change_last_side(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            w1.deactivate('attack')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                w1.deactivate('run')
            if event.key == pygame.K_a:
                w1.deactivate('walk', 'left')
            if event.key == pygame.K_d:
                w1.deactivate('walk', 'right')

    w1.update()
    game.draw()
    clock.tick(FPS)
