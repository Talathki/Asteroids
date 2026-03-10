import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.position = (x, y)
        self.position_x = x
        self.position_y = y
        self.radius = SHOT_RADIUS
#        self.velocity = velocity
        self.velocity = super().__init__(self.position_x, self.position_y, self.radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

#        if (
#            self.position.x < -self.radius
#            or self.position.x > SCREEN_WIDTH + self.radius
#            or self.position.y < -self.radius
#            or self.position.y > SCREEN_HEIGHT + self.radius
#            ):
#                self.kill()
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

