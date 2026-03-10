import pygame
import sys
import math
from constants import (
        PLAYER_RADIUS, 
        LINE_WIDTH, 
        PLAYER_TURN_SPEED, 
        PLAYER_SPEED, 
        PLAYER_MAX_SPEED,
        PLAYER_SHOOT_SPEED, 
        PLAYER_SHOOT_COOLDOWN_SECONDS, 
        PLAYER_ACCELERATION,
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
#        self.velocity = pygame.math.Vector2(0, 0)


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
        #if self.velocity != pygame.math.Vector2(0, 0):
        #    self.move(dt)
#        self.position += self.velocity * dt
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
#            self.move(dt)
            self.accelerate(dt)
        if keys[pygame.K_s]:
#            self.move(-dt)
            self.accelerate(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        #    if self.shot_cooldown < PLAYER_SHOOT_COOLDOWN_SECONDS:
        #        self.shot_cooldown += PLAYER_SHOOT_COOLDOWN_SECONDS
        #        self.shoot()
        if keys[pygame.K_ESCAPE]:
            print("Quitting")
            sys.exit()

        self.move()

        if not (keys[pygame.K_w] or keys[pygame.K_s]):
            deceleration = 0.9 * dt
            if self.velocity.length() > deceleration:
                self.velocity -= self.velocity.normalize() * deceleration
            else:
                self.velocity = pygame.Vector2(0, 0)

    #def move(self, dt):
    def move(self):
        self.position += self.velocity

##        unit_vector: pygame.Vector2 = pygame.Vector2(0, 1)
##        rotated_vector: pygame.Vector2 = unit_vector.rotate(self.rotation)
###        acceleration = self.accelerate(dt) * dt
##        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
##        #rotated_with_speed_vector = acceleration * PLAYER_SPEED * dt
##        
###        acceleration: pygame.Vector2 = (
###                rotated_vector * PLAYER_ACCELERATION * dt
###            )
##
###        self.velocity += acceleration
##        
##        self.position += rotated_with_speed_vector
###        self.position *= self.accelerate(dt)
###        self.position += acceleration * dt
###        self.position += velocity * dt
###        self.wrap_around()
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def accelerate(self, dt):
        #velocity = self.velocity
#        velocity = self.velocity
        max_speed = PLAYER_MAX_SPEED
        unit_vector: pygame.Vector2 = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        acceleration: pygame.Vector2 = (
                #rotated_with_speed_vector * PLAYER_ACCELERATION
                #PLAYER_ACCELERATION * dt
                rotated_vector * PLAYER_ACCELERATION
                #rotated_vector * PLAYER_ACCELERATION * dt
            )

#        velocity += acceleration 
#        self.velocity += velocity
#        if self.velocity.length() > max_speed:
#            self.velocity: pygame.Vector2 = self.velocity.normalize() * max_speed
        self.velocity += acceleration * dt
        if self.velocity.length() > max_speed:
            self.velocity: pygame.Vector2 = self.velocity.normalize() * max_speed
#        self.velocity = velocity
#        self.position += self.velocity * dt



    def shoot(self):
        cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
#        x = self.position[0]
#        y = self.position[1]
        if self.shot_cooldown > 0:
            return
        self.shot_cooldown += cooldown
        shot: Shot = Shot(self.position.x, self.position.y) 
        shot.velocity: pygame.Vector2 = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        #self.shot_cooldown += PLAYER_SHOOT_COOLDOWN_SECONDS

