import pygame
import tkinter
from start_cutscene import start_cutscene
from start_screen import start_screen
from game import game

root = tkinter.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()


def game_test(a, b):
    print(a + b)


def continue_test(a, b):
    print(a - b)


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Scary smile')
    FPS = 120
    start_cutscene(screen, size, FPS)
    while True:
        start_screen(screen, size, FPS, game, [screen, size, FPS], continue_test, [1, 2])
        # start_screen(screen, size, FPS, game, game_args, continue, continue_args), где:
        #     game - функция самого процесса игры; game_args - её аргументы
        #     continue - функция процесса сохранённой игры; сontinue_args - её аргументы
        # game_test, continue_test - пробные функции, созданные чтобы проверить работоспособность стартового экрана
