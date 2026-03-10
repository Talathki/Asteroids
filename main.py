import sys
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_PER_ASTEROID
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

_starfield_cache = None

def draw_background(screen: pygame.Surface):
    global _starfield_cache
    if _starfield_cache is None:
        # Generate a starfield
        _starfield_cache = []
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(100, 255)
            _starfield_cache.append((x, y, brightness))

    screen.fill((10, 10, 20)) # RGB dark blue-black bg
    # Draw stars
    for x, y, brightness in _starfield_cache:
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)

def main():
    VERSION = pygame.version.vernum
    print(f"Starting Asteroids with pygame version: {VERSION}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Player
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    Shot.containers = (updatable, drawable, shots)

    # Asteroids
    Asteroid.containers = (asteroids, updatable, drawable)
    #asteroid = Asteroid()

    # AsteroidField
    AsteroidField.containers = (updatable)
    asteroidField = AsteroidField()

    dt = 0
    score = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        #screen.fill("black")
        draw_background(screen)

        #player.draw(screen)
        for member in drawable:
            member.draw(screen)

        #player.update(dt)
        updatable.update(dt)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                print(f"Score: {score}")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    score += SCORE_PER_ASTEROID
        # refresh the screen
        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
