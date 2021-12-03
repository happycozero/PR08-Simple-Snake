import pygame
pygame.font.init()
pygame.init()

def load_font(font_name, font_size):
    return pygame.font.Font(font_name, font_size)

WINDOW_SIZE = (900, 700)
BLACK = (0,0,0)
WHITE = (255,255,255)
TITLE = "Swinging Wizards"
SCREEN = pygame.display.set_mode(WINDOW_SIZE, pygame.DOUBLEBUF | pygame.HWSURFACE)
FPS = 60
TARGET_FPS = 60
#FPS_FONT = load_font("dpcomic.ttf", 40)
CLOCK = pygame.time.Clock()

