import pygame as pg
from extra_functions import *
from game_class import Game


width, height = input_diff()

# Когда-нибудь сделать выбор сложности
width_window = calc_width(width)
height_window = cacl_height(height)
height_window += 25  # место для времени

pg.init()
window = pg.display.set_mode((width_window, height_window))
pg.display.set_caption("Лабиринт")

game = Game(width, height, window, width_window, height_window)

game.start_game()

flag_game = True
while flag_game:  # основной игровой цикл
    game.delete_player()

    if game.game_on:
        if tuple(game.player) == game.finish:
            game.game_on = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                flag_game = False
            # передвижение
            if event.type == pg.KEYDOWN:
                # Поведение клавиш
                key_pressed(event, game)

        # рисуем результат, если возволяет ширина экрана
        game.draw_score()

        game.draw_player()
        game.tick()
    else:
        if game.lost:
            game.show_path()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                flag_game = False

            if event.type == pg.KEYDOWN:
                # Начать новую игру
                if event.key == pg.K_r:
                    game = Game(width, height, window, width_window, height_window)
                    game.start_game()
    pg.display.update()

pg.quit()
