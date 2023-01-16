import sys
import os
import pygame
import sqlite3


class Audio:
    def __init__(self):
        pygame.mixer.init()
        self.effects = {}
        for fn in os.listdir(path='data/sounds'):
            if not fn.startswith('ost_'):
                self.effects[fn[:-4]] = pygame.mixer.Sound('data/sounds/' + fn)
        print(self.effects)

    def eff(self, name):
        return self.effects[name]

    def set_bg_music(self, name_with_extension):
        pygame.mixer.music.load('data/sounds/ost_' + name_with_extension)

    def bg_music(self):
        return pygame.mixer.music


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_continue():
    with open('data/continue.txt', 'r', encoding='UTF-8') as f:
        data_list = [[j.split(', ')[:-1] for j in i.split('\n')] for i in f.read().split('\n\n')]
    data = {}
    data['player'], data['monster'], data['camera'] = data_list[0]
    data['items'] = {}
    for i in data_list[1]:
        if i[0]:
            data['items'][i[0]] = i[1]
    data['collected_items'] = [i[0] for i in data_list[2] if i[0]]
    data['doors_opened'] = [i[0] for i in data_list[3] if i and i[0]]
    return data


def set_default_continue():
    with open('data/continue.txt', 'w', encoding='UTF-8') as f:
        f.write(""", , , положение игрока (x; y; этаж) (последний элемент каждой строки - пояснение)
, , , положение монстра (x; y; этаж)
, , , смещение камеры

, , -
, ,  |
, ,  } пложение вещей (класс предмета; id предмета мебели)
, ,  |
, , -

, -
,  |
,  } вещи в инвентаре (класс предмета)
,  |
, -

, -
, - открытые двери
, -
, - """)


def set_continue(data):
    player = ', '.join([str(i) for i in data['player']])
    monster = ', '.join([str(i) for i in data['monster']])
    camera = ', '.join([str(i) for i in data['camera']])
    doors_opened = data['doors_opened']
    dor_op = '\n'.join([i + ', -' for i in doors_opened]) + ' открытые двери' if doors_opened else ', - открытые двери'
    items = '\n'.join([i + ', ' + str(data['items'][i]) + ', ' for i in data['items']])
    if not items:
        items = ', , } пложение вещей (название предмета; id предмета мебели)'
    else:
        items = items.split('\n')
        items = '\n'.join(
            items[i] + '} пложение вещей (название предмета; id предмета мебели)' if i == len(items) // 2 else items[i]
            for
            i in range(len(items)))
    col_items = data['collected_items']
    if len(col_items) == 0:
        col_items = ', } вещи в инвентаре (название предмета)'
    else:
        col_items = '\n'.join(
            col_items[i] + ', } вещи в инвентаре (название предмета)' if i == len(col_items) // 2 else col_items[
                                                                                                           i] + ', '
            for i in range(len(col_items)))
    with open('data/continue.txt', 'w', encoding='UTF-8') as f:
        f.write(f"""{player}, положение игрока (x; y; этаж) (последний элемент каждой строки - пояснение)
{monster}, положение монстра (x; y; этаж)
{camera}, смещение камеры

{items}

{col_items}

{dor_op}""")


def load_map():
    con = sqlite3.connect('data/map.db')
    cur = con.cursor()
    data = {}
    data['furniture'] = cur.execute('select * from furniture').fetchall()
    data['walls'] = cur.execute('select * from walls').fetchall()
    data['floor'] = cur.execute('select * from floor').fetchall()
    con.close()
    return data


if __name__ == '__main__':
    set_default_continue()
