import json

from app.configurations.warriors_configuration import WARRIOR_NAME_TO_TYPE
from app.game.game import Game
from app.menu.menu import MainMenu, SettingsMenu
from app.screen_drawers.drawer import Drawer

from app.services_for_game.camera import Camera
from app.services_for_game.music import Music
from app.services_for_game.get_net_game_data import GetDataThread

from game_server.client import Client

from app.configurations.size_configurations import SCREEN_SIZE, FPS, SIZE

import pygame


def main_game_cycle(warrior, game, drawer):
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
                    warrior.modes_to_activate.append('c')
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
        game.update_objects()
        drawer.draw()


def run_game(screen, level, warrior_name, login, music, client=None):
    game = Game({}, level, music)

    if client:
        game_id = client.create_game()
        client.participate(game_id)
        participants = client.wait_for_game_start()

        for i in participants:
            login, warrior_name = i.split('-')
            WARRIOR_NAME_TO_TYPE[warrior_name](login, warrior_name, Camera(), game)

        get_data_thread = GetDataThread(game, client)
        get_data_thread.start()

    camera = Camera()

    main_warrior = WARRIOR_NAME_TO_TYPE[warrior_name](login, warrior_name, camera, game, music, client=client)
    drawer = Drawer(screen, game, camera, main_warrior)
    music.start()

    main_game_cycle(main_warrior, game, drawer)


def run_menu():
    menu = MainMenu(screen)
    settings = SettingsMenu(screen, load_user_settings_conditions())
    while True:
        res = menu.run_menu()
        if res == 'training':
            conditions = load_user_settings_conditions()
            music = True if conditions['music'] == 'music_on' else False
            sound_effects = True if conditions['sound_effects'] == 'sound_effects_on' else False
            run_game(screen, 1, conditions['warrior_name'], conditions['login'], Music(music, sound_effects))
        if res == 'settings':
            conditions = settings.run_menu()
            save_user_settings_conditions(conditions)


def save_user_settings_conditions(conditions):
    with open('settings.json', 'w') as file:
        json.dump(conditions, file)


def load_user_settings_conditions():
    with open('settings.json') as file:
        return json.load(file)


screen = pygame.display.set_mode(SCREEN_SIZE)
run_menu()

