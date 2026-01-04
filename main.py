import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0

updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()
Asteroid.containers = (updatable, drawable, asteroids)
AsteroidField.containers = (updatable)
Player.containers = (updatable, drawable)
Shot.containers = (updatable, drawable, shots)
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
asteroidfield = AsteroidField()

while True:
    log_state()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill("black")
    updatable.update(dt)
    for a in asteroids:
        if a.collideswith(player):
            log_event("player_hit")
            print("Game over!")
            sys.exit()
        for s in shots:
            if a.collideswith(s):
                log_event("asteroid_shot")
                a.split()
                s.kill()
    for d in drawable:
        d.draw(screen)
    pygame.display.flip()
    dt = clock.tick(60.0) / 1000