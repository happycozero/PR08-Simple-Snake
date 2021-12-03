import pygame
from pygame.locals import *
import engine
import os
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfile

pygame.init()

# Clock
clock = engine.CreateClock()
FPS = 30
# Window
infoObject = pygame.display.Info()
win = engine.SetWindow(1600, 900, pygame.RESIZABLE, 1)
blockSurface = engine.SetSurface(1280, 736)

# Sprites

block0 = engine.LoadImage(os.path.join('data', 'sprite', 'block0.png'))

block1 = engine.LoadImage(os.path.join('data', 'sprite', 'BottomCornerLeft.png'))
block2 = engine.LoadImage(os.path.join('data', 'sprite', 'BottomCornerRight.png'))
block3 = engine.LoadImage(os.path.join('data', 'sprite', 'Center.png'))
block4 = engine.LoadImage(os.path.join('data', 'sprite', 'MiddleBottom.png'))
block5 = engine.LoadImage(os.path.join('data', 'sprite', 'MiddleRowLeft.png'))
block6 = engine.LoadImage(os.path.join('data', 'sprite', 'MiddleRowRight.png'))
block7 = engine.LoadImage(os.path.join('data', 'sprite', 'TopCornerLeft.png'))
block8 = engine.LoadImage(os.path.join('data', 'sprite', 'TopCornerRight.png'))
block9 = engine.LoadImage(os.path.join('data', 'sprite', 'TopMiddle.png'))

block10 = engine.LoadImage(os.path.join('data', 'sprite', 'Connecter.png'))
block11 = engine.LoadImage(os.path.join('data', 'sprite', 'Connecter2.png'))
block12 = engine.LoadImage(os.path.join('data', 'sprite', 'Connecter3.png'))
block13 = engine.LoadImage(os.path.join('data', 'sprite', 'Connecter4.png'))

block14 = engine.LoadImage(os.path.join('data', 'sprite', 'torch.png'))

block15 = engine.LoadImage(os.path.join('data', 'sprite', 'Skeleton1.png'))

sprites = {"block0": block0,
           "block1": block1, "block2": block2, "block3": block3,
           "block4": block4, "block5": block5, "block6": block6,
           "block7": block7, "block8": block8, "block9": block9,

           "block10": block10,
           "block11": block11, "block12": block12, "block13": block13,
           "block14": block14, "block15": block15}

# SPRITE OPTION
class SpriteOption():
    def __init__(self, rect, spriteName):
        self.rect = rect
        self.spriteName = spriteName

    def Draw(self, surface):
        surface.blit(sprites[self.spriteName], self.rect)

# BLOCK
class Block:
    def __init__(self, color, rect):
        self.rect = rect
        self.mainColor = color
        self.color = color
        self.sprite = ""

    def Draw(self, surface):
        if self.sprite == "":
            pygame.draw.rect(surface, (self.color), self.rect)
        else:
            surface.blit(sprites[self.sprite], self.rect)

#FUNCTIONS
def CreateBlocks():
    z = 0
    blocks = []
    for x in range(0, 1312, 16):
        if z == 0:
            z = 1
        elif z == 1:
            z = 0
        for y in range(0, 768, 16):
            rect = pygame.Rect(x, y, 16, 16)
            if z == 0:
                block = Block((40, 40, 40), rect)
                blocks.append(block)
                z += 1
            else:
                block = Block((35, 35, 35), rect)
                blocks.append(block)
                z = 0
    return blocks

def SaveWorld(blocks):
    text = ""

    for i in blocks:
        if i.sprite != "":
            text += f"{i.rect.x} {i.rect.y} {i.sprite}\n"

    extensions = [('Text Document', '*.txt')]

    f = asksaveasfile(mode='w', defaultextension=".txt", filetypes=extensions)
    if f is None:
        return

    f.write(text)
    f.close()


def OpenWorld(): 
    blocks = CreateBlocks()

    extensions = [('Text Document', '*.txt')]
    f = askopenfile(filetypes=extensions)
    if f is None:
        return blocks
    text = f.read()

    for x in text.split('\n'):
        if x != "":
            x = x.split(" ")
            for block in blocks:
                if int(x[0]) == block.rect.x:
                    if int(x[1])  == block.rect.y:
                        block.sprite = x[2]

    return blocks

# APPENDING BLOCKS
blocks = CreateBlocks()
drawedSprites = []

# CHANGE SPRITE
spriteOptions = []
x = 30
y = 200
for z in sprites.items():
    rect = pygame.Rect(x, y, 32, 32)
    option = SpriteOption(rect, z[0])

    spriteOptions.append(option)
    y += 40


# VARIABLES
game = True
selectedSprite = "block0"

font = pygame.font.Font('freesansbold.ttf', 14)
selectedSpriteRect = pygame.Rect(10, 96, 10, 10)

while game:
    win.fill((50, 50, 50))
    blockSurface.fill((100, 100, 100))
    # INPUT
    Input = engine.Input(engine.Events(), engine.GetPressedKey(
    ), engine.GetMousePos(), engine.GetMousePressed())

    # EXIT EVENT
    for event in Input.events:
        if event.type == pygame.QUIT:
            game = False
    if Input.GetKeyDown(K_ESCAPE):
        game = False

    # OPEN
    openRect = pygame.Rect(200, 30, 90, 30)
    openTextRect = pygame.Rect(200, 37, 60, 30)
    openRectText = font.render("Open World", True, (0, 0, 0))
    pygame.draw.rect(win, (255, 255, 255), openRect)
    win.blit(openRectText, openTextRect)

    if openRect.collidepoint(pygame.mouse.get_pos()):
        if Input.GetMouseButtonDown(0):
            blocks = OpenWorld()

    # SAVE
    saveRect = pygame.Rect(100, 30, 90, 30)
    saveTextRect = pygame.Rect(100, 37, 60, 30)
    saveRectText = font.render("Save World", True, (0, 0, 0))
    pygame.draw.rect(win, (255, 255, 255), saveRect)
    win.blit(saveRectText, saveTextRect)

    if saveRect.collidepoint(pygame.mouse.get_pos()):
        if Input.GetMouseButtonDown(0):
            blocks = SaveWorld(blocks)
        

    # OPTION
    selectedSpriteText = font.render(
        "Selected Sprite: ", True, (255, 255, 255))

    win.blit(selectedSpriteText, selectedSpriteRect)
    win.blit(sprites[selectedSprite], (selectedSpriteRect.x +
             32, selectedSpriteRect.y + 32, 32, 32))

    for x in spriteOptions:
        if x.rect.collidepoint(pygame.mouse.get_pos()):
            if Input.GetMouseButtonDown(0):
                selectedSprite = x.spriteName
                print(selectedSprite)
        x.Draw(win)

    # BLOCKS
    if blocks == None:
        blocks = CreateBlocks()

    for x in blocks:
        if x.rect.collidepoint(pygame.mouse.get_pos()[0] - 160, pygame.mouse.get_pos()[1] - 82):
            x.color = (80, 80, 80)

            # DRAW BLOCK
            if Input.GetMouseButton(0):
                print("yes")
                x.sprite = selectedSprite
            # ERASE BLOCK
            if Input.GetMouseButtonDown(2):
                x.sprite = ""
        else:
            x.color = (x.mainColor)

        x.Draw(blockSurface)

    if Input.GetKeyDown(K_r):
        for x in blocks:
            if x.sprite != "":
                print(x.rect)

    win.blit(blockSurface, (160, 82))
    clock.tick(FPS)
    pygame.display.update()
