from game.game import Game
from screen_drawers.base_warrior_info import BaseWarriorInfo
from screen_drawers.pistol_warrior_info import PistolWarriorInfo
from screen_drawers.drawer import Drawer
from warriors.pistol_pirate import PistolPirate
from warriors.melee_warrior import MeleeWarrior
from services_for_game.camera import Camera
from services_for_game.music import Music
import pygame
from configurations.size_configurations import SCREEN_SIZE, FPS, SIZE


def main(warrior, drawer, game):
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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    warrior.deactivate('run')
                if event.key == pygame.K_a:
                    warrior.deactivate('walk', direction='left')
                if event.key == pygame.K_d:
                    warrior.deactivate('walk', direction='right')

        for w in game.warriors:
            w.update()
        drawer.draw()
        clock.tick(FPS)


screen = pygame.display.set_mode(SCREEN_SIZE)
camera = Camera()

Music().start()

game = Game(pygame.sprite.Group(), 1)

second_warrior = PistolPirate('2', Camera(), game)
main_warrior = MeleeWarrior('1', camera, game)

main_warrior_info = BaseWarriorInfo(main_warrior)

drawer = Drawer(screen, game, camera, main_warrior, main_warrior_info)

main(main_warrior, drawer, game)
