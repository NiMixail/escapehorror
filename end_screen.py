import pygame

from tools import load_image, terminate, Audio
from start_screen import start_screen

au = Audio()


def play(a, b):
    print(a + b)


def continue_play(a, b):
    print(a, b)


def can_continue():
    with open('data/continue.txt', 'r', encoding='UTF-8') as f:
        text = f.read()
    if text[0] == ',':
        return False
    return True


class Background(pygame.sprite.Sprite):
    def __init__(self, im, all_sprites, group):
        super().__init__(all_sprites)
        self.add(group)
        self.image = im
        self.rect = self.image.get_rect()


def end_screen(screen, size, FPS, type):
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    backgroundes = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    background_im = load_image('start_screen/bg_lose.png' if type == 'lose' else 'start_screen/bg_win.png')
    Background(background_im, all_sprites, backgroundes)

    pygame.mouse.set_visible(True)

    au.eff('screamer' if type == 'lose' else 'win').play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                start_screen(screen, size, FPS, play, ['1', '2'], continue_play, ['1', '2'])
            buttons.update(event)
        screen.fill((0, 0, 0))
        buttons.update()
        backgroundes.draw(screen)
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('end screen')
    FPS = 60
    end_screen(screen, size, FPS, 'win')
