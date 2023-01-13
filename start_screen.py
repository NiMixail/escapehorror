import pygame

from tools import load_image, terminate
from sounds import Audio

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


class Button(pygame.sprite.Sprite):
    def __init__(self, im, all_sprites, group, x, y, can_be_pressed, func, *args):
        super().__init__(all_sprites)
        self.add(group)
        self.first_im = im
        self.first_x, self.first_y = x, y
        self.image = im
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.can_be_pressed = can_be_pressed
        self.func = func
        self.func_args = args
        self.is_current = False
        self.mouse_was_pressed = False

    def update(self, *args):
        for event in args:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.x <= event.pos[0] <= self.rect.x + self.image.get_width() and self.rect.y <= \
                        event.pos[1] <= self.rect.y + self.image.get_height():
                    if not self.is_current and self.can_be_pressed():
                        self.is_current = True
                        au.eff('click').play()
                else:
                    self.is_current = False
        if not self.can_be_pressed():
            self.image = self.first_im.set_alpha(123)
        else:
            self.image = self.first_im
        if self.is_current and self.can_be_pressed():
            x, y = self.first_x + self.first_im.get_width() // 2, self.first_y + self.first_im.get_height() // 2
            self.image = pygame.transform.scale(self.image,
                                                (int(1.4 * self.first_im.get_width()),
                                                 int(1.4 * self.first_im.get_height())))
            self.rect.x, self.rect.y = x - self.image.get_width() // 2, y - self.image.get_height() // 2
        else:
            self.image = self.first_im
            self.rect.x, self.rect.y = self.first_x, self.first_y


def start_screen(screen, size, FPS, play, play_args, continue_play, continue_play_args):
    WIDTH, HEIGHT = size
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    backgroundes = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    windows = []
    background_im, pl_b_im, cont_pl_b_im, ex_b_im = load_image('start_screen/background.png'), \
                                                    load_image('start_screen/play_button.png', -1), load_image(
        'start_screen/continue_button.png', -1), \
                                                    load_image('start_screen/exit_button.png', -1)
    Background(background_im, all_sprites, backgroundes)
    interval = 5
    play_button = Button(pl_b_im, all_sprites, buttons, WIDTH // 2 - pl_b_im.get_width() // 2,
                         HEIGHT // 2 - pl_b_im.get_height() - interval,
                         lambda: True if len(windows) == 0 else False, play, *play_args)
    continue_button = Button(cont_pl_b_im, all_sprites, buttons, WIDTH // 2 - cont_pl_b_im.get_width() // 2,
                             HEIGHT // 2,
                             lambda: True if len(windows) == 0 and can_continue() else False,
                             continue_play, *continue_play_args)
    exit_button = Button(ex_b_im, all_sprites, buttons, WIDTH // 2 - ex_b_im.get_width() // 2,
                         HEIGHT // 2 + cont_pl_b_im.get_height() +
                         interval, lambda: True, terminate)
    buttons_list = [play_button, continue_button, exit_button]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons_list:
                    if button.is_current and button.can_be_pressed():
                        screen.fill((0, 0, 0))
                        clock.tick(5)
                        return button.func(*button.func_args)
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
    pygame.display.set_caption('стартовый экран')
    FPS = 60
    start_screen(screen, size, FPS, play, ['1', '2'], continue_play, ['1', '2'])
