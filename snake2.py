# imp
import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (116, 186, 78)
blue = (50, 153, 213)
barbie = (255, 5, 134)

dis_width = 600
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка на питоне')

clock = pygame.time.Clock()

snake_block = 15
snake_speed = 5

font_style = pygame.font.SysFont("bahnschrift", 22)
score_font = pygame.font.SysFont("comicsansms", 28)

def Your_score(score):
    dis.blit(score_font.render("Ваш счет: " + str(score), True, yellow), [0, 0])

def our_snake(snake_block, snake_list):
    for x, y in snake_list:
        pygame.draw.rect(dis, green, [x, y, snake_block - 0.1, snake_block - 0.1])

def message(msg, color):
    dis.blit(font_style.render(msg, True, color), [dis_width // 6, dis_height // 3])

def gameLoop():
    game_over = False
    game_close = False

    x1, y1 = dis_width // 2, dis_height // 2
    x1_change, y1_change = 0, 0
    snake_List = []
    Length_of_snake = 1
    snake_speed = 5
    ecx = 1

    foodx, foody = round(random.randrange(0, dis_width - snake_block) / 15.0) * 15.0, round(random.randrange(0, dis_height - snake_block) / 15.0) * 15.0
    foodx1, foody1 = round(random.randrange(0, dis_width - snake_block) / 15.0) * 15.0, round(random.randrange(0, dis_height - snake_block) / 15.0) * 15.0

    while not game_over:
        while game_close:
            dis.fill(blue)
            message('Нажмите R - Играть снова или Q - Выход', red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    x1_change = snake_block
                    y1_change = 0
                elif event.key in (pygame.K_UP, pygame.K_w):
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        if ecx > 10:
            pygame.draw.rect(dis, red, [foodx1, foody1, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if Length_of_snake < 1:
            game_close = True
        if Length_of_snake == 0 and ecx > 10:
            game_close = True
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 15.0) * 15.0
            foody = round(random.randrange(0, dis_height - snake_block) / 15.0) * 15.0
            foodx1 = round(random.randrange(0, dis_width - snake_block) / 15.0) * 15.0
            foody1 = round(random.randrange(0, dis_height - snake_block) / 15.0) * 15.0
            Length_of_snake += 1
            ecx += 1
            if snake_speed < 8:
                snake_speed += 0.2
            if snake_speed > 8 or snake_speed < 12:
                snake_speed += 0.1
            if snake_speed > 12:
                snake_speed += 0.05
        if x1 == foodx1 and y1 == foody1:
            foodx1 = round(random.randrange(0, dis_width - snake_block) / 15.0) * 15.0
            foody1 = round(random.randrange(0, dis_height - snake_block) / 15.0) * 15.0
            foodx = round(random.randrange(0, dis_width - snake_block) / 15.0) * 15.0
            foody = round(random.randrange(0, dis_height - snake_block) / 15.0) * 15.0
            Length_of_snake -= 3
            snake_Head.append(-x1)
            snake_Head.append(-y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[1:4]
            if Length_of_snake < 1:
                game_close = True

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
