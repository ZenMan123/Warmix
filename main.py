from Game import Game
from Warrior import Warrior
import pygame
from configurations import SIZE, FPS


def catch_events(keys, pressed, pos):
    if pressed[0] or w1.conditions['attack']['status']:
        if pressed[0]:
            w1.last_side = 'left' if pos[0] < w1.rect.x + w1.rect.width // 2 else 'right'
        w1.update('attack', w1.last_side)
        return

    if keys[pygame.K_SPACE] and not w1.conditions['jump']['status']:
        w1.update('jump', w1.last_side)
    if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
        w1.update('run', 'left')
    elif keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
        w1.update('run', 'right')
    elif keys[pygame.K_a]:
        w1.update('walk', 'left')
    elif keys[pygame.K_d]:
        w1.update('walk', 'right')
    else:
        w1.update('idle', w1.last_side)


screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

warriors1 = pygame.sprite.Group()
w1 = Warrior('1')
warriors1.add(w1)

game = Game('base.png', warriors1, pygame.sprite.Group(), screen)
game.draw()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()

    catch_events(keys, pressed, pos)

    game.draw()
    clock.tick(FPS)



