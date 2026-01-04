import pygame
import random
from circleshape import CircleShape
from constants import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        oldRadius = self.radius
        oldPosition = self.position
        oldVelocity = self.velocity
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            splitAngle = random.uniform(20,50)
            vel1 = oldVelocity.rotate(splitAngle)
            vel2 = oldVelocity.rotate(-splitAngle)
            splitRadius = oldRadius - ASTEROID_MIN_RADIUS
            split1 = Asteroid(oldPosition.x, oldPosition.y, splitRadius)
            split2 = Asteroid(oldPosition.x, oldPosition.y, splitRadius)
            split1.velocity = vel1 * 1.2
            split2.velocity = vel2 * 1.2