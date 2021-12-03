import pygame
import math
import random
import time
from scripts.particle import Particle
import numpy as np
from scripts.constants import *
from scripts.images import *
from functools import lru_cache
from scripts.entity import Entity

pygame.font.init()

particles = []
entities = []


def load_map(map_name):
    blocks = []
    with open(map_name, "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            stripped_line = stripped_line.split(" ")
            blocks.append(stripped_line)
        a_file.close()

    lights = []
    gold = []
    enemies = []
    for _ in blocks:
        if _[2] == "block14": #If the block is long grass
            lights.append([int(_[0]), int(_[1])-350])

        if _[2] == "block15": #If the block is long grass
            enemies.append([int(_[0]), int(_[1])-350])
            
            blocks.remove(_)
        if _[2] == "block0": #If the block is long grass
            gold.append([int(_[0]), int(_[1])-350])
            
            blocks.remove(_)

    return blocks, lights, gold, enemies

def load_font(font_name, font_size):
    return pygame.font.Font(font_name, font_size)

def get_text_rect(text):
    return text.get_rect()

def render_text(display, text, font, bold, color, position):
    text = font.render(text, bold, color)
    display.blit(text, position)

def render_button(display, text, font, bold, color, position, clicking):
    text = font.render(text, bold, color)
    text_rect = get_text_rect(text)
    text_rect.center = (position[0]+text_rect.width/2, position[1]+text_rect.height/2)

    display.blit(text, position)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = (mouse_x, mouse_y)

    if text_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, color, text_rect, 1)
        if clicking:
            pass

def calculate_delta_time(dt, prev_time):
    now = time.time()
    dt = now - prev_time
    prev_time = now

    return dt, prev_time

def particle_burst():
    for x in range(1):
        particles.append(Particle(random.randrange(0, 400), -15, random.randrange(-1, 1), -0.05, 4, (163, 167, 194), 1))


def handle_particles(display, scroll):
    for particle in particles:
        #for tile in tile_rects:
            #if pygame.Rect(particle[0]-scroll[0], paricle[1]-scroll[1])
        if particle.lifetime > 0:
            particle.draw(display, scroll)
        else:
            particles.remove(particle)



def render_shadows(display, scroll, shadow_size):
    for i in reversed(range(3)):
        pygame.draw.circle(display, (0,0,0, i*50), (100-scroll[0]+16, 100-scroll[1]+16), (shadow_size+(i*10)))




cache = {}

def cache_wrapper(func):
    if not func in cache:
        cache[func] = {}
    def cached_func(*args):
        if args in cache[func]:
            return cache[func][args]
        value = func(*args)
        cache[func][args] = value
        return value
    return cached_func


def fill_displays(displays, colors):
    for index, display in enumerate(displays):
        display.fill(colors[index])


def animate(image_list, animation_index, time_to_show_image_on_screen):
    if animation_index+1 >= len(image_list)*time_to_show_image_on_screen:
        animation_index = 0
    animation_index += 1


    return animation_index

@cache_wrapper #Cache the font :D
def render_fps_font(font, fps):
    return font.render(fps, True, WHITE)

@cache_wrapper
def rotate(image, rotation):
    return pygame.transform.rotate(image, rotation)

def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
          
    return list

def play_sound(path_to_sound):
    sound = pygame.mixer.Sound(path_to_sound)
    sound.play()

def render_tiles(display, scroll, tiles, player_pos, tile_index):
    tile_rects = []
    for _ in tiles:

        tile_rects.append([int(_[0]), int(_[1])-350, 16, 16, _[2]])
        x = int(_[0])-scroll[0]
        y = int(_[1])-scroll[1]-350
        dist = math.hypot(player_pos[0]-x, player_pos[1]-y)
        if dist < 100:
            try:
                display.blit(tile_index[_[2]], (x, y))
            except:
                pass
                #print(_[2])

    return tile_rects



def render_grass(display, scroll, grass, dt, player):
    for img in grass:
        if img[1]-int(img[0].get_width() / 2)-scroll[0] > -20 and img[1]-int(img[0].get_width() / 2)-scroll[0] < 350:
            if pygame.Rect(player.player_rect.x-scroll[0]-8, player.player_rect.y-scroll[1]-8, player.player_rect.width+16, player.player_rect.height+16).colliderect(pygame.Rect(img[1]-int(img[0].get_width() / 2)-scroll[0]+10, img[2]-int(img[0].get_height() / 2)-scroll[1]+10, 8, 16)):
                img_copy = pygame.transform.rotate(img[0], (np.sin(img[3]))*img[4])
                display.blit(img_copy, (img[1]-int(img[0].get_width() / 2)-scroll[0], img[2]-int(img[0].get_height() / 2)-scroll[1])) 
            else:
                img[3]+=dt
                img_copy = rotate(img[0], round((np.sin(img[3]))*10, 5))
                display.blit(img_copy, (img[1]-int(img[0].get_width() / 2)-scroll[0], img[2]-int(img[0].get_height() / 2)-scroll[1]))

def ghost_effect(entity):
    entity.alpha -= 5

def jump_effect(entity):
    entity.alpha -= 20


def circle_surf(radius, color):
    surf = pygame.Surface((radius, radius))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

def flame_effect(display, entity, shadows, scroll, sine):
    if entity.radius > 1:
        entity.radius -= 0.04
    else:
        entities.remove(entity)
    surf = pygame.Surface((6, 6))
    
    #pygame.draw.circle(surf, (255, 140, 60), (3, 3), 3+sine*entity.radius)
    #surf.set_colorkey((0,0,0))
    #display.blit(surf, ((entity.x-scroll[0])-3, (entity.y-scroll[1])-3), special_flags=pygame.BLEND_RGB_ADD)
    pygame.draw.circle(shadows, (255, 140, 60, 100), (entity.x-scroll[0], entity.y-scroll[1]), (1.5*entity.radius)+sine*5)

def render_button(display, text, font, bold, color, position, clicking, func, thing):
    text = font.render(text, bold, color)
    text_rect = get_text_rect(text)
    text_rect.height -= 10
    text_rect.center = (position[0]+text_rect.width/2, position[1]+text_rect.height/2)

    display.blit(text, position)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = (mouse_x/3, mouse_y/3)

    if thing:
        if text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(display, color, (text_rect.x, text_rect.y+10, text_rect.width, text_rect.height), 1)
            if clicking:
                func()
                clicking = False

