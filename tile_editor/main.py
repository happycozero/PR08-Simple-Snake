import pygame
from pygame.locals import *
import engine
import time
import os

pygame.init()

# Clock 
clock = engine.CreateClock()

# Window
win = engine.SetWindow(1280, 736, pygame.VIDEORESIZE, 1)


# Caption
caption = engine.SetCaption("Snake Game!")

# Variables"
FPS = 60
game = True

gravity = 0.2

last_time = time.time()


# Sprites
playerSprite = engine.LoadImage(os.path.join('data', 'sprite', 'player.png'))
block0 = engine.LoadImage('./data/sprite/block0.png')
block1 = engine.LoadImage('./data/sprite/block1.png')
block2 = engine.LoadImage('./data/sprite/block2.png')

sprites = {"playerSprite": playerSprite,
           "block0": block0, "block1": block1, "block2": block2}

# Player
class Player():
    def __init__(self):
        self.gameObject = engine.GameObject(64, 500, 32, 32, playerSprite)
        self.runSpeed = 3
        self.maxSpeed = 3
        self.jumpSpeed = 5
        self.velocityY = 0
        self.maxSpeedX = 3
        self.dx = 0
        self.jump = 1
        self.selectedLevel = 1

    def Teleport(self, x, y):
        self.velocityY = 0
        self.dx = 0
        self.gameObject.rect.x = x
        self.gameObject.rect.y = y

    def Update(self, surface, ground, Input, selectedLevel):
        self.dx = 0

        # MOVEMENT
        if Input.GetKey(K_a) and abs(self.dx) <= self.maxSpeedX:
            self.dx -= self.runSpeed
        if Input.GetKey(K_d) and abs(self.dx) <= self.maxSpeedX:
            self.dx += self.runSpeed
            
        # JUMP
        if Input.GetKeyDown(K_w) and self.jump > 0:
            self.velocityY = -self.jumpSpeed
            self.jump -= 1
        
        # DETECT RECTS
        detectGround = pygame.Rect(
            self.gameObject.rect.x, self.gameObject.rect.y + 4, self.gameObject.width, self.gameObject.height)
        detectCeiling = pygame.Rect(
            self.gameObject.rect.x, self.gameObject.rect.y - 4, self.gameObject.width, self.gameObject.height)
        detectSides = pygame.Rect(self.gameObject.rect.x + self.dx,
                                  self.gameObject.rect.y, self.gameObject.width, self.gameObject.height)

        # GRAVITY
        self.velocityY += gravity
        if self.velocityY > 10:
            self.velocityY = 10
        self.gameObject.rect.y += self.velocityY

        for i in ground["blocks"]:
            """ DETECT X """
            if i.rect.colliderect(detectSides):
                self.dx = 0

            """ DETECT Y """
            # DETEC GROUND
            if i.rect.colliderect(detectGround):
                # DETECT LAVA
                if i.type == "block1":
                    self.Teleport(64, 500)
                # DETECT FINISH
                if i.type == "block2":
                    if selectedLevel + 1 < 4:
                        self.selectedLevel += 1
                        self.Teleport(64, 500)
                    

                if self.velocityY > 0:
                    self.gameObject.rect.y = i.rect.top - self.gameObject.height
                    self.jump = 1
                    self.velocityY = 0
            # DETECT CEILING
            if i.rect.colliderect(detectCeiling):
                if self.velocityY < 0:
                    self.gameObject.rect.y = i.rect.top + self.gameObject.height
                    self.velocityY = 0

        # UPDATE X
        self.gameObject.rect.x += self.dx

        # DRAW OBJECT
        self.gameObject.DrawObject(surface)


player = Player()

# BLOCK
class Block():
    def __init__(self, x, y, sprite, type):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.type = type  # "block0" : "NORMAL", "block1" : "LAVA", "block2" : "FINISH"
        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

    def DrawBlock(self, surface):
        surface.blit(self.sprite, self.rect)


# ENVIROMENT
def LoadLevel(level):
    f = open(f'./data/world/level{str(level)}.txt', 'r')
    fData = f.read()
    blocks = []
    for i in fData.split("\n"):
        if i != "":
            i = i.split(" ")
            block = Block(i[0], i[1], sprites[i[2]], i[2])
            blocks.append(block)
    ground = {"blocks": []}
    ground["blocks"] = blocks
    f.close()
    return ground


previousLevel = player.selectedLevel - 1
selectedLevel = player.selectedLevel
ground = LoadLevel(selectedLevel)  # LOAD LEVEL

# Main Loop
while game:

    win.fill((50, 50, 50))
    
    # LEVEL 
    selectedLevel = player.selectedLevel
    if selectedLevel - previousLevel == 2:
        print(selectedLevel)
        ground = LoadLevel(selectedLevel)
        previousLevel = selectedLevel - 1

    # INPUT
    Input = engine.Input(engine.Events(), engine.GetPressedKey(
    ), engine.GetMousePos(), engine.GetMousePressed())

    # EXIT EVENT
    for event in Input.events:
        if event.type == pygame.QUIT:
            game = False
    if Input.GetKeyDown(K_ESCAPE):
        game = False

    # PLAYER UPDATE
    player.Update(win, ground, Input, selectedLevel)

    # DRAW WORLD
    for block in ground["blocks"]:
        block.DrawBlock(win)

    # DISPLAY UPDATE
    pygame.display.update()
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
