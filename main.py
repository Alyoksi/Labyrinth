from extra_functions import *
from Classes import *

pg.init()
sc = pg.display.set_mode(RES)
sc.fill(pg.Color('darkslategray'))

clock = pg.time.Clock()

# Creating players
human_start, human_finish = generate_human_start_finish(cols, rows)
bot_start, bot_finish = generate_bot_start_finish(cols, rows, human_start, human_finish)
board, human, bot = create_game(sc, human_start, human_finish, bot_start, bot_finish)

result = ''
going = True
running = True
while running:
    if (human.x, human.y) == human_finish:
        print("You won!!!")
        result = 'win'
        going = False
        (human.x, human.y) = human_start
    elif (bot.x, bot.y) == bot_finish:
        print("You lose!!!")
        result = 'lose'
        going = False
        (bot.x, bot.y) = bot_start

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if going:
                key_pressed(event, human, bot)

            # quit game
            if event.key == pg.K_q:
                running = False
            # quit game
            if event.key == pg.K_e:
                going = False
            # restart
            if event.key == pg.K_r:
                human_start, human_finish = generate_human_start_finish(cols, rows)
                bot_start, bot_finish = generate_bot_start_finish(cols, rows, human_start, human_finish)
                board, human, bot = create_game(sc, human_start, human_finish, bot_start, bot_finish)
                going = True


    board.draw_cells()
    human.draw_start_finish()

    if going:
        bot.draw_start_finish()
        bot.draw_player()
        human.draw_player()
    else:
        if result == 'lose':
            human.draw_path()

    pg.display.update()
    clock.tick(FPS)