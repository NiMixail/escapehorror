import sys
import os
import pygame


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
    data['player'], data['monster'] = data_list[0]
    data['items'] = {}
    for i in data_list[1]:
        data['items'][i[0]] = i[1]
    data['collected_items'] = [i[0] for i in data_list[2]]
    data['flashlight_charge'] = data_list[3][0][0]
    data['batteries_number'] = data_list[3][0][1]
    return data


def set_default_continue():
    with open('data/continue.txt', 'w', encoding='UTF-8') as f:
        f.write(""", , , положение игрока (x; y; этаж) (последний элемент каждой строки - пояснение)
, , , положение монстра (x; y; этаж)

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

, , заряд фонарика(%) + количество батареек""")
