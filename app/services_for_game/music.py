import pygame
from app.configurations.files_configurations import COLLECTING_SOUND_NAME, HURTING_SOUND_NAME, JUMPING_SOUND_NAME, \
    MUSIC_BACKGROUND_NAME, ATTACKING_SOUND_NAME, PATH_TO_MUSIC, BULLET_SHOOTING_NAME, EMPTY_MAGAZINE_NAME, \
    APPLE_EATING_NAME, COLLECTING_SWORD_NAME

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()


class Music:
    def __init__(self, music=True, sound_effects=True):
        self.music = music
        self.sound_effects = sound_effects

        pygame.mixer.music.load(f'{PATH_TO_MUSIC}/{MUSIC_BACKGROUND_NAME}')
        pygame.mixer.music.set_volume(0.3)
        self.hurting_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{HURTING_SOUND_NAME}')
        self.collecting_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{COLLECTING_SOUND_NAME}')
        self.jumping_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{JUMPING_SOUND_NAME}')
        self.attacking_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{ATTACKING_SOUND_NAME}')
        self.bullet_shooting_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{BULLET_SHOOTING_NAME}')
        self.empty_magazine_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{EMPTY_MAGAZINE_NAME}')
        self.apple_eating_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{APPLE_EATING_NAME}')
        self.collecting_sword_sound = pygame.mixer.Sound(f'{PATH_TO_MUSIC}/{COLLECTING_SWORD_NAME}')

    def start(self):
        if self.music:
            pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.pause()

    def play_hurting_sound(self):
        if self.sound_effects:
            self.hurting_sound.play()

    def play_collecting_sound(self):
        if self.sound_effects:
            self.collecting_sound.play()

    def play_jumping_sound(self):
        if self.sound_effects:
            self.jumping_sound.play()

    def play_attacking_sound(self):
        if self.sound_effects:
            self.attacking_sound.play()

    def play_bullet_shooting_sound(self):
        if self.sound_effects:
            self.bullet_shooting_sound.play()

    def play_empty_magazine_sound(self):
        if self.sound_effects:
            self.empty_magazine_sound.play()

    def play_apple_eating_sound(self):
        if self.sound_effects:
            self.apple_eating_sound.play()

    def play_collecting_sword(self):
        if self.sound_effects:
            self.collecting_sword_sound.play()
