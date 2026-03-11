import pygame
from circleshape import CircleShape
from constants import (
        SHOT_RADIUS, 
        LINE_WIDTH, 
        SCREEN_WIDTH, 
        SCREEN_HEIGHT,
        LASER_LIFETIME
    )

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
#        self.position = (x, y)
#        self.position_x = x
#        self.position_y = y
#        self.radius = SHOT_RADIUS
#        self.velocity = velocity
#        self.velocity = super().__init__(self.position_x, self.position_y, self.radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

        if (
            self.position.x < -self.radius
            or self.position.x > SCREEN_WIDTH + self.radius
            or self.position.y < -self.radius
            or self.position.y > SCREEN_HEIGHT + self.radius
            ):
                self.kill()
        # For shots that wrap around
#        if self.position.x < 0:
#            self.position.x = SCREEN_WIDTH
#        elif self.position.x > SCREEN_WIDTH:
#            self.position.x = 0
#
#        if self.position.y < 0:
#            self.position.y = SCREEN_HEIGHT
#        elif self.position.y > SCREEN_HEIGHT:
#            self.position.y = 0

class Laser(Shot):
    def __init__(self, x, y, rotation):
        super().__init__(x, y)
        #self.position = pygame.Vector2(x, y)
        self.rotation = rotation
        self.lifetime = 0.0
        self.width = 2
        self.laser_length = 500 # 500 pixels long
        self.direction = pygame.Vector2(0, 1).rotate(self.rotation) 
        self.laser_start_position = self.position
        self.laser_end_position = self.position + (self.direction * self.laser_length)

    def draw(self, screen):
        #laser_length = 500 # 500 pixels long
        #direction = pygame.Vector2(0, 1).rotate(self.rotation) 
        #start_position = self.position
        #end_position = self.position + self.direction * self.laser_length

        #pygame.draw.line(screen, "green", (int(start_position.x), int(start_position.y)), (int(end_position.x), int(end_position.y)), 2)
        pygame.draw.line(screen, "green", self.laser_start_position, self.laser_end_position, self.width)

    def update(self, dt):
        self.lifetime += dt
        
        if self.lifetime > LASER_LIFETIME:
            self.kill()

    def collides_with_laser(self, other):

        laser_vector = self.laser_end_position - self.laser_start_position
        laser_length_squared = laser_vector.length_squared()

        t = max(0, min(1, (other.position - self.laser_start_position).dot(laser_vector) / laser_length_squared))
        closest_point = self.laser_start_position + laser_vector * t
        distance = pygame.math.Vector2.distance_to(other.position, closest_point)
        if distance < (self.width + other.radius):
            return True
        return False

