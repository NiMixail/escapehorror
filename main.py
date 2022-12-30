import pygame
from tools import load_image, terminate
from start_cutscene import start_cutscene

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Scary smile')
    FPS = 60
    start_cutscene()
