from game.game import Game
from warriors.melee_warrior import MeleeWarrior
from services_for_game.camera import Camera
import pygame
from configurations.size_configurations import SCREEN_SIZE, FPS, SIZE


def main(warrior, game):
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    warrior.activate('walk', direction='left')
                if event.key == pygame.K_d:
                    warrior.activate('walk', direction='right')
                if event.key == pygame.K_e:
                    warrior.activate('collect')
                if event.key == pygame.K_q:
                    warrior.activate('run')
                if event.key == pygame.K_SPACE:
                    warrior.activate('jump')

            if event.type == pygame.MOUSEBUTTONDOWN:
                warrior.activate('attack')
                warrior.change_last_side(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                warrior.deactivate('attack')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    warrior.deactivate('run')
                if event.key == pygame.K_a:
                    warrior.deactivate('walk', direction='left')
                if event.key == pygame.K_d:
                    warrior.deactivate('walk', direction='right')

        warrior.update()
        game.draw()
        clock.tick(FPS)


screen = pygame.display.set_mode(SCREEN_SIZE)
camera = Camera(*SIZE)

warrior = MeleeWarrior('2', camera)
game = Game(warrior, pygame.sprite.Group(), camera, screen, 1)

main(warrior, game)



