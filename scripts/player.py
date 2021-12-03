import pygame
from scripts.constants import *
from scripts.images import *
from scripts.framework import *
import numpy as np
from functools import lru_cache

time = np.arange(-5, 1, 0.1)
amplitude   = np.sin(time)

class Player:
    def __init__(self, x, y, movement_speed):
        self.x = x
        self.y = y
        self.player_rect = pygame.Rect(self.x,self.y, 10, 16)
        self.player_movement = [0,0]
        self.moving_left = False
        self.moving_right = False
        self.movement_speed = movement_speed
        self.scroll = [0,0]
        self.vertical_momentum = 0
        self.air_timer = 0
        self.current_animation = 0
        self.animations = [idle_imgs, run_imgs, jump_img]
        self.animation_index = 0
        self.flipped = False
        self.rotation = 0
        self.jumping = False
        self.scale = [18, 27]

        



    
    def get_input(self, dt):
        self.player_movement = [0,0]
        self.air_timer += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.air_timer < 6:
                self.current_animation = 1
            else:

                self.animation_count = 2
            self.player_movement[0] -= self.movement_speed*dt*TARGET_FPS
        if keys[pygame.K_d]:
            if self.air_timer < 6:
                self.current_animation = 1
            else:
                self.animation_count = 2
            self.player_movement[0] += self.movement_speed*dt*TARGET_FPS

        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            if self.air_timer < 6:
                self.current_animation = 0 #Set the animation to idle
            else:
                self.current_animation = 2 #Set the animation to idle

        if self.player_movement[0] > 0:
            self.flipped = False
        elif self.player_movement[0] < 0:
            self.flipped = True

        self.player_movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.5
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3

    def check_collisions(self, tile_rects, scroll):
        hit_list = []
        for tile in tile_rects:
            if pygame.Rect(self.player_rect.x-scroll[0], self.player_rect.y-scroll[1], self.player_rect.width, self.player_rect.height).colliderect(pygame.Rect(tile[0]-scroll[0], tile[1]-scroll[1], tile[2], tile[3])):
                hit_list.append(pygame.Rect(tile[0], tile[1], 16, 16))
        return hit_list



    def move(self, tile_rects, scroll):
        collisions = {"top": False,
                    "bottom": False, 
                    "left": False,
                    "right": False}
        self.player_rect.x += self.player_movement[0]
        hit_list = self.check_collisions(tile_rects, scroll)
        for tile in hit_list:
            if self.player_movement[0] > 0:
                self.player_rect.right = tile.left
                collisions["right"] = True
            elif self.player_movement[0] < 0:
                self.player_rect.left = tile.right
                collisions["left"] = True


        self.player_rect.y += self.player_movement[1]
        hit_list = self.check_collisions(tile_rects, scroll)
        for tile in hit_list:
            if self.player_movement[1] > 0:
                self.player_rect.bottom = tile.top 
                collisions["bottom"] = True
                self.rotation = 0
                self.jumping = False
            elif self.player_movement[1] < 0:
                self.player_rect.top = tile.bottom
                collisions["top"] = True

        
        return self.player_rect, collisions




    def calculate_scroll(self):
        self.scroll[0] += (self.player_rect.x-self.scroll[0]-150)/10
        self.scroll[1] += (self.player_rect.y-self.scroll[1]-150)/10


    def draw(self, display, scroll):

        #pygame.draw.rect(display, (0,0,0), (self.player_rect.x-scroll[0], self.player_rect.y-scroll[1], self.player_rect.width, self.player_rect.height))
        self.animation_index = animate(self.animations[self.current_animation], self.animation_index, 10)
        image = self.animations[self.current_animation][self.animation_index//10]
        #image = pygame.transform.rotate(image, self.rotation)

        display.blit(pygame.transform.flip(pygame.transform.rotate(image, self.rotation), self.flipped, False), (self.player_rect.x-scroll[0], self.player_rect.y-scroll[1]-2))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.player_rect.x-scroll[0]+image.get_width()/2, mouse_y -  self.player_rect.y-scroll[1]

        

        angle = math.atan2(rel_y, rel_x)

        angle = math.degrees(angle)

        #display.blit(pygame.transform.rotate(bow_img, angle), (self.player_rect.x-scroll[0]+image.get_width()/2, self.player_rect.y-scroll[1]))





    def main(self, display, dt, tile_rects, scroll):

        if self.rotation >= 360 or self.rotation <= -360:
            self.rotation = 0
            self.jumping = False

        self.get_input(dt)
        self.rect, collisions = self.move(tile_rects, scroll)
        if collisions['bottom'] == True:
            self.air_timer = 0
        if collisions['top'] == True:
            self.vertical_momentum = 0




        self.calculate_scroll()
        self.draw(display, scroll)

