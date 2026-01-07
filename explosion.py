import pygame
from circleshape import CircleShape

class Explosion(CircleShape):
    def __init__(self, x, y, radius=5):
        super().__init__(x, y, radius)
        self.timer = 0.5  # Lifetime in seconds
        self.particles = []
        for i in range(8):
            vec = pygame.Vector2(1, 0).rotate(i * 45) * 50 # Speed
            self.particles.append({"pos": pygame.Vector2(x, y), "vel": vec})

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

        for p in self.particles:
            p["pos"] += p["vel"] * dt

    def draw(self, screen):
        for p in self.particles:
            pygame.draw.circle(screen, "orange", p["pos"], 2)
