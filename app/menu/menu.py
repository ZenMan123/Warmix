import pygame

from app.configurations.menu_configurations import PATH_TO_MENU, BACKGROUND_NAME, NET_GAME_BUTTON_NAME, \
    TRAINING_ROOM_BUTTON_NAME, SETTINGS_BUTTON_NAME, TURN_SOUND_EFFECTS_ON_BUTTON_NAME, \
    TURN_SOUND_EFFECTS_OFF_BUTTON_NAME, TURN_MUSIC_ON_BUTTON_NAME, TURN_MUSIC_OFF_BUTTON_NAME, BUTTON_BACK, \
    CONNECT_TO_THE_GAME, CREATE_GAME

from app.configurations.size_configurations import SCREEN_SIZE
from app.menu.button import Button, ChangingValueButton, InputValueButton
from abc import ABC, abstractmethod


class BaseMenu(ABC):
    def __init__(self, screen):
        self.background = pygame.transform.scale(pygame.image.load(f'{PATH_TO_MENU}/{BACKGROUND_NAME}'), SCREEN_SIZE)
        self.screen = screen
        self.set_buttons()

    @abstractmethod
    def set_buttons(self):
        pass

    @abstractmethod
    def run_menu(self):
        pass

    def update(self):
        self.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.blit(self.screen)
        pygame.display.flip()


class MainMenu(BaseMenu):
    def set_buttons(self):
        self.buttons = [
            Button(NET_GAME_BUTTON_NAME, 0, 'net_game'),
            Button(TRAINING_ROOM_BUTTON_NAME, 1, 'training'),
            Button(SETTINGS_BUTTON_NAME, 2, 'settings')
        ]

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button.process_aiming(event.pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        res = button.process_pressing(event.pos)
                        if res:
                            return res

                if event.type == pygame.QUIT:
                    return 'quit'
            self.update()


class SettingsMenu(BaseMenu):
    def __init__(self, screen, conditions):
        self.conditions = conditions
        super().__init__(screen)

    def set_buttons(self):
        self.buttons = [
            ChangingValueButton(0, music_on=TURN_MUSIC_OFF_BUTTON_NAME,
                                music_off=TURN_MUSIC_ON_BUTTON_NAME,
                                init_value=self.conditions['music']),
            ChangingValueButton(1, sound_effects_on=TURN_SOUND_EFFECTS_OFF_BUTTON_NAME,
                                sound_effects_off=TURN_SOUND_EFFECTS_ON_BUTTON_NAME,
                                init_value=self.conditions['sound_effects']),
            InputValueButton(2, 'Login', text=self.conditions['login']),
            InputValueButton(3, 'Warrior', text=self.conditions['warrior_name']),
            Button(BUTTON_BACK, 4, 'back')
        ]

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button.process_aiming(event.pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        res = button.process_pressing(event.pos)
                        if res:
                            if res.startswith('music_'):
                                self.conditions['music'] = res
                            if res.startswith('sound_effects_'):
                                self.conditions['sound_effects'] = res
                            if res == 'back':
                                return self.conditions
                if event.type == pygame.KEYDOWN:
                    for button in self.buttons:
                        try:
                            res = button.process_pressing_keyboard(event)
                            if res.startswith('Login:') and res.split('Login:')[1]:
                                self.conditions['login'] = res.split('Login:')[1]
                            if res.startswith('Warrior:') and res.split('Warrior:')[1]:
                                self.conditions['warrior_name'] = res.split('Warrior:')[1]
                        except:
                            continue

            self.update()


class NetGameMenu(BaseMenu):
    def __init__(self, *args):
        self.conditions = {}
        super().__init__(*args)

    def set_buttons(self):
        self.buttons = [
            Button(CONNECT_TO_THE_GAME, 0, 'connect'),
            InputValueButton(1, 'Game id'),
            Button(CREATE_GAME, 2, 'create'),
            Button(BUTTON_BACK, 3, 'back')
        ]

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button.process_aiming(event.pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        res: str = button.process_pressing(event.pos)
                        if res == 'connect':
                            return res, self.conditions['game_id']
                        if res:
                            return res

                if event.type == pygame.KEYDOWN:
                    for button in self.buttons:
                        try:
                            res = button.process_pressing_keyboard(event)
                            if res.startswith('Game id:'):
                                self.conditions['game_id'] = res.split('Game id:')[1]
                        except:
                            continue
            self.update()
