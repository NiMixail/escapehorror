import pygame
import tools
import random
import math


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

    def __init__(self, id, x, y, pose, fl, im, im_cur, cam, player, all_sprites, *groups):
        super().__init__(all_sprites)
        self.add(groups)
        self.id = id
        self.image_normal = im
        self.image = self.image_normal
        self.cur_color = pygame.Color('yellow')
        self.cur_rect = (0, 0, self.image.get_width(), self.image.get_height())
        im_cur = self.image.copy()
        pygame.draw.rect(im_cur, self.cur_color, self.cur_rect, 1)
        self.image_current = im_cur
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.cam = cam
        self.player = player

    def current_image_change(self):
        if self.player.current_object == self:
            self.image = self.image_current
        else:
            self.image = self.image_normal

    def update(self):
        self.current_image_change()
        if self.player.can_use(self) and self.player.z_pressed:
            self.player.floor = 1 if self.player.floor == 2 else 2
        self.cam.apply(self)


class Furniture_that_can_be_opened(pygame.sprite.Sprite):
    def __init__(self, id, x, y, pose, fl, im, im_cur, cam, player, all_sprites, *groups):
        super().__init__(all_sprites)
        self.add(groups)
        self.id = id
        self.image_closed, self.image_opened = im
        if pose:
            self.image_closed = pygame.transform.rotate(self.image_closed, pose)
            self.image_opened = pygame.transform.rotate(self.image_opened, pose)
        self.image = self.image_closed
        self.cur_color = pygame.Color('yellow')
        self.cur_rect = (0, 0, self.image.get_width(), self.image.get_height())
        image_current_opened = self.image_opened.copy()
        pygame.draw.rect(image_current_opened, self.cur_color, self.cur_rect, 1)
        self.image_current_opened = image_current_opened
        image_current_closed = self.image_closed.copy()
        pygame.draw.rect(image_current_closed, self.cur_color, self.cur_rect, 1)
        self.image_current_closed = image_current_closed
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.cam = cam
        self.player = player
        self.item = None
        self.image_with_item = None
        self.image_current_with_item = None
        self.status = 'closed'

    def set_image_with_item(self):
        image_opened = self.image_opened.copy()
        image_opened.blit(self.item.image, (
            image_opened.get_width() // 2 - self.item.image.get_width() // 2,
            image_opened.get_height() // 2 - self.item.image.get_height() // 2))
        self.image_with_item = image_opened
        image_current_with_item = image_opened.copy()
        rect = (self.image_opened.get_width() // 2 - self.item.image.get_width() // 2,
                image_opened.get_height() // 2 - self.item.image.get_height() // 2, self.item.image.get_width(),
                self.item.image.get_height())
        pygame.draw.rect(image_current_with_item, self.cur_color, rect, 1)
        self.image_current_with_item = image_current_with_item

    def func(self):
        if self.status == 'closed':
            self.image = self.image_opened
            self.status = 'opened'
            if self.item:
                self.image = self.image_with_item
                self.status = 'opened_with_item'
        elif self.item:
            self.player.items += [self.item]
            self.item = None
            self.image = self.image_opened
            self.status = 'opened'
        else:
            self.image = self.image_closed
            self.status = 'closed'

    def current_image_change(self):
        if self.player.current_object == self:
            if self.status == 'closed':
                self.image = self.image_current_closed
            elif self.status == 'opened_with_item':
                self.image = self.image_current_with_item
            elif self.status == 'opened':
                self.image = self.image_current_opened
        else:
            if self.status == 'closed':
                self.image = self.image_closed
            elif self.status == 'opened':
                self.image = self.image_opened
            elif self.status == 'opened_with_item':
                self.image = self.image_with_item

    def update(self):
        self.current_image_change()
        if self.player.current_object == self and self.player.z_pressed:
            self.func()
        self.cam.apply(self)


class Furniture_you_can_hide(pygame.sprite.Sprite):
    def __init__(self, id, x, y, pose, fl, im, im_cur, cam, player, all_sprites, *groups):
        super().__init__(all_sprites)
        self.add(groups)
        self.id = id
        self.image_normal = im
        self.image_current = im_cur
        self.image = self.image_normal
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.pos = x, y
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.cam = cam
        self.player = player

    def current_image_change(self):
        if self.player.current_object == self:
            self.image = self.image_current
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.image = self.image_normal
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_image_change()
        if self.player.current_object == self and self.player.z_pressed:
            self.player.is_hidden = True if not self.player.is_hidden else False
        self.cam.apply(self)


class Door(pygame.sprite.Sprite):
    def __init__(self, id, x, y, pose, fl, im, im_cur, cam, player, all_sprites, *groups):
        super().__init__(all_sprites)
        self.add(groups)
        self.id = id
        self.image_closed, self.image_opened = im
        self.dx, self.dy = 0, 0
        if pose:
            self.image_opened = pygame.transform.rotate(self.image_opened, pose)
            self.image_closed = pygame.transform.rotate(self.image_closed, pose)
        self.pose = pose
        self.image = self.image_closed
        self.centre = (x + self.image.get_width() // 2, y + self.image.get_height() // 2)
        self.rect = self.image.get_rect()
        self.pos = [x, y]
        self.rect.x, self.rect.y = self.pos
        self.floor = fl
        self.cam = cam
        self.player = player

    def open_close(self):
        player_centre = (self.player.pos[0] + self.player.image.get_width() // 2,
                         self.player.pos[1] + self.player.image.get_height() // 2)
        if math.sqrt((player_centre[0] - self.centre[0]) ** 2 + (player_centre[1] - self.centre[1]) ** 2) <= int(
                self.player.image.get_width() * 1.5):
            self.image = self.image_opened
            if self.pose == 180:
                self.dy = self.image_closed.get_height() - self.image_opened.get_height()
            elif self.pose == 270:
                self.dx = self.image_closed.get_width() - self.image_opened.get_width()
        else:
            self.image = self.image_closed
            self.dx, self.dy = 0, 0

    def update(self):
        self.open_close()
        self.cam.apply(self)
        self.rect.x += self.dx
        self.rect.y += self.dy


class Door_locked(pygame.sprite.Sprite):
    def __init__(self, id, x, y, pose, fl, im, door_args, color, cam, player, all_sprites, *groups):
        super().__init__(all_sprites)
        self.add(groups)
        self.id = id
        self.image_normal = im

        if pose:
            self.image_normal = pygame.transform.rotate(self.image_normal, pose)
        self.pose = pose
        cur_color = pygame.Color('yellow')
        cur_rect = (0, 0, self.image_normal.get_width(), self.image_normal.get_height())
        im_cur = self.image_normal.copy()
        pygame.draw.rect(im_cur, cur_color, cur_rect, 1)
        self.image_current = im_cur
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.pos = self.rect.x, self.rect.y = x, y
        self.floor = fl
        self.cam = cam
        self.player = player
        self.color = color
        self.door_args = door_args

    def current_image_change(self):
        if self.player.current_object == self:
            self.image = self.image_current
        else:
            self.image = self.image_normal

    def func(self):
        i_key, i_hammer = -1, -1
        for i in range(len(self.player.items)):
            if self.player.items[i].name == self.color + '_key':
                i_key = i
            elif self.player.items[i].name == 'hammer':
                i_hammer = i
        if i_key != -1:
            del self.player.items[i_key]
        else:
            del self.player.items[i_hammer]
        self.kill()
        images, all_sprites, group = self.door_args
        group = group[self.floor]
        Door(self.id, self.pos[0], self.pos[1], self.pose, self.floor, images, None, self.cam, self.player, all_sprites,
             group)

    def update(self):
        self.current_image_change()
        pl_items_names = [i.name for i in self.player.items]
        if self.player.current_object == self and self.player.z_pressed and any(
                [i in pl_items_names for i in ['hammer', self.color + '_key']]):
            self.func()
        self.cam.apply(self)


class Waste(pygame.sprite.Sprite):
    def __init__(self, id, x, y, pose, fl, im, im_cur, cam, player, all_sprites, *groups):
        super().__init__(all_sprites)
        self.add(groups)
        self.id = id
        self.image = im
        if pose:
            self.image = pygame.transform.rotate(self.image, pose)
        self.rect = self.image.get_rect()
        self.pos = self.rect.x, self.rect.y = x, y
        self.floor = fl
        self.cam = cam
        self.player = player

    def update(self):
        self.cam.apply(self)


class Item(pygame.sprite.Sprite):
    def __init__(self, name, image, all_sprites, group):
        super().__init__(all_sprites)
        self.add(group)
        self.image = image
        self.name = name


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


class Interaction_Trigger(pygame.sprite.Sprite):
    def __init__(self, mainer, group, x, y):
        super().__init__()
        self.add(group)
        self.image = pygame.Surface((mainer.image.get_width() * 2, mainer.image.get_height() * 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.image.fill((255, 255, 255))
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.fl = mainer.floor

    def hide(self):
        self.image.set_alpha(0)

    def show(self):
        self.image.set_alpha(100)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, fl, im, all_sprites, group, scr_size, map_size, fps, cam, screen, furn_group):
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
        self.screen = screen
        self.move_triggers = {}
        self.interaction_trigger = None
        self.z_pressed = False
        self.items = []
        self.current_object = None
        self.is_hidden = False
        self.furn_group = furn_group

    def can_move_down(self):
        return self.move_triggers['down'].can_move() and not self.is_hidden

    def can_move_up(self):
        return self.move_triggers['up'].can_move() and not self.is_hidden

    def can_move_right(self):
        return self.move_triggers['right'].can_move() and not self.is_hidden

    def can_move_left(self):
        return self.move_triggers['left'].can_move() and not self.is_hidden

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

    def update_interaction_trigger(self):
        self.interaction_trigger.rect.x = self.rect.x - self.image.get_width() // 2
        self.interaction_trigger.rect.y = self.rect.y - self.image.get_height() // 2
        self.interaction_trigger.fl = self.floor

    def can_use(self, obj):
        if pygame.sprite.collide_rect(self.interaction_trigger, obj):
            return True
        return False

    def current_check(self):
        spr_list = pygame.sprite.spritecollide(self.interaction_trigger, self.furn_group[self.floor], False)
        if len(spr_list) == 0:
            self.current_object = None
            return
        centre = (self.pos[0] + self.image.get_width() // 2, self.pos[1] + self.image.get_height() // 2)
        spr_dict = {}
        for obj in spr_list:
            obj_centre = (obj.pos[0] + obj.image.get_width() // 2, obj.pos[1] + obj.image.get_height() // 2)
            dist = math.sqrt((centre[0] - obj_centre[0]) ** 2 + (centre[1] - obj_centre[1]) ** 2)
            spr_dict[dist] = obj
        self.current_object = spr_dict[min(spr_dict)]

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
                if self.is_hidden and self.current_object.__class__ != Furniture_you_can_hide:
                    self.is_hidden = False
                self.z_pressed = True

    def is_hidden_image_change(self):
        if self.is_hidden:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

    def draw_inventar(self):
        if len(self.items) > 0:
            x_pos = self.scr_width - max([i.image.get_width() for i in self.items]) - 10
            y_pos = 10
            y_interval = max([i.image.get_height() for i in self.items]) + 5
            for item in self.items:
                self.screen.blit(item.image, (x_pos, y_pos))
                y_pos += y_interval

    def update(self, keys, keys_pressed):
        self.z_pressed = False
        self.motion(keys)
        self.current_check()
        self.deystvie(keys_pressed)
        self.is_hidden_image_change()
        self.cam.apply(self)
        self.update_move_triggers()
        self.update_interaction_trigger()


class Monster(pygame.sprite.Sprite):
    def __init__(self, im, x, y, fl, all_sprites, group, cam):
        super().__init__(all_sprites)
        self.add(group)
        self.image = im
        self.rect = self.image.get_rect()
        self.pos = self.rect.x, self.rect.y = x, y
        self.floor = fl
        self.cam = cam

    def update(self):
        self.cam.apply(self)


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
    pygame.mouse.set_visible(False)
    # ==============группы_спрайтов=====================================================================================
    all_sprites = pygame.sprite.Group()

    floor_first_floor = pygame.sprite.Group()
    floor_second_floor = pygame.sprite.Group()
    walls_first_floor = pygame.sprite.Group()
    walls_second_floor = pygame.sprite.Group()

    furniture_first_floor = pygame.sprite.Group()
    furniture_second_floor = pygame.sprite.Group()
    doors_first_floor = pygame.sprite.Group()
    doors_second_floor = pygame.sprite.Group()
    waste_first_floor = pygame.sprite.Group()
    waste_second_floor = pygame.sprite.Group()

    items = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    move_triggers = pygame.sprite.Group()
    interaction_triggers = pygame.sprite.Group()
    # ============камера_и_главный_герой================================================================================
    camera = Camera(size)
    player = Player(50, 50, 1, tools.load_image('player.png', -1), all_sprites, player_group, size, map_size, FPS,
                    camera, screen, {1: furniture_first_floor, 2: furniture_second_floor})
    camera.floor = player.floor
    cant_move_groups = {1: [walls_first_floor, furniture_first_floor, waste_first_floor],
                        2: [walls_second_floor, furniture_second_floor, waste_second_floor]}
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
    player.interaction_trigger = Interaction_Trigger(player, interaction_triggers,
                                                     player.pos[0] - player.image.get_width() // 2,
                                                     player.pos[1] - player.image.get_height() // 2)
    # ======заполлнение_карты===========================================================================================
    classes = {'Stairs': Stairs, 'Cupboard': Furniture_that_can_be_opened,
               'Glass_Cupboard': Furniture_that_can_be_opened, 'Shelf': Furniture_that_can_be_opened,
               'Kitchen_Cupboard': Furniture_that_can_be_opened, 'Can_hide': Furniture_you_can_hide, 'Door': Door}
    images = {'Stairs': tools.load_image('furniture\\stairs.jpg'), 'Cupboard': (
        tools.load_image('furniture\\cupboard.png', -1), tools.load_image('furniture\\cupboard_opened.png', -1)),
              'Door': (
                  tools.load_image('furniture\\door_closed.png'), tools.load_image('furniture\\door_opened.png', -1))}
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
    furniture_that_can_have_item = []
    for i in map['furniture']:
        id, cl, x, y, pose, fl, im, im_cur = i
        im = tools.load_image('furniture\\' + im, -1) if im else images[cl]
        im_cur = tools.load_image('furniture\\' + im_cur, -1) if im_cur else None
        if cl != 'Door' and cl in classes:
            self_groups = furniture_first_floor if fl == 1 else furniture_second_floor
        elif cl == 'Door':
            self_groups = doors_first_floor if fl == 1 else doors_second_floor
        else:
            self_groups = waste_first_floor if fl == 1 else waste_second_floor
        furn = classes.get(cl, Waste)(id, x, y, pose, fl, im, im_cur, camera, player, all_sprites,
                                      self_groups)
        if classes.get(cl, None) == Furniture_that_can_be_opened:
            furniture_that_can_have_item += [furn]
    door_args = [images['Door'], all_sprites, {1: doors_first_floor, 2: doors_second_floor}]
    Door_locked(993, 1500, 1500, None, 1, tools.load_image('furniture\\door_locked_red.png'), door_args, 'red',
                camera, player, all_sprites, furniture_first_floor, furniture_first_floor)
    Door_locked(994, 1500, 1650, 180, 1, tools.load_image('furniture\\door_locked_blue.png'), door_args, 'blue',
                camera, player, all_sprites, furniture_first_floor, furniture_first_floor)
    Door_locked(995, 1500, 1800, 270, 1, tools.load_image('furniture\\door_locked_green.png'), door_args, 'green',
                camera, player, all_sprites, furniture_first_floor, furniture_first_floor)
    # ===============предметы===========================================================================================
    hammer = Item('hammer', tools.load_image('items\\hammer.png', -1), all_sprites, items)
    red_key = Item('red_key', tools.load_image('items\\red_key.png', -1), all_sprites, items)
    blue_key = Item('blue_key', tools.load_image('items\\blue_key.png', -1), all_sprites, items)
    green_key = Item('green_key', tools.load_image('items\\green_key.png', -1), all_sprites, items)
    hammer_mainer, red_key_mainer, blue_key_mainer, green_key_mainer = random.sample(furniture_that_can_have_item, 4)
    hammer_mainer.item = hammer
    hammer_mainer.set_image_with_item()
    red_key_mainer.item = red_key
    red_key_mainer.set_image_with_item()
    blue_key_mainer.item = blue_key
    blue_key_mainer.set_image_with_item()
    green_key_mainer.item = green_key
    green_key_mainer.set_image_with_item()
    # ==========главный_цикл============================================================================================

    while True:
        keys_pressed = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mouse.set_visible(True)
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
            doors_first_floor.update()
            waste_first_floor.update()
        elif player.floor == 2:
            floor_second_floor.update()
            walls_second_floor.update()
            furniture_second_floor.update()
            doors_second_floor.update()
            waste_second_floor.update()

        if player.floor == 1:
            floor_first_floor.draw(screen)
            walls_first_floor.draw(screen)
            furniture_first_floor.draw(screen)
            doors_first_floor.draw(screen)
            waste_first_floor.draw(screen)
        elif player.floor == 2:
            floor_second_floor.draw(screen)
            walls_second_floor.draw(screen)
            furniture_second_floor.draw(screen)
            doors_second_floor.draw(screen)
            waste_second_floor.draw(screen)
        player_group.draw(screen)
        move_triggers.draw(screen)
        interaction_triggers.draw(screen)
        player.draw_inventar()

        clock.tick(FPS)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1542, 864
    FPS = 120
    screen = pygame.display.set_mode(size)
    game(screen, size, FPS)
