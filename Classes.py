from random import choice
from Constants import *
from extra_functions import input_diff

# Клетки
grid_cells = []

# размеры, количество клеток
TILE = input_diff()
rows, cols = HEIGHT // TILE, WIDTH // TILE

class Board:

    def __init__(self, screen):
        global grid_cells

        self.screen = screen


        grid_cells = [Cell(screen, col, row) for row in range(rows) for col in range(cols)]

    def generate_labyrinth(self):
        current_cell = grid_cells[0]
        current_cell.visited = True
        cnt_visited = 1
        stack = []
        while cnt_visited != rows * cols:
            next_cell = current_cell.check_neighbors()
            if next_cell:
                next_cell.visited = True
                cnt_visited += 1
                stack.append(current_cell)
                remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()

    def draw_cells(self):
        [cell.draw() for cell in grid_cells]

class Cell:

    def __init__(self, screen, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'left': True, 'bottom': True,}
        self.visited = False
        self.screen = screen

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pg.draw.rect(self.screen, BACKGROUND, (x, y, TILE, TILE))

        if self.walls['top']:
            pg.draw.line(self.screen, pg.Color('darkorange'), (x, y), (x+TILE, y), 2)
        if self.walls['right']:
            pg.draw.line(self.screen, pg.Color('darkorange'), (x+TILE, y), (x+TILE, y+TILE), 2)
        if self.walls['left']:
            pg.draw.line(self.screen, pg.Color('darkorange'), (x, y), (x, y+TILE), 2)
        if self.walls['bottom']:
            pg.draw.line(self.screen, pg.Color('darkorange'), (x, y+TILE), (x+TILE, y+TILE), 2)

    def check_neighbors(self):
        x, y = self.x, self.y
        neighbors = []
        top   =  check_cell(x, y - 1)
        right =  check_cell(x+1, y)
        left  =  check_cell(x-1, y)
        bottom= check_cell(x, y + 1)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if left and not left.visited:
            neighbors.append(left)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        return choice(neighbors) if neighbors else False

class Player:

    def __init__(self, screen, base_color, start_color, finish_color, x, y, fx, fy):
        self.x = x
        self.y = y

        self.sx = x*TILE
        self.sy = y*TILE

        self.fx= fx
        self.fy = fy

        self.screen = screen
        self.color = base_color
        self.start_color = start_color
        self.finish_color = finish_color
        self.path = []
        self.stack = []

        self.find_path_to_finish(self.x, self.y)
        self.path.reverse()

    def find_path_to_finish(self, x, y, px=-1, py=-1):
        if x != self.x or y != self.y:
            self.stack.append((x, y))
        if x == self.fx and y == self.fy:
            self.path = self.stack[:]
            return

        if y-1 != py and check_cell(x, y-1):
            if not check_cell(x, y).walls['top']:
                self.find_path_to_finish(x, y-1, x, y)
        if not check_cell(x, y).walls['bottom']:
            if y+1 != py and check_cell(x, y+1):
                self.find_path_to_finish(x, y+1, x, y)
        if not check_cell(x, y).walls['right']:
            if x+1 != px and check_cell(x+1, y):
                self.find_path_to_finish(x+1, y, x, y)
        if not check_cell(x, y).walls['left']:
            if x-1 != px and check_cell(x-1, y):
                self.find_path_to_finish(x-1, y, x, y)

        self.stack.pop()

    def draw_start_finish(self):
        pg.draw.rect(self.screen, self.start_color, (self.sx + 2, self.sy + 2, TILE - 2, TILE - 2))
        pg.draw.rect(self.screen, self.finish_color, (self.fx * TILE + 2, self.fy * TILE + 2, TILE - 2, TILE - 2))

    def draw_path(self):
        for a, b in self.path:
            x, y = a * TILE, b * TILE
            pg.draw.circle(self.screen, self.color, (x + TILE // 2, y + TILE // 2), (TILE - 10) // 4, 2)

    def draw_player(self):
        x, y = self.x * TILE, self.y * TILE
        pg.draw.circle(self.screen, self.color, (x+TILE//2, y+TILE//2), (TILE-10) // 2)

class Human(Player):

    def moveUP(self):
        if not check_cell(self.x, self.y).walls['top']:
            self.y -= 1

    def moveRIGHT(self):
        if not check_cell(self.x, self.y).walls['right']:
            self.x += 1

    def moveLEFT(self):
        if not check_cell(self.x, self.y).walls['left']:
            self.x -= 1

    def moveDOWN(self):
        if not check_cell(self.x, self.y).walls['bottom']:
            self.y += 1

class Bot(Player):
    def stepNext(self):
        if self.path:
            if choice([True, True, False]):
                self.x, self.y = self.path[-1]
                self.path.pop()

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    if dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    if dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def check_cell(x, y):

    if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
        return False
    return grid_cells[x + y*cols]

def create_game(sc, human_start, human_finish, bot_start, bot_finish):
    board = Board(sc)
    board.generate_labyrinth()

    # Создаем игрока-человека
    human = Human(sc, BLUE, GREEN, RED, human_start[0], human_start[1], human_finish[0], human_finish[1])
    # Создаем игрока-бота
    bot = Bot(sc, BLACK, GREY, GREY, bot_start[0], bot_start[1], bot_finish[0], bot_finish[1])

    return board, human, bot
