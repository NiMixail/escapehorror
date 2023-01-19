import pygame
from tools import load_image, terminate, Audio

au = Audio()


class Ball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, napr, v, FPS, all_sprites, group):
        super().__init__(all_sprites)
        self.add(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x, self.napr, self.v, self.fps = self.rect.x, napr, v, FPS

    def update(self):
        self.x += self.napr * self.v / self.fps
        self.rect.x = int(self.x)


def part_1(screen, size, FPS):
    WIDTH, HEIGHT = size
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    balls = pygame.sprite.Group()

    im_1, im_2 = load_image('start_cutscene/picture_1.png', -1), load_image('start_cutscene/picture_2.png', -1)
    font = pygame.font.Font(None, 30)
    alpha = 0
    alpha_moving = 5
    font_sur = font.render("PRESENTS", True, (0, 0, 0))
    font_sur.set_alpha(alpha)

    diam = 200
    b1 = Ball(im_1, 0, HEIGHT // 2 - diam // 2, 1, WIDTH // 2 - diam, FPS, all_sprites, balls)
    b2 = Ball(im_2, WIDTH - diam, HEIGHT // 2 - diam // 2, -1, WIDTH // 2 - diam, FPS, all_sprites, balls)
    text = False

    au.eff('mixser').play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        screen.fill((255, 255, 255))
        if not text:
            balls.update()
            if pygame.sprite.collide_rect(b1, b2):
                text = True
        else:
            alpha += alpha_moving
            font_sur.set_alpha(alpha)
            screen.blit(font_sur,
                        (WIDTH // 2 - font_sur.get_width() // 2,
                         HEIGHT // 2 - font_sur.get_height() // 2 + diam // 2 + 10))
            if alpha >= 500:
                alpha_moving *= -1
            elif alpha <= 0 and alpha_moving < -1:
                return
        balls.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class Background(pygame.sprite.Sprite):
    def __init__(self, image, all_sprites, group):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.add(group)


class Pencil(pygame.sprite.Sprite):
    def __init__(self, image, points, v, fps, screen, all_sprites, group):
        super().__init__(all_sprites)
        self.add(group)
        self.points = points
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.points[0][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.cur_letter, self.cur_point = 0, 1
        self.last_point = None
        self.v = v
        self.fps = fps
        self.screen = screen
        self.drawed_lines = []

    def update(self):
        if self.cur_letter < len(self.points):
            x, y = self.points[self.cur_letter][self.cur_point]
            if abs(x - self.rect.x) < self.v / self.fps:
                self.rect.x = x
            else:
                self.rect.x += (self.v / self.fps) * (1 if self.rect.x < x else -1)
            if abs(y - self.rect.y) < self.v / self.fps:
                self.rect.y = y
            else:
                self.rect.y += (self.v / self.fps) * (1 if self.rect.y < y else -1)
            if self.last_point:
                self.drawed_lines += [(self.last_point, (self.rect.x, self.rect.y))]
            for i in self.drawed_lines:
                pygame.draw.line(self.screen, (67, 67, 67), i[0], i[1], 5)
            self.last_point = (self.rect.x, self.rect.y)
            if self.rect.x == x and self.rect.y == y:
                self.cur_point += 1
            if self.cur_point == len(self.points[self.cur_letter]):
                self.cur_letter += 1
                self.cur_point = 0
                if self.cur_letter < len(self.points):
                    self.rect.x, self.rect.y = self.points[self.cur_letter][0]
                self.last_point = None


def part_2(screen, size, FPS):
    WIDTH, HEIGHT = size
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    backgroundes = pygame.sprite.Group()
    penciles = pygame.sprite.Group()

    backgr_im, pencil_im = load_image('start_cutscene/background.png'), load_image('start_cutscene/pencil.png', -1)
    background = Background(backgr_im, all_sprites, backgroundes)
    points = [
        [(174, 206), (153, 202), (139, 209), (125, 230), (131, 251), (145, 260), (161, 258), (165, 252), (170, 223),
         (173, 217), (172, 190), (172, 170), (174, 141), (174, 115), (173, 116), (173, 132), (173, 149), (173, 165),
         (174, 181), (176, 198), (177, 215), (180, 228), (185, 245), (192, 257), (198, 262), (206, 263)],
        [(219, 189), (219, 197), (220, 208), (221, 220), (221, 228), (222, 234), (222, 246), (222, 259), (222, 262)],
        [(221, 206), (223, 201), (228, 194), (236, 191), (248, 190), (253, 192), (256, 197)],
        [(297, 196), (288, 194), (282, 197), (276, 204), (272, 215), (271, 226), (273, 237), (279, 250), (289, 258),
         (296, 257), (299, 250), (302, 237), (304, 225), (306, 207), (306, 196), (306, 197), (306, 210), (309, 229),
         (311, 238), (313, 246), (318, 253), (321, 254)],
        [(337, 193), (338, 199), (342, 212), (345, 222), (351, 235), (355, 241), (357, 245), (358, 246), (360, 242),
         (366, 229), (371, 218), (379, 198), (379, 198), (383, 211), (388, 223), (392, 233), (396, 241), (398, 243),
         (401, 239), (408, 230), (412, 221), (416, 206), (419, 198)],
        [(439, 191), (440, 200), (441, 212), (442, 223), (443, 233), (443, 241), (443, 249), (444, 252)],
        [(441, 198), (452, 196), (457, 198), (465, 204), (469, 216), (470, 223), (471, 231), (474, 238), (478, 243),
         (480, 244)],
        [(558, 221), (577, 216), (583, 213), (601, 194), (607, 181), (609, 158), (598, 138), (588, 137), (584, 143),
         (582, 153), (582, 166), (581, 178), (578, 190), (578, 201), (578, 212), (579, 229), (579, 239), (586, 253),
         (597, 259), (608, 263), (619, 254), (627, 242), (618, 219), (601, 206), (586, 209)],
        [(655, 201), (659, 215), (663, 226), (667, 237), (675, 247), (683, 251), (688, 250), (692, 242), (696, 231),
         (699, 220), (700, 206), (698, 197), (698, 206), (700, 217), (703, 228), (704, 242), (708, 253), (712, 269),
         (712, 281), (712, 296), (709, 316), (699, 331), (676, 340), (664, 337), (652, 328), (654, 313), (666, 297),
         (680, 287), (687, 283), (704, 275), (730, 260), (738, 254), (750, 246), (753, 243)],
        [(190, 452), (186, 461), (185, 481), (186, 494), (188, 508), (189, 519), (190, 526), (191, 539), (192, 548),
         (193, 559), (194, 570), (195, 581)],
        [(194, 450), (194, 463), (197, 475), (208, 493), (215, 505), (220, 512), (221, 512), (226, 507), (237, 496),
         (245, 485), (254, 470), (262, 456), (263, 456), (264, 467), (264, 483), (265, 498), (266, 513), (267, 528),
         (268, 537), (270, 551), (271, 559), (271, 568), (272, 572)],
        [(300, 525), (300, 529), (302, 539), (302, 547), (303, 555), (304, 561), (304, 569)], [(302, 497)],
        [(382, 514), (376, 521), (371, 528), (368, 533), (364, 541), (360, 547), (354, 555), (347, 566), (347, 567),
         (343, 570)],
        [(335, 513), (338, 519), (345, 529), (353, 538), (358, 545), (365, 552), (371, 559), (376, 566), (378, 567)],
        [(447, 521), (444, 515), (434, 513), (425, 513), (418, 516), (412, 522), (409, 527), (408, 538), (407, 551),
         (407, 556), (415, 561), (427, 564), (429, 560), (434, 552), (440, 540), (441, 530), (444, 514), (444, 505),
         (444, 513), (444, 523), (444, 543), (447, 548), (460, 558), (466, 561)],
        [(486, 509), (487, 517), (488, 529), (490, 538), (491, 543), (491, 560), (491, 562)], [(484, 490)],
        [(518, 450), (517, 458), (517, 472), (518, 482), (518, 493), (518, 502), (518, 515), (518, 526), (519, 532),
         (520, 540), (520, 548), (524, 553), (529, 558), (530, 558)],
        [(659, 432), (655, 455), (655, 464), (656, 485), (655, 494), (655, 501), (654, 516), (654, 528), (653, 543),
         (653, 553), (652, 560)],
        [(656, 440), (663, 454), (668, 469), (675, 485), (681, 495), (686, 504), (690, 516), (697, 530), (703, 544),
         (711, 559), (711, 559), (713, 548), (713, 537), (715, 518), (717, 499), (720, 480), (724, 460), (725, 448),
         (727, 437), (729, 431)], [(758, 508), (758, 517), (759, 531), (759, 539), (760, 552)], [(761, 478)],
        [(801, 428), (800, 443), (800, 453), (798, 464), (797, 477), (796, 491), (796, 504), (796, 516), (796, 527),
         (796, 538), (796, 550)], [(826, 487), (822, 492), (815, 500), (808, 509), (806, 512)],
        [(805, 513), (810, 519), (816, 526), (820, 534), (823, 541), (825, 544)],
        [(860, 494), (860, 502), (861, 515), (861, 525), (861, 534), (861, 550)], [(858, 467)],
        [(890, 429), (890, 443), (889, 462), (888, 477), (889, 488), (890, 505), (892, 518), (899, 531), (905, 537),
         (914, 537), (924, 530)], [(883, 493), (893, 493), (901, 494), (910, 496)],
        [(947, 493), (951, 507), (952, 514), (953, 526), (955, 539), (955, 544)], [(955, 461)],
        [(991, 485), (992, 493), (993, 504), (993, 519), (993, 528), (995, 538), (995, 549)],
        [(997, 486), (1009, 486), (1018, 492), (1025, 502), (1026, 507), (1028, 518), (1032, 528), (1034, 534),
         (1038, 536), (1042, 537)]]
    pencil = Pencil(pencil_im, points, 3000, FPS, screen, all_sprites, penciles)

    au.eff('mixser').stop()
    au.eff('pencil').play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        screen.fill((0, 0, 0))
        backgroundes.draw(screen)
        penciles.update()
        penciles.draw(screen)
        if pencil.cur_letter == len(points):
            print(1)
            font = pygame.font.Font(None, 68)
            font_sur = font.render("and Stable Diffusion image generating AI", True, (50, 50, 50))
            screen.blit(font_sur,
                        (WIDTH // 2 - font_sur.get_width() // 2,
                         HEIGHT // 12 * 11 - font_sur.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            return
        pygame.display.flip()
        clock.tick(FPS * 1.5)


def part_3(screen, size, FPS):
    WIDTH, HEIGHT = size
    alpha = 0
    alpha_moving = 4
    font = pygame.font.Font(None, 68)
    font_sur = font.render("SCARY SMILE", True, (255, 0, 0))
    font_sur.set_alpha(alpha)

    au.eff('pencil').stop()
    au.eff('fortepiano_strike').set_volume(500)
    au.eff('fortepiano_strike').play()

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                au.eff('fortepiano_strike').stop()
                return
        screen.fill((0, 0, 0))
        alpha += alpha_moving
        font_sur.set_alpha(alpha)
        screen.blit(font_sur,
                    (WIDTH // 2 - font_sur.get_width() // 2,
                     HEIGHT // 2 - font_sur.get_height() // 2))
        if alpha >= 800:
            alpha_moving *= -1
        elif alpha <= 0 and alpha_moving < -1:
            return
        pygame.display.flip()
        clock.tick(FPS // 2)


def start_cutscene(screen, size, FPS):
    pygame.mouse.set_visible(False)
    part_1(screen, size, FPS)
    part_2(screen, size, FPS)
    part_3(screen, size, FPS)
    pygame.mouse.set_visible(True)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('стартовая катсцена')
    FPS = 60
    start_cutscene(screen, size, FPS)
