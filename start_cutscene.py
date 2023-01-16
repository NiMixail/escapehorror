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
                self.cur_point = 1
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
        [(148, 121), (147, 130), (145, 156), (143, 169), (140, 184), (137, 201), (136, 217), (136, 229), (135, 239),
         (134, 256), (135, 272), (133, 294), (130, 305), (126, 317), (118, 334), (112, 345), (100, 349), (97, 349)],
        [(146, 124), (162, 128), (169, 133), (178, 141), (184, 148), (188, 157), (190, 166), (192, 177), (194, 192),
         (191, 202), (186, 216), (180, 228), (171, 237), (154, 248), (145, 250), (134, 250)],
        [(226, 225), (219, 246), (219, 253), (217, 270), (213, 283), (212, 292), (212, 302), (210, 315), (210, 323),
         (212, 337), (219, 349), (227, 356), (236, 360)], [(230, 198), (231, 194), (236, 196), (231, 199), (227, 196)],
        [(323, 237), (316, 236), (305, 239), (300, 243), (294, 250), (286, 259), (282, 266), (279, 275), (275, 288),
         (274, 293), (275, 307), (276, 324), (277, 334), (286, 348), (291, 352), (302, 358), (308, 360), (314, 360),
         (320, 360), (328, 358)],
        [(398, 189), (395, 201), (395, 212), (394, 217), (390, 233), (390, 237), (389, 246), (388, 253), (386, 263),
         (383, 277), (382, 292), (383, 298), (381, 307), (381, 315), (380, 327), (379, 329), (378, 345), (378, 349),
         (382, 360), (385, 364), (389, 367), (398, 369), (405, 368), (409, 366), (416, 360)],
        [(355, 262), (368, 268), (372, 268), (387, 270), (390, 270), (400, 273), (408, 274), (412, 272)],
        [(442, 268), (442, 270), (443, 277), (442, 293), (442, 296), (442, 305), (442, 317), (441, 326), (441, 335),
         (441, 343), (441, 352), (445, 361), (449, 365), (455, 367), (463, 366), (471, 360), (477, 349), (478, 339),
         (481, 324), (483, 310), (483, 295), (483, 281), (485, 266), (485, 270), (484, 278), (486, 290), (482, 300),
         (482, 305), (482, 312), (483, 329), (482, 333), (482, 344), (483, 353), (488, 364), (494, 371), (497, 373)],
        [(522, 266), (522, 270), (524, 280), (521, 294), (520, 306), (522, 321), (522, 339), (520, 354), (520, 365),
         (521, 372)], [(527, 282), (530, 278), (535, 276), (551, 275), (558, 274), (565, 282), (565, 282)],
        [(569, 339), (582, 339), (590, 339), (602, 335), (613, 329), (625, 323), (632, 313), (641, 297), (642, 282),
         (634, 276), (624, 274), (617, 275), (613, 279), (610, 291), (610, 293), (608, 303), (606, 314), (603, 325),
         (602, 342), (602, 349), (606, 370), (603, 359), (604, 375), (614, 376), (621, 381), (627, 380), (636, 378),
         (641, 375)],
        [(715, 290), (707, 285), (692, 287), (685, 289), (681, 293), (676, 302), (675, 308), (673, 316), (672, 326),
         (667, 349), (666, 357), (671, 375), (673, 377), (680, 381), (691, 376), (695, 372), (705, 360), (711, 352),
         (723, 326), (725, 319), (730, 299), (732, 293), (736, 280), (745, 256), (749, 245), (752, 232), (755, 217),
         (757, 203), (755, 194), (748, 192), (743, 203), (742, 221), (743, 224), (737, 242), (735, 262), (732, 270),
         (728, 298), (728, 305), (727, 321), (727, 331), (726, 343), (728, 357), (730, 368), (732, 375), (736, 379),
         (744, 382), (746, 382)],
        [(913, 343), (922, 337), (940, 328), (948, 319), (958, 301), (960, 285), (970, 265), (978, 237), (974, 225),
         (968, 214), (957, 213), (954, 217), (954, 224), (949, 241), (949, 246), (946, 267), (943, 276), (938, 292),
         (936, 304), (935, 320), (933, 329), (931, 345), (928, 359), (935, 375), (940, 391), (945, 400), (957, 409),
         (973, 409), (985, 399), (990, 381), (993, 359), (990, 345), (977, 330), (969, 329), (944, 332)],
        [(1046, 329), (1044, 338), (1045, 352), (1046, 358), (1042, 377), (1043, 389), (1045, 399), (1053, 406),
         (1063, 404), (1070, 398), (1080, 385), (1085, 377), (1087, 358), (1091, 337), (1093, 334), (1094, 336),
         (1092, 346), (1089, 363), (1090, 369), (1090, 379), (1086, 399), (1083, 405), (1081, 415), (1078, 430),
         (1070, 451), (1063, 465), (1055, 479), (1048, 493), (1037, 506), (1023, 514), (999, 524), (979, 517),
         (975, 511), (976, 491), (984, 484), (1011, 460), (1027, 450), (1057, 437), (1077, 428), (1090, 425),
         (1109, 416), (1128, 406), (1138, 403), (1149, 397), (1156, 392), (1167, 381), (1169, 381)],
        [(311, 544), (307, 544), (289, 549), (282, 563), (277, 573), (271, 591), (267, 606), (265, 626), (267, 644),
         (270, 662), (281, 679), (307, 693), (315, 697), (337, 697), (345, 695), (351, 691), (363, 674), (364, 662),
         (365, 649), (364, 640), (364, 640), (365, 648), (365, 668), (365, 679), (366, 691)],
        [(347, 642), (349, 642), (365, 646), (371, 646), (378, 643), (384, 641), (388, 642)],
        [(429, 643), (431, 647), (431, 660), (428, 675), (429, 686), (431, 701), (431, 716), (431, 723), (431, 725)],
        [(430, 652), (432, 648), (442, 641), (450, 640), (462, 641), (469, 643), (474, 648)],
        [(525, 649), (526, 649), (523, 658), (523, 663), (523, 667), (523, 675), (522, 685), (520, 691), (520, 696),
         (522, 710), (523, 713), (526, 719), (536, 723), (543, 724), (547, 722)],
        [(528, 618), (538, 620), (539, 620), (533, 621), (526, 618), (528, 617), (534, 613)],
        [(612, 639), (600, 637), (588, 637), (583, 639), (575, 649), (576, 655), (584, 668), (592, 675), (605, 668),
         (613, 675), (614, 679), (616, 689), (617, 701), (612, 708), (609, 712), (599, 722), (581, 724), (576, 725),
         (571, 722)],
        [(638, 587), (636, 596), (636, 610), (635, 620), (633, 637), (633, 653), (633, 669), (632, 683), (632, 690),
         (630, 706), (628, 723), (629, 728), (628, 722)],
        [(634, 654), (642, 657), (653, 663), (657, 669), (661, 683), (662, 686), (661, 700), (660, 708), (661, 720),
         (661, 728)],
        [(715, 664), (713, 662), (699, 659), (696, 659), (692, 665), (691, 673), (691, 681), (693, 688), (692, 698),
         (692, 705), (694, 715), (698, 720), (700, 722), (705, 722), (713, 717), (717, 713), (721, 695), (726, 681),
         (725, 666), (725, 658), (725, 669), (725, 677), (727, 689), (727, 696), (729, 707), (733, 713), (738, 720),
         (741, 722), (746, 722), (752, 721)],
        [(840, 570), (840, 573), (840, 582), (836, 599), (837, 612), (837, 631), (836, 644), (835, 656), (834, 670),
         (832, 687), (832, 697), (832, 711), (834, 722), (834, 735)],
        [(837, 653), (842, 644), (847, 640), (856, 632), (868, 617), (872, 612), (883, 596), (891, 588), (895, 584)],
        [(837, 655), (844, 665), (849, 673), (857, 681), (862, 687), (866, 693), (878, 710), (882, 715), (888, 722),
         (892, 727), (894, 731), (900, 737)],
        [(920, 656), (920, 663), (921, 675), (921, 687), (921, 696), (922, 710), (923, 729), (926, 735), (938, 736),
         (945, 734), (949, 733), (954, 724), (963, 707), (966, 697), (968, 677), (969, 667), (971, 660), (971, 665),
         (969, 676), (968, 683), (968, 694), (970, 707), (974, 725), (976, 728), (980, 733), (988, 734), (993, 735)],
        [(1012, 659), (1017, 659), (1028, 661), (1036, 663), (1049, 661), (1065, 659), (1069, 659), (1073, 661),
         (1070, 670), (1066, 677), (1061, 684), (1054, 699), (1040, 723), (1034, 728), (1027, 735), (1024, 739),
         (1024, 741), (1034, 741), (1045, 740), (1053, 740), (1064, 741), (1075, 739), (1085, 738)],
        [(1103, 659), (1102, 661), (1102, 678), (1102, 688), (1101, 695), (1102, 710), (1102, 717), (1104, 726),
         (1104, 743)],
        [(1104, 666), (1119, 671), (1126, 674), (1133, 681), (1136, 688), (1137, 696), (1138, 703), (1139, 710),
         (1139, 721), (1138, 732), (1137, 737)],
        [(1163, 712), (1169, 713), (1183, 708), (1189, 706), (1200, 699), (1207, 685), (1210, 676), (1205, 663),
         (1197, 659), (1193, 662), (1190, 672), (1189, 683), (1187, 692), (1186, 704), (1181, 726), (1184, 735),
         (1190, 746), (1200, 750), (1210, 751), (1222, 746), (1227, 741)],
        [(1285, 661), (1278, 660), (1270, 660), (1263, 663), (1260, 666), (1252, 678), (1250, 681), (1245, 704),
         (1245, 711), (1253, 729), (1257, 739), (1263, 746), (1271, 747), (1279, 748), (1287, 749), (1297, 747),
         (1299, 738), (1300, 738)],
        [(1354, 671), (1349, 671), (1340, 672), (1332, 679), (1328, 684), (1324, 696), (1322, 710), (1328, 729),
         (1333, 742), (1342, 754), (1351, 755), (1360, 751), (1366, 744), (1374, 726), (1375, 715), (1379, 694),
         (1378, 685), (1362, 668)],
        [(1408, 669), (1410, 679), (1412, 692), (1413, 698), (1417, 714), (1420, 724), (1422, 733), (1423, 743),
         (1427, 757), (1428, 764), (1427, 761), (1435, 752), (1440, 745), (1445, 726), (1445, 716), (1458, 697),
         (1465, 688), (1466, 680), (1470, 672), (1473, 666), (1474, 666)]]
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
        clock.tick(FPS * 2)


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
        if alpha >= 500:
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
