from constants import *
import pygame as pg


def calc_width(width):
    return ((width * 2 - 1) // 2 + 1) * width_line + ((width * 2 - 1) // 2) * width_walls + border * 2


def cacl_height(height):
    return ((height * 2 - 1) // 2 + 1) * width_line + ((height * 2 - 1) // 2) * width_walls + border * 2


def input_diff():
    width, height = (0, 0)

    print('''Выберите сложность:
    1. Легкая (10 x 7)
    2. Нормальная (20 x 15)
    3. Сложная (30 x 20) ''')

    diff = input("Введите только номер сложности: ")
    while not (diff.isdigit()) or not (1 <= int(diff) <= 3):
        print("Сложность - целое число от 1 от 3!")
        diff = input("Введите только номер сложности: ")
    diff = int(diff)
    if diff == 1:
        width = 10
        height = 7
    elif diff == 2:
        width = 20
        height = 15
    elif diff == 3:
        width = 30
        height = 20

    return width, height


def key_pressed(event, game):
    # Движение
    if event.key == pg.K_RIGHT or event.key == pg.K_d:
        game.click_RIGHT()
    if event.key == pg.K_LEFT or event.key == pg.K_a:
        game.click_LEFT()
    if event.key == pg.K_UP or event.key == pg.K_w:
        game.click_UP()
    if event.key == pg.K_DOWN or event.key == pg.K_s:
        game.click_DOWN()

    # TODO: исправить README.md
    if event.key == pg.K_e:
        game.game_on = False
        game.lost = True

    # Запустить след
    if event.key == pg.K_t:
        game.setting_trace()
    # Начать заново
    if event.key == pg.K_r:
        game.start_game()
    # Возврат в начало
    if event.key == pg.K_c:
        game.player[0] = game.start[0]
        game.player[1] = game.start[1]
