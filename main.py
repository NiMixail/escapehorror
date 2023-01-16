import pygame
import tkinter
from start_cutscene import start_cutscene
from start_screen import start_screen
from game import game

root = tkinter.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Scary smile')
    FPS = 120
    start_cutscene(screen, size, FPS)
    while True:
        start_screen(screen, size, FPS, game, [screen, size, FPS], game, [screen, size, FPS, True])
