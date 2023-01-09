import pygame
import tools


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, fl, im, all_sprites, group, cam):
        super().__init__(all_sprites)
        self.add(group)
        self.image = im
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.cam = cam

    def update(self):
        self.cam.apply(self)


class Wall(pygame.sprite.Sprite):
    height = 30

    def __init__(self, x, y, fl, type, width, all_sprites, group, cam):
        super().__init__(all_sprites)
        self.add(group)
        size = (Wall.height, width) if type == 'vert' else (width, Wall.height)
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.cam = cam

    def update(self):
        self.cam.apply(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, fl, im, all_sprites, group, scr_size, fps, cam):
        super().__init__(all_sprites)
        self.add(group)
        self.image = im
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = [x, y]
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.scr_width, self.scr_height = scr_size
        self.v = 500
        self.fps = fps
        self.cam = cam

    def update(self, keys):
        if keys[pygame.K_DOWN]:
            self.pos[1] += self.v / self.fps
        if keys[pygame.K_UP]:
            self.pos[1] -= self.v / self.fps
        if keys[pygame.K_RIGHT]:
            self.pos[0] += self.v / self.fps
        if keys[pygame.K_LEFT]:
            self.pos[0] -= self.v / self.fps

        self.rect.x, self.rect.y = self.pos


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x, obj.rect.y = obj.pos  # у каждого объекта есть атрибут pos, где находятся его координаты на карте
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def pos_on_screen(self, obj):  # возвращает положение объекта на экране
        return (obj.pos[0] + self.dx, obj.pos[1] + self.dy)

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def game(screen, size, FPS):
    WIDTH, HEIGHT = size
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    floor_first_floor = pygame.sprite.Group()
    floor_second_floor = pygame.sprite.Group()
    walls_first_floor = pygame.sprite.Group()
    walls_second_floor = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    camera = Camera()
    player = Player(50, 50, 1, tools.load_image('player.png', -1), all_sprites, player_group, size, FPS, camera)
    map = tools.load_map()
    for floor in map['floor']:
        id, x, y, fl, width, height, image = floor
        image = tools.load_image('furniture\\' + image)
        for x_pos in range(x, width, image.get_width()):
            for y_pos in range(y, height, image.get_height()):
                Floor(x_pos, y_pos, fl, image, all_sprites,
                      floor_first_floor if fl == 1 else floor_second_floor, camera)
    for wall in map['walls']:
        id, x, y, fl, type, width = wall
        Wall(x, y, fl, type, width, all_sprites, walls_first_floor if fl == 1 else walls_second_floor, camera)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                tools.terminate()
        keys = pygame.key.get_pressed()

        screen.fill((0, 0, 0))
        floor_first_floor.update()
        walls_first_floor.update()
        player_group.update(keys)

        floor_first_floor.draw(screen)
        walls_first_floor.draw(screen)
        player_group.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1600, 900
    FPS = 60
    screen = pygame.display.set_mode(size)
    game(screen, size, FPS)
