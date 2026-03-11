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
        PLAYER_FRICTION,
        SCREEN_WIDTH, 
        SCREEN_HEIGHT
        )
from circleshape import CircleShape
from shot import Shot, Laser

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
#        self.radius = PLAYER_RADIUS # initialized through CircleShape
        self.shot_cooldown = 0
        """Power ups"""
        self.laser_active = False
        self.shield_active = False
        self.rapid_shot_active = False
        self.scatter_shot_active = False
        self.triple_shot_active = False
        self.speed_active = False

        # Create list of active powerups
        self.powerups_active = []

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

    def collides_with_triangle(self, other):
        triangle_points = self.triangle()
        for point in triangle_points:
            if point.distance_to(other.position) <= other.radius:
                return True
        if self.position.distance_to(other.position) <= self.radius + other.radius:
            return True
        return False

    """ Draw the player """
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    """ Rotate player """
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    """ Update on frame refresh """
    def update(self, dt):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt

        keys = pygame.key.get_pressed()
        """ Movement """
        ''' Rotate left (A or Left-Arrow) '''
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        ''' Rotate right (D or Right-Arrow) '''
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        ''' Accelerate forwards (W or Up-Arrow) '''
        if keys[pygame.K_w] or keys[pygame.K_UP]:
#            self.move(dt)         # Movement logic in accelerate and update 
            self.accelerate(dt)
        ''' Accelerate backwards (S or Down-Arrow) '''
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
#            self.move(-dt)        # Movement logic in accelerate and update 
            self.accelerate(-dt)
        ''' Shoot '''
        if keys[pygame.K_SPACE]:
            self.shoot()
        ''' Pause (Currently Quit) '''
        if keys[pygame.K_ESCAPE]:
            print("Quitting")
            sys.exit()

        """ Move in current velocity direction """
        self.move()

        """ Decelerate player over time """
        if not (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_s] or keys[pygame.K_DOWN]):
            deceleration = PLAYER_FRICTION * dt
            if self.velocity.length() > deceleration:
                self.velocity -= self.velocity.normalize() * deceleration
            else:
                self.velocity = pygame.Vector2(0, 0)

        """ Update list of active powerups """
        if self.laser_active and "laser" not in self.powerups_active:
            self.powerups_active.append("laser")

    def move(self):
        self.position += self.velocity

        # moved this logic to acceleration
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
        """Wrap around screen"""
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def accelerate(self, dt):
        max_speed = PLAYER_MAX_SPEED
        unit_vector: pygame.Vector2 = pygame.Vector2(0, 1)
        rotated_vector: pygame.Vector2 = unit_vector.rotate(self.rotation)
        acceleration: pygame.Vector2 = (
                rotated_vector * PLAYER_ACCELERATION
            )

        self.velocity += acceleration * dt
        if self.velocity.length() > max_speed:
            self.velocity: pygame.Vector2 = self.velocity.normalize() * max_speed

    def shoot(self):
        # Add logic if a powerup is active
        cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        if self.rapid_shot_active:
            cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS * 0.1
        elif self.laser_active:
            cooldown = 0

        if self.shot_cooldown > 0:
            return
        self.shot_cooldown += cooldown

        """ Triple Shot """
        if self.triple_shot_active:
            # Shoot 3 shots in spread
            for angle_offset in [-15, 0, 15]:
                shot = Shot(self.position.x, self.position.y)
                shot.velocity = (
                    pygame.Vector2(0, 1).rotate(self.rotation + angle_offset) * PLAYER_SHOOT_SPEED
                )
        """ Scatter shot """
        if self.scatter_shot_active:
            # Shoot 7 shots in spread
            for angle_offset in [-45, -30, -15, 0, 15, 30, 45]:
                shot = Shot(self.position.x, self.position.y)
                shot.velocity = (
                    pygame.Vector2(0, 1).rotate(self.rotation + angle_offset) * PLAYER_SHOOT_SPEED
                )
        """ Laser """
        if self.laser_active:
            shot = Laser(self.position.x, self.position.y, self.rotation)
            shot.rotation = self.rotation
    #        shot: Shot = Shot(self.position.x, self.position.y) 
    #        shot.velocity = (
    #            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    #        )
#            shot.velocity = (
#                pygame.Vector2(0, 1).rotate(self.rotation)
#            )
        """ Standard Shot """
        if not (self.laser_active 
                or self.triple_shot_active 
                or self.scatter_shot_active):
            shot: Shot = Shot(self.position.x, self.position.y) 
            shot.velocity = (
                pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            )

        """ TEST """
#        for angle_offset in [-45, -30, -15, 0, 15, 30, 45]:
#            shot = Shot(self.position.x, self.position.y)
#            shot.velocity = (
#                pygame.Vector2(0, 1).rotate(self.rotation + angle_offset) * PLAYER_SHOOT_SPEED
#            )
        """ END TEST """
