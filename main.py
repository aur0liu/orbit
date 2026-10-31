import json
import pygame

from main_menu import *
from new_sim import *

#config:

#initialise pygame
pygame.init()
pygame.font.init()

#create window
pygame.display.set_caption("ORBIT")
display = (1280, 720)
window = pygame.display.set_mode(display)

#create clock object
fps = 60
clock = pygame.time.Clock()


main_menu(window, fps, clock)




            