''''To anyone reading this, let me give you some context - This game was made a 5 day challenge, during those 5 days
I was able to work on the game full-time and had many irl thing to do, the code is therefore a massive mess, I do apologize :(
(also there are definitly bugs xD)'''

import pygame
import time
from scripts.constants import *
import scripts.framework as framework
import scripts.player as player_

import random
from scripts.images import *
import math
import numpy as np
from scripts.bullet import Bullet

from scripts.entity import Entity
from scripts.enemy import Enemy, FlyingEnemy, FlyingDestoryer
import sys



pygame.init()

display = pygame.Surface((300, 233.33))
display.set_alpha(None)

shadows = pygame.Surface((300, 233), pygame.SRCALPHA)
shadows.set_alpha(80)

pygame.display.set_caption(TITLE)
prev_time = time.time()



block_dict = {
"block0": gold_img,
"block1": block1, 
"block2": block2, 
"block3": block3,
"block4": block4, 
"block5": block5, 
"block6": block6,
"block7": block7, 
"block8": block8,
"block9": block9,
"block10": block10,
"block11": block11, 
"block12": block12, 
"block13": block13
}

maps = ["assets/maps/level1.txt","assets/maps/level2.txt", "assets/maps/level3.txt", "assets/maps/level4.txt"]
gold_per_level = [3, 6, 3, 6]
gold_count = 0 
map_index = 0
tiles, lights, gold, enemys = framework.load_map(maps[map_index])

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

player = player_.Player(200, 100, 4)

scroll = [0,0]

entities = []

bullets = []


screen_shake = 0

portal_animation_index = 0

FPS_FONT = pygame.font.Font("assets/font/AvenuePixel-Regular.ttf", 40)
SMALL_FONT = pygame.font.Font("assets/font/AvenuePixel-Regular.ttf", 20)

start_time = time.time()
begin = time.time()

entities = []

flame_cooldown = 0


enemies = []
for enemy in enemys:
    enemies.append(FlyingEnemy(enemy[0], enemy[1], "FlyingEnemy"))
enemy_bullets = []

projectiles = [[-2, 2], [2, -2], [-2, 0], [2, 0], [0, 2], [0, -2]]

particles = []

circles=[]

fall_tiles = []

circle_radius = 30

boot_cooldown_sfx = 0

dead = False
has_spawned_death_particles=False

menu = True

shoot_cooldown = 0

clicking = False

def play():
    global menu
    menu = False

lighting = True



def fancy_lighting_off():
    global lighting
    lighting = False
    print(lighting)



def fancy_lighting_on():
    global lighting
    lighting = True
    print(lighting)

while menu:
    display.fill((17, 5, 36))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                lighting = not lighting
                print(lighting)
                
        '''if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False'''

    main_menu_text = framework.render_fps_font(FPS_FONT, "Down The Mineshaft")
    display.blit(main_menu_text, (42, 20))

    framework.render_button(display, "Play", FPS_FONT, False, (255,255,255), (125, 100), clicking, play, True)
    #print(lighting)
    if lighting:
        framework.render_button(display, "E to disable lighing", FPS_FONT, False, (255,255,255), (40, 135), False, fancy_lighting_off, False)

    if not lighting:
        framework.render_button(display, "E to enable lighing", FPS_FONT, False, (255,255,255), (40, 135), False, fancy_lighting_on, False)
    clicking = False


    SCREEN.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    #SCREEN.blit(pygame.transform.scale(shadows,WINDOW_SIZE),(0,0))
    pygame.display.flip()
    CLOCK.tick(FPS)



while not menu:
    framework.fill_displays([display, shadows], [(17, 5, 36), (0,0,0)])


    scroll[0] += (player.player_rect.x-scroll[0]-150)/8
    scroll[1] += (player.player_rect.y-scroll[1]-75)/8
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    if player.player_movement[0] > 0 or player.player_movement[0] < 0:
        if boot_cooldown_sfx <= 0:
            sound = random.choice(["assets/sound_effects/boot1.wav", "assets/sound_effects/boot2.wav"])
            framework.play_sound(sound)
            boot_cooldown_sfx = 20
        else:
            boot_cooldown_sfx -= 1

    if screen_shake:
        scroll[0] += random.randint(0, 8) - 4
        scroll[1] += random.randint(0, 8) - 4


    now = time.time()
    dt = now - prev_time
    prev_time = now

    tile_rects = framework.render_tiles(display, scroll, tiles, [player.player_rect.x-scroll[0], player.player_rect.y-scroll[1]], block_dict)
    #for tile in tile_rects:
     #   pygame.draw.rect(display, (0,0,0), (tile[0]-scroll[0], tile[1]-scroll[1], 16, 16), 1)
    if not dead:
        player.main(display, dt, tile_rects, scroll)
    else:
        player.player_movement = [0,0]
        if not has_spawned_death_particles:
            for x in range(50):
                #x, y, x_vel, y_vel, gravity, radius
                particles.append([player.x+random.randrange(-3, 3)-scroll[0], player.y+random.randrange(0, 10)-scroll[1], random.randrange(-3, 3), 10, 3, random.choice([(232, 123, 67), (245, 161, 93)])])
            has_spawned_death_particles = True


    
    #Events---------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not dead:
                    player.animation_index = 2
                    if player.air_timer < 6:
                        player.vertical_momentum = -6


            if event.key == pygame.K_RETURN:
                tiles, lights, gold, enemys = framework.load_map(maps[map_index])
                entities = []
                enemies = []
                has_spawned_death_particles = False
                enemy_bullets = []
                for enemy in enemys:
                    enemies.append(FlyingEnemy(enemy[0], enemy[1], "FlyingEnemy"))

                player = player_.Player(100, 100, 4)
                gold_count = 0
                circle_radius = 30
                dead = False
                    

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and shoot_cooldown <= 0:
                framework.play_sound("assets/sound_effects/throw.flac")
                mp = pygame.mouse.get_pos()
                rel_x, rel_y = mp[0] - player.player_rect.x-scroll[0], mp[1] - player.player_rect.y-scroll[1]
                angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

                bullets.append(Bullet(player.player_rect.x, player.player_rect.y, mp[0]/3, mp[1]/3, scroll, bomb_img, angle))
                shoot_cooldown = 37

    if shoot_cooldown > 0:
        shoot_cooldown -= 1

    for bullet in bullets:
        bullet.draw(display, shadows,scroll)
        player.player_movement[0] += 10
        for enemy in enemies:
            try:
                if pygame.Rect(bullet.x-scroll[0]-25, bullet.y-scroll[1]-25, 16, 16).colliderect(pygame.Rect(enemy.x-scroll[0]+enemy.rect.width, enemy.y-scroll[1]+enemy.rect.height, enemy.rect.width, enemy.rect.height)):
                    framework.play_sound("assets/sound_effects/skeleton_death.wav")
                    screen_shake = 10
                    for x in range(50):
                        #x, y, x_vel, y_vel, gravity, radius

                        particles.append([bullet.x+random.randrange(-20, 20), bullet.y+random.randrange(-10, 10), random.randrange(-3, 3), 10, 3, random.choice([(221, 66, 70), (223, 214, 138)])])

                    enemies.remove(enemy)
                    bullets.remove(bullet)
            except:
                pass
                

        for tile in tile_rects: 
            if pygame.Rect(tile[0]-scroll[0], tile[1]-scroll[1], tile[2], tile[3]).colliderect(pygame.Rect(bullet.x-scroll[0], bullet.y-scroll[1], 4, 4)):
                if pygame.Rect(bullet.x-scroll[0]-25, bullet.y-scroll[1]-25, 70, 70).colliderect(pygame.Rect(player.player_rect.x-scroll[0], player.player_rect.y-scroll[1], player.player_rect.width, player.player_rect.height)):
                    player.player_rect.y -= 3
                    player.vertical_momentum = -10
                framework.play_sound("assets/sound_effects/explosion.wav")
                screen_shake = 10
                for x in range(50):

                    #x, y, x_vel, y_vel, gravity, radius
                    particles.append([bullet.x+random.randrange(-20, 20), bullet.y+random.randrange(-10, 10), random.randrange(-3, 3), 10, 3, random.choice([(221, 66, 70), (223, 214, 138)])])

                for enemy in enemies:
                    if pygame.Rect(bullet.x-scroll[0]-25, bullet.y-scroll[1]-25, 50, 50).colliderect(pygame.Rect(enemy.x-scroll[0]+enemy.rect.width, enemy.y-scroll[1]+enemy.rect.height, enemy.rect.width, enemy.rect.height)):
                        framework.play_sound("assets/sound_effects/skeleton_death.wav")
                        enemies.remove(enemy)

                try:
                    circles.append([bullet.x+random.randrange(-10, 10), bullet.y+random.randrange(-10, 10), 10, 10])
                    bullets.remove(bullet)
                except:
                    pass
                break





    for particle in particles:
        particle[0] += particle[2]
        particle[1] -= particle[3]
        particle[3] -= 1
        if particle[2] == 0:
            particle[2] = 2
        particle[4] -= 0.05
        if particle[4] <= 0:
            particles.remove(particle)
        pygame.draw.circle(display, particle[5], (particle[0]-scroll[0], particle[1]-scroll[1]), particle[4])

    for circle in circles:
        circle[2] += 3
        circle[3] -= 1
        if circle[3] <= 1:
            circles.remove(circle)
        pygame.draw.circle(display, random.choice([(221, 66, 70), (223, 214, 138)]), (circle[0]-scroll[0], circle[1]-scroll[1]), circle[2], circle[3])
                    
    if int(gold_count) >= gold_per_level[map_index]:

        if map_index != 3:
            circle_radius += circle_radius//12
            pygame.draw.circle(display, (0,0,0), (300//2, 233.33//2), circle_radius)

            if circle_radius > 300:

                map_index += 1
                tiles, lights, gold, enemys = framework.load_map(maps[map_index])
                entities = []
                enemies = []
                for enemy in enemys:
                    enemies.append(FlyingEnemy(enemy[0], enemy[1], "FlyingEnemy"))

                player = player_.Player(100, 100, 4)
                gold_count = 0
                circle_radius = 30

        else:
            circle_radius += circle_radius//12
            pygame.draw.circle(display, (0,0,0), (300//2, 233.33//2), circle_radius)
            FONT = pygame.font.Font("assets/font/AvenuePixel-Regular.ttf", 35)
            text4 = framework.render_fps_font(FONT, "You Win! Thanks for playing")
            display.blit(text4, (24, 100))
                    
    '''fps = str(int(CLOCK.get_fps()))
    fps_text = framework.render_fps_font(FPS_FONT, fps)
    display.blit(fps_text, (25,25))'''

    '''for tile in tiles:
        if int(tile[1])-scroll[1] < player.player_rect.y-scroll[1]:

            dist = math.hypot((int(tile[0])-scroll[0])-(player.player_rect.x-scroll[0]), (int(tile[1])-scroll[1])-(player.player_rect.y-scroll[1]))
            if dist < 80:
                if tile[4] == "block4":
                     if abs((int(tile[0])-scroll[0])-(player.player_rect.x-scroll[0])) < 10:
                        pygame.draw.rect(display, (255, 0, 0), (int(tile[0])-scroll[0], int(tile[1])-350-scroll[1], 16, 16))
                        fall_tiles.append(tile)'''

    framework.handle_particles(display, scroll)

    if map_index == 0:
        text = framework.render_fps_font(SMALL_FONT, "Hunt for the gold")
        display.blit(text, (150-scroll[0], 100-scroll[1]))

        text2 = framework.render_fps_font(SMALL_FONT, "Click to fire bomb")
        display.blit(text2, (80-scroll[0], -50-scroll[1]))

    if dead:
        
        text3 = framework.render_fps_font(FPS_FONT, "Dead, Enter to restart...")
        display.blit(text3, (20, 100))


    start_time += dt*5
    for i in reversed(range(1)):
        pygame.draw.circle(shadows, (0, 0, 0, 0+i*50), (player.player_rect.x-scroll[0]+3, player.player_rect.y-scroll[1]+4), (40+i*5))

    framework.handle_particles(display, scroll)


    for light in lights:
        display.blit(torch_img, (light[0]-scroll[0], light[1]-scroll[1]))
        if flame_cooldown <= 0:
            framework.entities.append(Entity(random.randrange(light[0], light[0]+10),light[1]+5, None, 255, framework.flame_effect, [0, -0.3], random.choice([(221, 66, 70), (223, 214, 138)])))
            flame_cooldown = 4 
        else:
            flame_cooldown -= 1

    for entity in framework.entities:
        #print(entity)
        entity.draw(display, shadows, scroll)

    for g in gold:
        if pygame.Rect(player.player_rect.x-scroll[0], player.player_rect.y-scroll[1], player.player_rect.width, player.player_rect.height).colliderect(g[0]-scroll[0], g[1]-scroll[1], 16, 16):
            framework.play_sound("assets/sound_effects/pickup.wav")
            gold.remove(g)
            for x in range(30):
                #x, y, x_vel, y_vel, gravity, radius
                particles.append([g[0]+random.randrange(-20, 20), g[1]+random.randrange(-10, 10), random.randrange(-3, 3), 3, 2, (255, 184, 74)])
            gold_count += 1
        g[1] += np.sin(start_time)/5
        display.blit(gold_img, (g[0]-scroll[0], g[1]-scroll[1]))

    for enemy in enemies:
        if enemy.name == "FlyingEnemy":
            enemy.draw(display, scroll, player.player_rect)
            #pygame.draw.rect(display, (255,0,0), (enemy.x-scroll[0]+enemy.rect.width, enemy.y-scroll[1]+enemy.rect.height, enemy.rect.width, enemy.rect.height))
            if enemy.bullet_cooldown <= 0 and enemy.dist < 150:
                for x in range(len(projectiles)):
                    enemy_bullets.append([enemy.x+skeleton_imgs[0].get_width()/2, enemy.y+skeleton_imgs[0].get_height()/2, projectiles[x], 300])
                enemy.bullet_cooldown = 100
            else:
                enemy.bullet_cooldown -= 1

        elif enemy.name == "FlyingDestroyer":
            enemy.draw(display, scroll, player.player_rect,fall_tiles)


            for tile in fall_tiles:
                enemy.width += 1
                pygame.draw.line(display, (212, 30, 60), (enemy.x-scroll[0]+skeleton_imgs[0].get_width()/2, enemy.y-scroll[1]+skeleton_imgs[0].get_height()/2), (tile[0]-scroll[0]+8, tile[1]-scroll[1]+8), enemy.width)

                if enemy.width == 5:
                    tile_rects.remove(tile)
                    
            if fall_tiles == []:
                enemy.width = 1

    for bullet in enemy_bullets:
        pygame.draw.circle(shadows, (212, 30, 60,100), (bullet[0]-scroll[0], bullet[1]-scroll[1]), 2+abs(np.sin(start_time)*5))
        bullet[0] += bullet[2][0]
        bullet[1] += bullet[2][1]
        bullet[3] -= 1
        pygame.draw.circle(display, (212, 30, 60), (bullet[0]-scroll[0], bullet[1]-scroll[1]), 2)

        if pygame.Rect(bullet[0]-scroll[0]-2, bullet[1]-scroll[1]-2, 4, 4).colliderect(player.player_rect.x-scroll[0], player.player_rect.y-scroll[1],
        player.player_rect.width, player.player_rect.height):
            if not dead:
                framework.play_sound("assets/sound_effects/player_death.wav")
                screen_shake = 10
                dead = True


        if bullet[3] <= 0:
            enemy_bullets.remove(bullet)

    gold_count_text = framework.render_fps_font(FPS_FONT, f"Gold: {gold_count}/{gold_per_level[map_index]}")
    display.blit(gold_count_text, (10,10))

    if screen_shake > 0:
        screen_shake -= 1
    
    #Update Screen--------------------------------------------------

    SCREEN.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    if lighting:
        SCREEN.blit(pygame.transform.scale(shadows,WINDOW_SIZE),(0,0))
    pygame.display.flip()
    CLOCK.tick(FPS)