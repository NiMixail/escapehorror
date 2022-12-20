import sys
import os
import pygame
from tools import load_image, terminate

all_sprites = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(all_sprites)
        self.image = load_image(image, -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


def part_1(screen, size, FPS):
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((255, 255, 255))
        pygame.display.flip()
        clock.tick(FPS)


def part_2(screen, size, FPS):
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((255, 255, 255))
        pygame.display.flip()
        clock.tick(FPS)


def start_cutscene(screen, size, FPS):
    part_1(screen, size, FPS)
    part_2(screen, size, FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('стартовая катсцена')
    FPS = 60
    start_cutscene(screen, size, FPS)
