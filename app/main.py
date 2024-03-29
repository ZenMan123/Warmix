import json
from time import sleep

from app.configurations.warriors_configuration import WARRIOR_NAME_TO_TYPE
from app.game.game import Game
from app.menu.menu import MainMenu, SettingsMenu, NetGameMenu
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
                game.music.stop()
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

        clock.tick(FPS)
        game.update_objects()
        drawer.draw()


def run_game(screen, level, user_warrior_name, user_login, music, client=None, game_id=None):
    game = Game({}, level, music)

    if client:
        if not game_id:
            game_id = client.create_game()
            client.participate(game_id)
            waiting_screen(screen)
            participants = client.start_game()
        else:
            client.participate(game_id)
            participants = client.wait_for_game_start()
        print(participants)

        for i in participants:
            login, warrior_name = i.split('-')
            if login != user_login:
                WARRIOR_NAME_TO_TYPE[warrior_name](login, warrior_name, Camera(), game, Music(), real=False)

        get_data_thread = GetDataThread(game, client)
        get_data_thread.start()

    camera = Camera()

    main_warrior = WARRIOR_NAME_TO_TYPE[user_warrior_name](user_login, user_warrior_name, camera, game, music, client=client)
    print(main_warrior.login)
    drawer = Drawer(screen, game, camera, main_warrior)
    music.start()
    main_game_cycle(main_warrior, game, drawer)


def waiting_screen(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 36)
    screen.blit(font.render('Click any key to start game', 1, (255, 0, 0)), (200, 200))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False


def run_menu():
    menu = MainMenu(screen)
    settings = SettingsMenu(screen, load_user_settings_conditions())
    net_game = NetGameMenu(screen)

    while True:
        conditions = load_user_settings_conditions()
        music = True if conditions['music'] == 'music_on' else False
        sound_effects = True if conditions['sound_effects'] == 'sound_effects_on' else False

        res = menu.run_menu()
        if res == 'training':
            run_game(screen, 1, conditions['warrior_name'], conditions['login'], Music(music, sound_effects))
        if res == 'settings':
            conditions = settings.run_menu()
            save_user_settings_conditions(conditions)
        if res == 'net_game':
            res = net_game.run_menu()
            if res == 'create':
                run_game(screen, 1, conditions['warrior_name'], conditions['login'],
                         Music(music, sound_effects), Client(conditions['login'], conditions['warrior_name']))
            if res[0] == 'connect':
                run_game(screen, 1, conditions['warrior_name'], conditions['login'], Music(music, sound_effects),
                         Client(conditions['login'], conditions['warrior_name']), res[1])

        if res == 'quit':
            break


def save_user_settings_conditions(conditions):
    with open('settings.json', 'w') as file:
        json.dump(conditions, file)


def load_user_settings_conditions():
    with open('settings.json') as file:
        return json.load(file)


screen = pygame.display.set_mode(SCREEN_SIZE)
run_menu()
