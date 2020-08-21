import pygame
from configurations.files_configurations import COLLECTING_SOUND_NAME, HURTING_SOUND_NAME, JUMPING_SOUND_NAME, \
    MUSIC_BACKGROUND_NAME, ATTACKING_SOUND_NAME, PATH_TO_MUSIC, BULLET_SHOOTING_NAME, EMPTY_MAGAZINE_NAME, \
    APPLE_EATING_NAME, COLLECTING_SWORD_NAME

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()


class Music:
    pygame.mixer.music.load(f'{PATH_TO_MUSIC}/{MUSIC_BACKGROUND_NAME}')
    pygame.mixer.music.set_volume(0.3)
    hurting_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{HURTING_SOUND_NAME}')
    collecting_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{COLLECTING_SOUND_NAME}')
    jumping_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{JUMPING_SOUND_NAME}')
    attacking_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{ATTACKING_SOUND_NAME}')
    bullet_shooting_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{BULLET_SHOOTING_NAME}')
    empty_magazine_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{EMPTY_MAGAZINE_NAME}')
    apple_eating_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{APPLE_EATING_NAME}')
    collecting_sword_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{COLLECTING_SWORD_NAME}')

    @staticmethod
    def start():
        pygame.mixer.music.play(-1)

    @staticmethod
    def stop():
        pygame.mixer.music.pause()

    @staticmethod
    def play_hurting_sound():
        Music.hurting_sound.play()

    @staticmethod
    def play_collecting_sound():
        Music.collecting_sound.play()

    @staticmethod
    def play_jumping_sound():
        Music.jumping_sound.play()

    @staticmethod
    def play_attacking_sound():
        Music.attacking_sound.play()

    @staticmethod
    def play_bullet_shooting_sound():
        Music.bullet_shooting_sound.play()

    @staticmethod
    def play_empty_magazine_sound():
        Music.empty_magazine_sound.play()

    @staticmethod
    def play_apple_eating_sound():
        Music.apple_eating_sound.play()

    @staticmethod
    def play_collecting_sword():
        Music.collecting_sword_sound.play()
