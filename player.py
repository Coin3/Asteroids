import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)

        self.rotation = 0
        self.cooldown = 0
        self.weapon_type = "default" # default, double
        self.speed_multiplier = 1.0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        # Acceleration logic
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        # PLAYER_SPEED is now acceleration
        acceleration = rotated_vector * PLAYER_SPEED * self.speed_multiplier * dt
        self.velocity += acceleration
    
    def update(self, dt):
        self.cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Apply velocity to position
        self.position += self.velocity * dt
        # Apply friction
        self.velocity *= 0.98

        # Wrap around screen
        self.wrap_position()

    def shoot(self):
        if self.cooldown <= 0:
            if self.weapon_type == "default":
                playerShot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
                playerShot.velocity = pygame.Vector2(0,1)
                playerShot.velocity = playerShot.velocity.rotate(self.rotation)
                playerShot.velocity = playerShot.velocity * PLAYER_SHOOT_SPEED
            elif self.weapon_type == "double":
                # Create two shots offset by a bit
                offset = pygame.Vector2(0, 1).rotate(self.rotation + 90) * 10

                shot1 = Shot(self.position.x + offset.x, self.position.y + offset.y, SHOT_RADIUS)
                shot1.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

                shot2 = Shot(self.position.x - offset.x, self.position.y - offset.y, SHOT_RADIUS)
                shot2.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

            self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        else:
            pass

    def collideswith(self, other):
        # Check if polygon (self) collides with circle (other)
        # 1. Check if other center is inside the triangle
        # 2. Check if other intersects any of the triangle edges

        # Get triangle vertices
        vertices = self.triangle()

        # Function to check if point is in triangle
        def is_point_in_triangle(p, p0, p1, p2):
            s = p0.y * p2.x - p0.x * p2.y + (p2.y - p0.y) * p.x + (p0.x - p2.x) * p.y
            t = p0.x * p1.y - p0.y * p1.x + (p0.y - p1.y) * p.x + (p1.x - p0.x) * p.y

            if (s < 0) != (t < 0):
                return False

            A = -p1.y * p2.x + p0.y * (p2.x - p1.x) + p0.x * (p1.y - p2.y) + p1.x * p2.y

            return A < 0 and (s <= 0 and s + t >= A) or (s >= 0 and s + t <= A)

        if is_point_in_triangle(other.position, vertices[0], vertices[1], vertices[2]):
            return True

        # Function to check intersection of line segment and circle
        def intersect_line_circle(p1, p2, circle_center, radius):
            d = p2 - p1
            f = p1 - circle_center

            a = d.dot(d)
            b = 2 * f.dot(d)
            c = f.dot(f) - radius * radius

            discriminant = b*b - 4*a*c

            if discriminant < 0:
                return False

            discriminant = discriminant ** 0.5
            t1 = (-b - discriminant) / (2*a)
            t2 = (-b + discriminant) / (2*a)

            if (0 <= t1 <= 1) or (0 <= t2 <= 1):
                return True
            return False

        # Check edges
        if intersect_line_circle(vertices[0], vertices[1], other.position, other.radius):
            return True
        if intersect_line_circle(vertices[1], vertices[2], other.position, other.radius):
            return True
        if intersect_line_circle(vertices[2], vertices[0], other.position, other.radius):
            return True

        return False
