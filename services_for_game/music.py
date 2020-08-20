import pygame
from configurations.files_configurations import COLLECTING_SOUND_NAME, HURTING_SOUND_NAME, JUMPING_SOUND_NAME, \
    MUSIC_BACKGROUND_NAME, ATTACKING_SOUND_NAME, PATH_TO_MUSIC


class Music:
    def __init__(self):
        pygame.mixer.music.load(f'{PATH_TO_MUSIC}/{MUSIC_BACKGROUND_NAME}')
        pygame.mixer.music.set_volume(0.3)
        self.hurting_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{HURTING_SOUND_NAME}')
        self.collecting_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{COLLECTING_SOUND_NAME}')
        self.jumping_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{JUMPING_SOUND_NAME}')
        self.attacking_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{ATTACKING_SOUND_NAME}')

    def start(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.pause()

    def play_hurting_sound(self):
        self.hurting_sound.play()

    def play_collecting_sound(self):
        self.collecting_sound.play()

    def play_jumping_sound(self):
        self.jumping_sound.play()

    def play_attacking_sound(self):
        self.attacking_sound.play()
