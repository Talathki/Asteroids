import pygame
import random

from circleshape import CircleShape
from constants import (
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        LINE_WIDTH,
        POWERUP_DURATION
    )

class PowerUp(CircleShape):
    POWERUP_TYPES = ["laser", "shield", "rapid_shot", "scatter_shot", "triple_shot", "speed"]

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.powerup_type = random.choice(self.POWERUP_TYPES)
        self.rotation = 0.0
        self.rotation_speed = 90.0

    def draw(self, screen):
        points = []
        for i in range(4):
            angle = self.rotation + i * 90
            point = self.position + pygame.Vector2(0, self.radius).rotate(angle)
            points.append(point)

        colors = {
            "laser": (0, 0, 255),           # Light Green
            "shield": (0, 100, 255),        # Blue
            "rapid_shot": (255, 0, 0),      # Red
            "scatter_shot": (125, 0, 255),  # Purple
            "triple_shot": (255, 255, 0),   # Yellow
            "speed": (0, 200, 255)          # Light Blue
        }
        color = colors.get(self.powerup_type, "white")
        pygame.draw.polygon(screen, color, points, LINE_WIDTH)

    def update(self, dt):
        self.rotation += self.rotation_speed * dt
        # Wrap around screen
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

class PowerUpManager:
    def __init__(self):
        """ PowerUp booleans """
        self.laser_active = False
        self.shield_active = False
        self.rapid_shot_active = False
        self.scatter_shot_active = False
        self.triple_shot_active = False
        self.speed_active = False

        """ PowerUp Timers """
        self.laser_timer = 0.0
        self.shield_timer = 0.0
        self.rapid_shot_timer= 0.0
        self.scatter_shot_timer = 0.0
        self.triple_shot_timer = 0.0
        self.speed_timer = 0.0

    def activate(self, powerup_type):
        if powerup_type == "laser":
            self.laser_active = True
            self.laser_timer = POWERUP_DURATION 
        if powerup_type == "shield":
            self.shield_active = True
            self.shield_timer = POWERUP_DURATION 
        if powerup_type == "rapid_shot":
            self.rapid_shot_active = True
            self.rapid_shot_timer = POWERUP_DURATION 
        if powerup_type == "scatter_shot":
            self.scatter_shot_active = True
            self.scatter_shot_timer = POWERUP_DURATION 
        if powerup_type == "triple_shot":
            self.triple_shot_active = True
            self.triple_shot_timer = POWERUP_DURATION 
        if powerup_type == "speed":
            self.speed_active = True
            self.speed_timer = POWERUP_DURATION 

    def update(self, dt):
        if self.laser_active:
            self.laser_timer -= dt
            if self.laser_timer <= 0:
                self.laser_active = False

        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False

        if self.rapid_shot_active:
            self.rapid_shot_timer -= dt
            if self.rapid_shot_timer <= 0:
                self.rapid_shot_active = False

        if self.scatter_shot_active:
            self.scatter_shot_timer -= dt
            if self.scatter_shot_timer <= 0:
                self.scatter_shot_active = False

        if self.triple_shot_active:
            self.triple_shot_timer -= dt
            if self.triple_shot_timer <= 0:
                self.triple_shot_active = False

        if self.speed_active:
            self.speed_timer -= dt
            if self.speed_timer <= 0:
                self.speed_active = False
