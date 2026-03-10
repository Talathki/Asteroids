import pygame
import math
import random

from circleshape import CircleShape
from constants import (
        LINE_WIDTH, 
        ASTEROID_MIN_RADIUS, 
        SCREEN_WIDTH, 
        SCREEN_HEIGHT
    )
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
        # Lumpy shape points
        num_points = random.randint(8, 12)
        self.shape_points = []

        for i in range(num_points):
            angle = (360 / num_points) * i

            # Vary radius up to 20%
            offset = random.uniform(0.8, 1.2)
            point_radius = radius * offset
            self.shape_points.append((angle, point_radius))

        # Unnecessary
        #self.position = (x, y)
        #self.position_x = x
        #self.position_y = y
        #self.radius = radius
        #self.velocity = super().__init__(self.position_x, self.position_y, self.radius)

    def draw(self, screen):
        # Old, just a circle shape
        #pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

        # draw lumpy asteroids
        points = []
        for angle, point_radius in self.shape_points:
            rad = math.radians(angle)
            x = self.position.x + point_radius * math.cos(rad)
            y = self.position.y + point_radius * math.sin(rad)
            points.append((x, y))
        if len(points) > 2:
            pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)

        # Wrap around screen
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")

            new_angle = random.uniform(20, 50)

            new_vel = self.velocity.rotate(new_angle) * 1.2
            new_neg_vel = self.velocity.rotate(-new_angle) * 1.2
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = new_vel
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2.velocity = new_neg_vel

        
