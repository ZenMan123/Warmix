from app.game.game import Game
from app.screen_drawers.base_warrior_info import BaseWarriorInfo
from app.screen_drawers.pistol_warrior_info import PistolWarriorInfo
from app.screen_drawers.drawer import Drawer
from app.warriors.pistol_pirate import PistolPirate
from app.warriors.melee_warrior import MeleeWarrior
from app.services_for_game.camera import Camera
from app.services_for_game.music import Music
import pygame
from app.configurations.size_configurations import SCREEN_SIZE, FPS, SIZE
from game_server.client import Client
import threading


class GetDataThread(threading.Thread):
    def __init__(self, warriors, client):
        self.warriors = warriors
        self.client = client

    def run(self):
        data = self.client.receive_data().split('%')
        print(data)


def update_main_warrior(warrior, drawer):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    warrior.activate('walk', direction='left')
                    warrior.modes_to_activate.append('wl')
                if event.key == pygame.K_d:
                    warrior.activate('walk', direction='right')
                    warrior.modes_to_activate.append('wr')
                if event.key == pygame.K_e:
                    warrior.activate('collect')
                    warrior.modes_to_activate.append('wc')
                if event.key == pygame.K_q:
                    warrior.activate('run')
                    warrior.modes_to_activate.append('ru')
                if event.key == pygame.K_SPACE:
                    warrior.activate('jump')
                    warrior.modes_to_activate.append('j')

            if event.type == pygame.MOUSEBUTTONDOWN:
                warrior.activate('attack')
                warrior.change_last_side(event.pos)
                warrior.modes_to_activate.append(f'a_{event.pos[0]}_{event.pos[1]}')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    warrior.deactivate('run')
                    warrior.modes_to_deactivate.append('ru')
                if event.key == pygame.K_a:
                    warrior.deactivate('walk', direction='left')
                    warrior.modes_to_deactivate.append('wl')
                if event.key == pygame.K_d:
                    warrior.deactivate('walk', direction='right')
                    warrior.modes_to_deactivate.append('wr')

        clock.tick(FPS)
        warrior.update()
        drawer.draw()


def main(warrior, drawer):
    update_main_warrior(warrior, drawer)


# client = Client('artem', 'artem')
# client.login()
# client.set_warrior_name('2')
#
# game = client.create_game()
# print('Created game:', game)
#
# client.participate(game)
#
# input("click enter to start game")
# client.start()
# participants = client.wait_for_game_start()
# print('Game started! Participants: ', participants)

screen = pygame.display.set_mode(SCREEN_SIZE)
camera = Camera()

Music().start()

game = Game(pygame.sprite.Group(), 1)

main_warrior = PistolPirate('artem', '2', camera, game)
main_warrior_info = PistolWarriorInfo(main_warrior)

drawer = Drawer(screen, game, camera, main_warrior, main_warrior_info)

main(main_warrior, drawer)
