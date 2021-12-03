import pygame
from pygame.locals import *


def SetWindow(width, height, flags, vsync):
    return pygame.display.set_mode(
        (width, height), flags, vsync)


def SetCaption(caption):
    return pygame.display.set_caption(caption)


def CreateClock():
    return pygame.time.Clock()


def Events():
    return pygame.event.get()


def DisplayUpdate():
    pygame.display.update()


def GetPressedKey():
    return pygame.key.get_pressed()


def GetMousePos():
    return pygame.mouse.get_pos()


def GetMousePressed():
    return pygame.mouse.get_pressed()


def LoadImage(path):
    return pygame.image.load(path)


def SetSurface(width, height):
    return pygame.Surface((width, height))

# Input
class Input():
    def __init__(self, events, keyPressed, mousePos, mousePressed):
        self.events = events
        self.keyPressed = keyPressed
        self.mousePos = mousePos
        self.mousePressed = mousePressed

    """KEYBOARD"""

    def GetKeyDown(self, key):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
                else:
                    return False

    def GetKeyUp(self, key):
        for event in self.events:
            if event.type == pygame.KEYUP:
                if event.key == key:
                    return True
                else:
                    return False

    def GetKey(self, key):
        if self.keyPressed[key]:
            return True
        else:
            return False

    """MOUSE"""

    def GetMouseButton(self, mouseButton):
        if self.mousePressed[mouseButton]:
            return True
        else:
            return False

    def GetMouseButtonDown(self, mouseButton):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mousePressed[mouseButton]:
                    return True
                #else:
                    #return False

    def GetMouseButtonUp(self, mouseButton):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mousePressed[mouseButton]:
                    return True
                else:
                    return False


# GameObject
class GameObject():

    def __init__(self, x, y, width, height, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sprite = sprite

    def DrawObject(self, surface):
        surface.blit(self.sprite, self.rect)
