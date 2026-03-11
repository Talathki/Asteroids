import sys
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_PER_ASTEROID
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot, Laser

""" Cache for starfield """
_starfield_cache = None

""" Function to draw the starfield """
def draw_background(screen: pygame.Surface):
    global _starfield_cache
    if _starfield_cache is None:
        """Generate a starfield"""
        _starfield_cache = []
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(100, 255)
            _starfield_cache.append((x, y, brightness))

    screen.fill((10, 10, 20)) # RGB dark blue-black bg
    """Draw stars"""
    for x, y, brightness in _starfield_cache:
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)

""" Game over screen function """
def game_over_screen(screen, score):
    # Set large, medium, small fonts
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 24)

    # Specify the text for Game over, score, and restart prompt
    game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
    score_text = font_medium.render(f"Final Score: {score}", True, (255, 255, 255))
    restart_text = font_small.render(
        "Press R to Restart, or Q to Quit", True, (200, 200, 200)
    )

    # Create rectangles to render text on screen
    game_over_rect = game_over_text.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
    )
    score_rect = score_text.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    )
    restart_rect = restart_text.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    sys.exit()

        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        pygame.display.flip()

""" Create a pause screen function """
def pause_screen(screen, score):
    pause_font = pygame.font.Font(None, 72)
    pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    )
    resume_font = pygame.font.Font(None, 48)
    resume_text = resume_font.render(
        "Press ESC to resume, or press Q to quit", True, (255, 255, 255)
    )
    resume_rect = resume_text.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)
    )

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    screen.blit(pause_text, pause_rect)
    screen.blit(resume_text, resume_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_q:
                    sys.exit()

""" Function to initialize game objects """
def init_game():
    """ Create container groups """
    # Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    """ Initialize container groups """
    # Short-lived objects
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)

    # AsteroidField to generate asteroids
    AsteroidField.containers = (updatable)
    AsteroidField()

    # Player
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    return {
        "updatable": updatable,
        "drawable": drawable,
        "asteroids": asteroids,
        "shots": shots,
        "powerups": powerups,
        "player": player
    }




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
    Laser.containers = (updatable, drawable, shots)

    # Asteroids
    Asteroid.containers = (asteroids, updatable, drawable)
    #asteroid = Asteroid()

    # AsteroidField
    AsteroidField.containers = (updatable)
    asteroidField = AsteroidField()

    # Initialize delta timer
    dt = 0

    # Initialize score
    score = 0

    # Initialize list of powerups
    powerups_active = player.powerups_active

    # Initialize game over = false
#    game_over = False
    # Initialize pause screen
#    pause = False

    # Initialize score fonts
    #score_font = pygame.font.Font(None, 48)
    #score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    #screen.blit(score_text, (10, 10))

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

        # Draw score, always on top, top-left
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        # Show powerups
        powerup_font = pygame.font.Font(None, 48)
        powerup_text = powerup_font.render(f"Powerups active: {powerups_active}", True, (255, 255, 255))
        # Only show list of powerups if active
        if powerups_active != []:
            screen.blit(powerup_text, (10, 60))

        #player.update(dt)
        updatable.update(dt)
        for asteroid in asteroids:
            if player.collides_with_triangle(asteroid):
                log_event("player_hit")
                print("Game over!")
                print(f"Score: {score}")
                game_over_screen(screen, score)
                #sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid) or shot.collides_with_laser(asteroid):
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
