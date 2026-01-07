import sys
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from powerup import PowerUp

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    font = pygame.font.SysFont("arial", 24)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)
    Explosion.containers = (updatable, drawable, explosions)
    PowerUp.containers = (updatable, drawable, powerups)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    score = 0
    lives = 3
    shield_active = False
    bombs = 1

    def respawn_player_func():
        nonlocal shield_active, bombs, player, score, lives # Use nonlocal for vars in main scope
        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        player.velocity = pygame.Vector2(0, 0)
        player.rotation = 0
        # Reset powerups
        shield_active = False
        player.speed_multiplier = 1.0
        player.weapon_type = "default"
        bombs = 1

        # Clear nearby asteroids to avoid instant death
        for a in list(asteroids):
            if a.position.distance_to(player.position) < 150:
                a.kill()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: # Bomb
                    if bombs > 0:
                        bombs -= 1
                        # Destroy all asteroids
                        for a in list(asteroids): # Iterate over a copy
                            Explosion(a.position.x, a.position.y)
                            a.kill()
                            score += 10

        screen.fill("black")
        updatable.update(dt)

        # Randomly spawn powerups
        if random.random() < 0.001:
            kind = random.choice(["shield", "speed", "weapon"])
            PowerUp(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), kind)

        # Powerup collisions
        for p in list(powerups):
            if player.collideswith(p):
                if p.kind == "shield":
                    shield_active = True
                elif p.kind == "speed":
                    player.speed_multiplier = 1.5
                elif p.kind == "weapon":
                    if player.weapon_type == "default":
                        player.weapon_type = "double"
                    else:
                        player.weapon_type = "default"
                p.kill()

        for a in list(asteroids):
            if player.collideswith(a):
                if shield_active:
                    shield_active = False
                    a.split()
                    Explosion(a.position.x, a.position.y)
                else:
                    log_event("player_hit")
                    Explosion(player.position.x, player.position.y)
                    lives -= 1
                    if lives > 0:
                        print(f"Lives left: {lives}")
                        respawn_player_func()
                    else:
                        print("Game over!")
                        pygame.quit()
                        sys.exit()

            # If asteroid died from shield collision, skip checking shots against it
            if not a.alive():
                continue

            for s in list(shots):
                if not s.alive(): continue

                if a.collideswith(s):
                    log_event("asteroid_shot")
                    Explosion(a.position.x, a.position.y)
                    a.split()
                    s.kill()
                    score += 10
                    break

        for d in drawable:
            d.draw(screen)

        # Draw UI
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))
        lives_surface = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_surface, (10, 40))
        bombs_surface = font.render(f"Bombs: {bombs}", True, (255, 255, 255))
        screen.blit(bombs_surface, (10, 70))

        if shield_active:
            shield_surface = font.render("SHIELD", True, (0, 0, 255))
            screen.blit(shield_surface, (10, 100))
            pygame.draw.circle(screen, "blue", player.position, player.radius + 5, 1)

        pygame.display.flip()
        dt = clock.tick(60.0) / 1000

if __name__ == "__main__":
    main()
