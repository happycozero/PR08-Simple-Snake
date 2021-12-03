import pygame

class Particle:
    def __init__(self, x, y, x_vel, y_vel, radius, color, gravity_scale):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.gravity = 1
        self.radius = radius
        self.color = color
        self.lifetime = 2000
        self.gravity_scale = gravity_scale

    def draw(self, display, scroll):
        self.lifetime -= 1
        self.gravity -= self.gravity_scale
        self.x += self.x_vel
        self.y += self.y_vel * self.gravity
        self.radius -= 0.01
        pygame.draw.circle(display,self.color,(int(self.x)-scroll[0], int(self.y)-scroll[1]), self.radius)
        #pygame.draw.rect(display, self.color, (int(self.x)-scroll[0], int(self.y)-scroll[1], self.radius, self.radius))