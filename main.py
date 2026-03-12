import sys
import pygame
import random
from constants import (
        SCREEN_WIDTH, 
        SCREEN_HEIGHT, 
        SCORE_PER_ASTEROID,
        POWERUP_SPAWN_RATE_SECS
    )
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot, Laser
from powerups import PowerUp, PowerUpManager

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
    pygame.display.set_caption("Asteroids")

    global _starfield_cache


    """ Testing with init_game, commenting these """
#    # Groups
#    updatable = pygame.sprite.Group()
#    drawable = pygame.sprite.Group()
#    asteroids = pygame.sprite.Group()
#    shots = pygame.sprite.Group()
#
#    # Player
#    Player.containers = (updatable, drawable)
#    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
#    Shot.containers = (updatable, drawable, shots)
#    Laser.containers = (updatable, drawable, shots)
#
#    # Asteroids
#    Asteroid.containers = (asteroids, updatable, drawable)
#    #asteroid = Asteroid()
#
#    # AsteroidField
#    AsteroidField.containers = (updatable)
#    asteroidField = AsteroidField()
#
#    # Initialize delta timer
#    dt = 0
#
#    # Initialize score
#    score = 0
#
#    # Initialize list of powerups
#    powerups_active = player.powerups_active
    """ End here """

    # Initialize game over = false
#    game_over = False
    # Initialize pause screen
#    pause = False

    # Initialize score fonts
    #score_font = pygame.font.Font(None, 48)
    #score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    #screen.blit(score_text, (10, 10))

    while True:
#        log_state()
        
        """ Testing with the init_game function """
        game_objects = init_game()
        updatable = game_objects["updatable"]
        drawable = game_objects["drawable"]
        asteroids = game_objects["asteroids"]
        shots = game_objects["shots"]
        powerups = game_objects["powerups"]
        player = game_objects["player"]

        powerup_manager = PowerUpManager()

        dt = 0
        score = 0
        powerup_spawn_timer = 0.0

        game_over = False
        paused = False
        font = pygame.font.Font(None, 48)
        pause_font = pygame.font.Font(None, 72)

        while not game_over:
            log_state()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused

            if not paused:
                # Update power-up manager
                powerup_manager.update(dt)
                player.shield_active = powerup_manager.shield_active
                player.speed_active = powerup_manager.speed_active
                player.rapid_shot_active = powerup_manager.rapid_shot_active
                player.triple_shot_active = powerup_manager.triple_shot_active
                player.scatter_shot_active = powerup_manager.scatter_shot_active
                player.laser_active = powerup_manager.laser_active

                updatable.update(dt)

                # Spawn power-ups (when not paused)
                powerup_spawn_timer += dt
                if powerup_spawn_timer > POWERUP_SPAWN_RATE_SECS and len(powerups) == 0:
                    powerup_spawn_timer = 0
                    x = random.randint(50, SCREEN_WIDTH -50)
                    y = random.randint(50, SCREEN_HEIGHT -50)
                    powerup = PowerUp(x, y)
                    powerup.containers = (powerups, updatable, drawable)
                    powerup.add((powerups, updatable, drawable))

            # Check collisions
            for asteroid in asteroids:
                if player.shield_active:
                    # Shield protects from one hit
                    if asteroid.collides_with(player):
                        log_event("player_shield_hit")
                        asteroid.split()
                        score += SCORE_PER_ASTEROID
                        powerup_manager.shield_active = False
                        player.shield_active = False
                else:
                    if player.collides_with_triangle(asteroid):
                        log_event("player_hit")
                        game_over = True
                        break

            # Check collisions: shots vs asteroids
            for asteroid in list(asteroids):
                for shot in list(shots):
                    if shot.collides_with(asteroid) or shot.collides_with_laser(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()
                        score += SCORE_PER_ASTEROID
                        break

            for powerup in list(powerups):
                if powerup.collides_with(player):
                    log_event("powerup_collected", type=powerup.powerup_type)
                    powerup_manager.activate(powerup.powerup_type)
                    powerup.kill()

            # Draw everything
            draw_background(screen)

            for obj in drawable:
                obj.draw(screen)

            # Draw score (top left, always on)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Draw pause screen
            if paused:
                pause_text = pause.font.render("PAUSED", True, (255, 255, 255))
                pause_rect = pause_text.get_rect(
                    center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                )
                # Draw semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                screen.blit(pause_text, pause_rect)

            # Draw power-up status
            y_offset = 60
            if powerup_manager.shield_active:
                shield_text = font.render(
                    f"Shield: {round(powerup_manager.shield_timer, 2)}s", True, (0, 100, 255)
                )
                screen.blit(shield_text, (10, y_offset))
                y_offset += 40
            if powerup_manager.rapid_shot_active:
                rapid_shot_text = font.render(
                    f"Rapid Shot: {round(powerup_manager.rapid_shot_timer, 2)}s", True, (255, 0, 0)
                )
                screen.blit(rapid_shot_text, (10, y_offset))
                y_offset += 40
            if powerup_manager.triple_shot_active:
                triple_shot_text = font.render(
                    f"Triple Shot: {round(powerup_manager.triple_shot_timer, 2)}s", True, (255, 255, 0)
                )
                screen.blit(triple_shot_text, (10, y_offset))
                y_offset += 40
            if powerup_manager.scatter_shot_active:
                scatter_shot_text = font.render(
                    f"Scatter Shot: {round(powerup_manager.scatter_shot_timer, 2)}s", True, (125, 0, 255)
                )
                screen.blit(scatter_shot_text, (10, y_offset))
                y_offset += 40
            if powerup_manager.speed_active:
                speed_text = font.render(
                    f"Speed: {round(powerup_manager.speed_timer, 2)}s", True, (0, 200, 255)
                )
                screen.blit(speed_text, (10, y_offset))
                y_offset += 40
            if powerup_manager.laser_active:
                laser_text = font.render(
                    f"Laser: {round(powerup_manager.laser_timer, 2)}s", True, (0, 0, 255)
                )
                screen.blit(laser_text, (10, y_offset))
                y_offset += 40

            pygame.display.flip()
            dt = clock.tick(60) / 1000

        # Game over - show screen and check for restart
        if not game_over_screen(screen, score):
            return




        """ End testing, uncomment after here when done """ 
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                return
#
#        #screen.fill("black")
#        draw_background(screen)
#
#        #player.draw(screen)
#        for member in drawable:
#            member.draw(screen)
#
#        # Draw score, always on top, top-left
#        score_font = pygame.font.Font(None, 48)
#        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
#        screen.blit(score_text, (10, 10))
#        # Show powerups
#        powerup_font = pygame.font.Font(None, 48)
#        powerup_text = powerup_font.render(f"Powerups active: {powerups_active}", True, (255, 255, 255))
#        # Only show list of powerups if active
#        if powerups_active != []:
#            screen.blit(powerup_text, (10, 60))
#
#        #player.update(dt)
#        updatable.update(dt)
#        for asteroid in asteroids:
#            if player.collides_with_triangle(asteroid):
#                log_event("player_hit")
#                print("Game over!")
#                print(f"Score: {score}")
#                game_over_screen(screen, score)
#                #sys.exit()
#            for shot in shots:
#                if shot.collides_with(asteroid) or shot.collides_with_laser(asteroid):
#                    log_event("asteroid_shot")
#                    shot.kill()
#                    asteroid.split()
#                    score += SCORE_PER_ASTEROID
#        # refresh the screen
#        pygame.display.flip()
#
#        # limit the framerate to 60 FPS
#        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
