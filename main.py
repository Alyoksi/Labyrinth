import pygame as pg
from extra_functions import *
from game_class import Game

# Когда-нибудь сделать выбор сложности
width = 10
height = 10
width_window = calc_width(width)
height_window = cacl_height(height)

info = True
if width < 10:
    info = False
if info:
    height_window += 70

pg.init()
window = pg.display.set_mode((width_window, height_window))
pg.display.set_caption("Лабиринт")

game = Game(width, height, window, width_window, height_window)
game.info = info


game.start_game()

flag_game = True
while flag_game:  # основной игровой цикл
    game.delete_player()
    if tuple(game.player) == game.finish:
        game.start_new_game()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            flag_game = False
        # передвижение
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                game.click_RIGHT()
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                game.click_LEFT()
            if event.key == pg.K_UP or event.key == pg.K_w:
                game.click_UP()
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                game.click_DOWN()
            if event.key == pg.K_p:
                pass

            if event.key == pg.K_q:
                game.setting_trace()

            # Начать заново
            if event.key == pg.K_r:
                game.start_game()

            # Возврат в начало
            if event.key == pg.K_e:
                game.player[0] = game.start[0]
                game.player[1] = game.start[1]

    # рисуем результат, если возволяет ширина экрана
    if game.info:
        game.draw_score()

    game.draw_player()
    game.tick()
    pg.display.update()
