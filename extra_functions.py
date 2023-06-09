import random
from constants import *

def generate_start_point(cols, rows):
    """Функция выбора точки начала лабиринта"""
    # Если True, то рандомим y, иначе x
    if random.choice([True, False]):
        if random.choice([True, False]):
            game_start = (0, random.randint(0, rows - 1))
        else:
            game_start = (cols - 1, random.randint(0, rows - 1))
    else:
        if random.choice([True, False]):
            game_start = (random.randint(0, cols - 1), 0)
        else:
            game_start = (random.randint(0, cols - 1), rows - 1)

    return game_start

def generate_finish_point(cols, rows, start):
    """Выбор точки конца лабиринта"""
    return cols - 1 - start[0], rows - 1 - start[1]

def generate_human_start_finish(cols, rows):
    """generate start and finish points for human"""
    human_start = generate_start_point(cols, rows)
    human_finish = generate_finish_point(cols, rows, human_start)
    return human_start, human_finish

def generate_bot_start_finish(cols, rows, human_start, human_finish):
    """generate start and finish points for bot so that they don't collide with human's"""
    bot_start = generate_start_point(cols, rows)
    bot_finish = generate_finish_point(cols, rows, bot_start)
    while (bot_start == human_start or bot_start == human_finish) or \
            (bot_finish == human_finish or bot_finish == human_start):
        bot_start = generate_start_point(cols, rows)
        bot_finish = generate_finish_point(cols, rows, bot_start)

    return bot_start, bot_finish

def key_pressed(event, human, bot):
    """function that reacts on some keys..."""
    if event.key == pg.K_RIGHT or event.key == pg.K_d:
        human.moveRIGHT()
        bot.stepNext()
    if event.key == pg.K_LEFT or event.key == pg.K_a:
        human.moveLEFT()
        bot.stepNext()
    if event.key == pg.K_UP or event.key == pg.K_w:
        human.moveUP()
        bot.stepNext()
    if event.key == pg.K_DOWN or event.key == pg.K_s:
        human.moveDOWN()
        bot.stepNext()
