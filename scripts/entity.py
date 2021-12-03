import pygame
import random
import numpy as np

class Entity:
    def __init__(self, x, y, image, alpha, function, vector, color):
        self.x = x
        self.y = y
        self.color = color
        try:
            self.image = image.copy()
        except:
            self.image = None
        self.alpha = alpha
        self.function = function
        self.vector = vector
        self.radius = random.randrange(3, 5)
        self.sine = random.randrange(-100, 100)
    
    def draw(self, display, shadows, scroll):
        self.sine += 1
        self.function(display, self, shadows, scroll, int(np.sin(self.sine)))

        self.x += self.vector[0]
        self.y += self.vector[1]
        try:
            self.image.set_alpha(self.alpha)
            display.blit(self.image, (self.x-scroll[0], self.y-scroll[1]))
        except:
            pygame.draw.circle(display, self.color, ((self.x-scroll[0]), (self.y-scroll[1])), self.radius)