import pygame
import sys
from constants import (
        PLAYER_RADIUS, 
        LINE_WIDTH, 
        PLAYER_TURN_SPEED, 
        PLAYER_SPEED, 
        PLAYER_SHOOT_SPEED, 
        PLAYER_SHOOT_COOLDOWN_SECONDS, 
        SCREEN_WIDTH, 
        SCREEN_HEIGHT
        )
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.radius = PLAYER_RADIUS
        self.shot_cooldown = 0


    def triangle(self):
        forward = (
                pygame.Vector2(0, 1).rotate(self.rotation)
            )
        right = (
                pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
            )
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt

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
            if self.shot_cooldown < PLAYER_SHOOT_COOLDOWN_SECONDS:
                self.shot_cooldown += PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()
        if keys[pygame.K_ESCAPE]:
            print("Quitting")
            sys.exit()



    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        self.wrap_around()
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0


    def shoot(self):
        x = self.position[0]
        y = self.position[1]
        shot = Shot(x, y) 
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        #self.shot_cooldown += PLAYER_SHOOT_COOLDOWN_SECONDS

