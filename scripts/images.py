import pygame
from scripts.constants import *
import os

def load_img(img, transparent):

    if transparent == False:

        image = pygame.image.load(img).convert()
        image.set_colorkey(WHITE)
    else:
        image = pygame.image.load(img)
    return image

test_block = load_img("assets/images/block0.png", False)

idle_imgs = [load_img("assets/images/player/idle/idle_1.png", False), 
load_img("assets/images/player/idle/idle_2.png", False), 
load_img("assets/images/player/idle/idle_3.png", False)]

run_imgs = [load_img("assets/images/player/run/run_1.png", False), 
load_img("assets/images/player/run/run_2.png", False), 
load_img("assets/images/player/run/run_3.png", False), 
load_img("assets/images/player/run/run_4.png", False)]

jump_img = [load_img("assets/images/player/jump/jump.png", False)]
print(os.path.join('assets', 'images', 'BottomCornerLeft.png'))
block1 = load_img('assets/images/BottomCornerLeft.png', False)
block2 = load_img('assets/images/BottomCornerRight.png', False)
block3 = load_img('assets/images/Center.png', False)
block4 = load_img('assets/images/MiddleBottom.png', False)
block5 = load_img('assets/images/MiddleRowLeft.png', False)
block6 = load_img('assets/images/MiddleRowRight.png', False)
block7 = load_img('assets/images/TopCornerLeft.png', False)
block8 = load_img('assets/images/TopCornerRight.png', False)
block9 = load_img('assets/images/TopMiddle.png', False)

block10 = load_img('assets/images/Connecter.png', False)
block11 = load_img('assets/images/Connecter2.png', False)
block12 =load_img('assets/images/Connecter3.png', False)
block13 = load_img('assets/images/Connecter4.png', False)

torch_img = load_img("assets/images/torch.png", False)

gold_img = load_img("assets/images/block0.png", False)

bow_img = load_img("assets/images/Bow.png", False)
arrow_img = load_img("assets/images/Arrow.png", False)
bomb_img = load_img("assets/images/Bomb.png", False)
gold_img = load_img("assets/images/Gold.png", False)

skeleton_imgs = [load_img("assets/images/skeleton/Skeleton1.png", True), 
load_img("assets/images/skeleton/Skeleton2.png", True), 
load_img("assets/images/skeleton/Skeleton3.png", True)]
