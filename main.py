from Game import Game
from Warrior import Warrior
import pygame
from configurations import SIZE, FPS

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
    if keys[pygame.K_LEFT] and keys[pygame.K_LSHIFT]:
        w1.update('run', 'left')
    elif keys[pygame.K_RIGHT] and keys[pygame.K_LSHIFT]:
        w1.update('run', 'right')
    elif keys[pygame.K_LEFT]:
        w1.update('walk', 'left')
    elif keys[pygame.K_RIGHT]:
        w1.update('walk', 'right')
    else:
        w1.update('idle', w1.last_side)

    game.draw()
    clock.tick(FPS)



