import pygame
import random
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class PowerUp(CircleShape):
    def __init__(self, x, y, kind):
        super().__init__(x, y, 15)
        self.kind = kind # "shield", "speed", "weapon"
        self.velocity = pygame.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()

    def draw(self, screen):
        color = "white"
        if self.kind == "shield":
            color = "blue"
        elif self.kind == "speed":
            color = "green"
        elif self.kind == "weapon":
            color = "red"
        pygame.draw.circle(screen, color, self.position, self.radius)
        # Maybe draw a letter/icon
