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
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.cam = cam

    def update(self):
        self.cam.apply(self)


class Stairs(pygame.sprite.Sprite):

    def __init__(self, id, x, y, pose, fl, im, cam, player, all_sprites, *groups):
        super().__init__(all_sprites)
        self.add(groups)
        self.id = id
        self.image = im
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.cam = cam
        self.player = player

    def update(self):
        if self.player.z_pressed and self.player.collide_with(self):
            self.player.floor = 1 if self.player.floor == 2 else 2
        self.cam.apply(self)


class Furniture_that_can_be_opened(pygame.sprite.Sprite):
    def __init__(self, id, x, y, pose, fl, im, cam, player, all_sprites, *groups):
        super().__init__(all_sprites)
        self.add(groups)
        self.id = id
        self.image_closed, self.image_opened = im
        self.image_closed = pygame.transform.rotate(self.image_closed, pose)
        self.image_opened = pygame.transform.rotate(self.image_opened, pose)
        self.image = self.image_closed
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.cam = cam
        self.player = player
        self.opened = False

    def open_close(self):
        self.image = self.image_opened if self.image == self.image_closed else self.image_closed

    def update(self):
        if self.player.z_pressed and self.player.collide_with(self) and not self.opened:
            self.open_close()
        self.cam.apply(self)


class Table(pygame.sprite.Sprite):
    pass


class Chair(pygame.sprite.Sprite):
    pass


class Move_Trigger(pygame.sprite.Sprite):
    def __init__(self, type, mainer, group, x, y, cant_move):
        super().__init__()
        self.add(group)
        size = (1, mainer.image.get_height() - 8) if type == 'vert' else (mainer.image.get_width() - 8, 1)
        self.image = pygame.Surface(size)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.fl = mainer.floor
        self.cant_move_groups = cant_move

    def hide(self):
        self.image.set_alpha(0)

    def show(self):
        self.image.set_alpha(255)

    def can_move(self):
        if any([pygame.sprite.spritecollideany(self, i) for i in self.cant_move_groups[self.fl]]):
            return False
        return True


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, fl, im, all_sprites, group, scr_size, map_size, fps, cam):
        super().__init__(all_sprites)
        self.add(group)
        self.image = im
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = [x, y]
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.scr_width, self.scr_height = scr_size
        self.map_size = map_size
        self.v = 500
        self.fps = fps
        self.cam = cam
        self.move_triggers = {}
        self.z_pressed = False

    def can_move_down(self):
        return self.move_triggers['down'].can_move()

    def can_move_up(self):
        return self.move_triggers['up'].can_move()

    def can_move_right(self):
        return self.move_triggers['right'].can_move()

    def can_move_left(self):
        return self.move_triggers['left'].can_move()

    def update_move_triggers(self):
        self.move_triggers['down'].rect.x = self.rect.x + 4
        self.move_triggers['down'].rect.y = self.rect.y + self.image.get_height() + self.v / self.fps
        self.move_triggers['down'].fl = self.floor
        self.move_triggers['up'].rect.x = self.rect.x + 4
        self.move_triggers['up'].rect.y = self.rect.y - self.v / self.fps + 1
        self.move_triggers['up'].fl = self.floor
        self.move_triggers['right'].rect.x = self.rect.x + self.image.get_width() + self.v / self.fps
        self.move_triggers['right'].rect.y = self.rect.y + 4
        self.move_triggers['right'].fl = self.floor
        self.move_triggers['left'].rect.x = self.rect.x - self.v / self.fps + 1
        self.move_triggers['left'].rect.y = self.rect.y + 4
        self.move_triggers['left'].fl = self.floor

    def collide_with(self, obj):
        if any([pygame.sprite.collide_rect(self.move_triggers[i], obj) for i in self.move_triggers]):
            return True
        return False

    def motion(self, keys):
        if keys[pygame.K_DOWN] and self.can_move_down():
            self.pos[1] += self.v / self.fps
        if keys[pygame.K_UP] and self.can_move_up():
            self.pos[1] -= self.v / self.fps
        if keys[pygame.K_RIGHT] and self.can_move_right():
            self.pos[0] += self.v / self.fps
        if keys[pygame.K_LEFT] and self.can_move_left():
            self.pos[0] -= self.v / self.fps
        if self.scr_width // 2 - self.image.get_width() // 2 <= self.pos[0] <= self.map_size[self.floor][
            0] - self.scr_width // 2 - self.image.get_width() // 2:
            self.cam.update(self, 'ox')
        if self.scr_height // 2 - self.image.get_height() // 2 <= \
                self.pos[1] <= self.map_size[self.floor][1] - self.scr_height // 2 - self.image.get_height() // 2:
            self.cam.update(self, 'oy')

    def deystvie(self, keys):
        for key in keys:
            if key == pygame.K_z:
                self.z_pressed = True

    def update(self, keys, keys_pressed):
        self.z_pressed = False
        self.motion(keys)
        self.deystvie(keys_pressed)
        self.cam.apply(self)
        self.update_move_triggers()


class Camera:
    def __init__(self, scr_size):
        self.scr_width, self.scr_height = scr_size
        self.dx = 0
        self.dy = 0
        self.floor = None

    def apply(self, obj):
        if obj.floor == self.floor:
            obj.rect.x, obj.rect.y = obj.pos  # у каждого объекта есть атрибут pos, где находятся его координаты на карте
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    def pos_on_screen(self, obj):  # возвращает положение объекта на экране
        return (obj.pos[0] + self.dx, obj.pos[1] + self.dy)

    def update(self, target, axis):
        self.floor = target.floor
        if axis == 'ox':
            self.dx = -(target.pos[0] + target.image.get_width() // 2 - self.scr_width // 2)
        elif axis == 'oy':
            self.dy = -(target.pos[1] + target.image.get_height() // 2 - self.scr_height // 2)


def game(screen, size, FPS):
    WIDTH, HEIGHT = size
    map_size = {}
    map_size[1] = (4600, 2400)
    map_size[2] = (3200, 1800)
    clock = pygame.time.Clock()
    # ==============группы_спрайтов=====================================================================================
    all_sprites = pygame.sprite.Group()
    floor_first_floor = pygame.sprite.Group()
    floor_second_floor = pygame.sprite.Group()
    walls_first_floor = pygame.sprite.Group()
    walls_second_floor = pygame.sprite.Group()
    furniture_first_floor = pygame.sprite.Group()
    furniture_second_floor = pygame.sprite.Group()
    stairs_first_floor = pygame.sprite.Group()
    stairs_second_floor = pygame.sprite.Group()
    furniture_that_can_be_opened_first_floor = pygame.sprite.Group()
    furniture_that_can_be_opened_second_floor = pygame.sprite.Group()
    chairs_first_floor = pygame.sprite.Group()
    chairs_second_floor = pygame.sprite.Group()
    tables_first_floor = pygame.sprite.Group()
    tables_second_floor = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    move_triggers = pygame.sprite.Group()
    # ============камера_и_главный_герой================================================================================
    camera = Camera(size)
    player = Player(50, 50, 1, tools.load_image('player.png', -1), all_sprites, player_group, size, map_size, FPS,
                    camera)
    camera.floor = player.floor
    cant_move_groups = {1: [walls_first_floor, furniture_first_floor], 2: [walls_second_floor, furniture_second_floor]}
    player.move_triggers = {
        'left': Move_Trigger('vert', player, move_triggers, player.pos[0] - player.v / player.fps,
                             player.pos[1] + 4, cant_move_groups),
        'up': Move_Trigger('hor', player, move_triggers, player.pos[0] + 4,
                           player.pos[1] - player.v / player.fps,
                           cant_move_groups),
        'right': Move_Trigger('vert', player, move_triggers,
                              player.pos[0] + player.image.get_width() + player.v / player.fps,
                              player.pos[1] + 4,
                              cant_move_groups),
        'down': Move_Trigger('hor', player, move_triggers, player.pos[0] + 4,
                             player.pos[1] + player.image.get_height() + player.v / player.fps, cant_move_groups)}
    # ======заполлнение_карты===========================================================================================
    classes = {'Stairs': Stairs, 'Cupboard': Furniture_that_can_be_opened,
               'Glass_Cupboard': Furniture_that_can_be_opened, 'Shelf': Furniture_that_can_be_opened,
               'Chair': Chair, 'Table': Table}
    images = {'Stairs': tools.load_image('furniture\\stairs.jpg'), 'Cupboard': (
        tools.load_image('furniture\\cupboard.png', -1), tools.load_image('furniture\\cupboard_opened.png', -1))}
    groups = {'Stairs': {1: stairs_first_floor, 2: stairs_second_floor},
              'Cupboard': {1: furniture_that_can_be_opened_first_floor, 2: furniture_that_can_be_opened_second_floor},
              'Glass_Cupboard': {1: furniture_that_can_be_opened_first_floor,
                                 2: furniture_that_can_be_opened_second_floor},
              'Shelf': {1: furniture_that_can_be_opened_first_floor, 2: furniture_that_can_be_opened_second_floor},
              'Chair': {1: chairs_first_floor, 2: chairs_second_floor},
              'Table': {1: tables_first_floor, 2: tables_second_floor}}
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

    for item in map['furniture']:
        id, cl, x, y, pose, fl, unic, im = item
        im = im if im else images[cl]
        group = groups[cl][fl]
        classes[cl](id, x, y, pose, fl, im, camera, player, all_sprites,
                    furniture_first_floor if fl == 1 else furniture_second_floor, group)

    # ==========главный_цикл============================================================================================

    while True:
        keys_pressed = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.KEYDOWN:
                keys_pressed += [event.key]
        keys = pygame.key.get_pressed()

        screen.fill((255, 255, 255))
        player_group.update(keys, keys_pressed)
        if player.floor == 1:
            floor_first_floor.update()
            walls_first_floor.update()
            furniture_first_floor.update()
        elif player.floor == 2:
            floor_second_floor.update()
            walls_second_floor.update()
            furniture_second_floor.update()

        if player.floor == 1:
            floor_first_floor.draw(screen)
            walls_first_floor.draw(screen)
            furniture_first_floor.draw(screen)
        elif player.floor == 2:
            floor_second_floor.draw(screen)
            walls_second_floor.draw(screen)
            furniture_second_floor.draw(screen)
        player_group.draw(screen)
        move_triggers.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1542, 864
    FPS = 60
    screen = pygame.display.set_mode(size)
    game(screen, size, FPS)