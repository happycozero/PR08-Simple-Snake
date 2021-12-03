import pygame
import math
import numpy as np
import time


class Bullet:
    def __init__(self, x, y, mouse_x, mouse_y, scroll, image, rot_angle):
        self.x = x
        self.y = y
        self.angle = math.atan2((self.y)-scroll[1]-mouse_y, (self.x)-scroll[0]-mouse_x)
        self.x_vel = math.cos(self.angle)*2
        self.y_vel = math.sin(self.angle)*2
        self.image = image
        self.rot_angle = rot_angle
        self.y_vel = 3
        self.start_time = time.time()
        

    def draw(self, display, shadows, scroll):
        self.x += -self.x_vel
        self.y += -self.y_vel
        self.y_vel -= 0.4
        self.start_time += 1
        pygame.draw.circle(shadows, (212, 30, 60,100), (self.x-scroll[0], self.y-scroll[1]), 3+abs(np.sin(self.start_time)*5))
        display.blit(self.image, (self.x-scroll[0]-5, self.y-scroll[1]-5))
        #pygame.draw.circle(display, (0,0,0), (self.x-scroll[0], self.y-scroll[1]), 4)
        #pygame.draw.rect(display, (255,0,0), (self.x-scroll[0]-25, self.y-scroll[1]-25, 50, 50), 1)
