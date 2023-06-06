from random import choice
from constants import *

# Array of cells
grid_cells = []

class Board:

    def __init__(self, screen):
        global grid_cells

        self.screen = screen
        # creating default field
        grid_cells = [Cell(screen, col, row) for row in range(rows) for col in range(cols)]

    def generate_labyrinth(self):
        """function that changes array grid_cells so that forms labyrinth"""

        current_cell = grid_cells[0]
        current_cell.visited = True
        cnt_visited = 1
        stack = []
        # while not all cells were visited
        while cnt_visited != rows * cols:
            # take next cell
            next_cell = current_cell.check_neighbors()
            # if we can take next cell
            if next_cell:
                next_cell.visited = True
                cnt_visited += 1
                stack.append(current_cell)
                remove_walls(current_cell, next_cell)
                current_cell = next_cell
            # taking one step back
            elif stack:
                current_cell = stack.pop()

    def draw_cells(self):
        """drawing all cells with borders from grid_cell array"""
        [cell.draw() for cell in grid_cells]

class Cell:

    def __init__(self, screen, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'left': True, 'bottom': True,}
        self.visited = False
        self.screen = screen

    def check_neighbors(self):
        """function return array of adjoing cells if there are any, otherwise False"""
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

    def draw(self):
        # convert to field coords
        x, y = self.x * TILE, self.y * TILE
        # drawing cell
        if self.visited:
            pg.draw.rect(self.screen, BACKGROUND, (x, y, TILE, TILE))

        # drawing walls
        if self.walls['top']:
            pg.draw.line(self.screen, pg.Color('darkorange'), (x, y), (x+TILE, y), BORDERS)
        if self.walls['right']:
            pg.draw.line(self.screen, pg.Color('darkorange'), (x+TILE, y), (x+TILE, y+TILE), BORDERS)
        if self.walls['left']:
            pg.draw.line(self.screen, pg.Color('darkorange'), (x, y), (x, y+TILE), BORDERS)
        if self.walls['bottom']:
            pg.draw.line(self.screen, pg.Color('darkorange'), (x, y+TILE), (x+TILE, y+TILE), BORDERS)

class Player:

    def __init__(self, screen, base_color, start_color, finish_color, x, y, fx, fy):
        # player coords
        self.x = x
        self.y = y

        # start coords
        self.sx = x
        self.sy = y
        # finish coords
        self.fx= fx
        self.fy = fy

        self.screen = screen
        # player color
        self.color = base_color
        # start point color
        self.start_color = start_color
        # finish point color
        self.finish_color = finish_color
        # array of points that create path from start to finish
        self.path = []
        self.stack = []

    def find_path(self, x, y, px=-1, py=-1):
        # if not start point
        if x != self.x or y != self.y:
            self.stack.append((x, y))
        # if we met finish - end
        if x == self.fx and y == self.fy:
            self.path = self.stack[::-1]
            return

        # go to any possible direction
        if y-1 != py and check_cell(x, y-1):
            if not check_cell(x, y).walls['top']:
                self.find_path(x, y - 1, x, y)
        if not check_cell(x, y).walls['bottom']:
            if y+1 != py and check_cell(x, y+1):
                self.find_path(x, y + 1, x, y)
        if not check_cell(x, y).walls['right']:
            if x+1 != px and check_cell(x+1, y):
                self.find_path(x + 1, y, x, y)
        if not check_cell(x, y).walls['left']:
            if x-1 != px and check_cell(x-1, y):
                self.find_path(x - 1, y, x, y)

        self.stack.pop()

    def draw_start_finish(self):
        """drawing start and finish cells"""
        pg.draw.rect(self.screen, self.start_color, (self.sx*TILE + BORDERS, self.sy * TILE+ BORDERS,
                                                     TILE - BORDERS, TILE - BORDERS))
        
        pg.draw.rect(self.screen, self.finish_color, (self.fx * TILE + BORDERS, self.fy * TILE + BORDERS,
                                                      TILE - BORDERS, TILE - BORDERS))

    def draw_path(self):
        """drawing path from start to finish"""
        for a, b in self.path:
            x, y = a * TILE, b * TILE
            pg.draw.circle(self.screen, self.color, (x + TILE // 2, y + TILE // 2), (TILE - 10) // 4, 3)

    def draw_player(self):
        x, y = self.x * TILE, self.y * TILE
        pg.draw.circle(self.screen, self.color, (x+TILE//2, y+TILE//2), (TILE-10) // 2)

class Human(Player):
    """A class describing user behavior"""
    # Human movement
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
    """A class describing user behavior"""
    # bot movement
    def stepNext(self):
        if self.path:
            # for 1 human move bot has 2/3 chance to step forward
            if choice([True, True, False]):
                self.x, self.y = self.path[-1]
                self.path.pop()

def remove_walls(current, next):
    """removing wall between two adjoined cells"""
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
    """return cell object in (x,y) coords in main matrix if posible, False otherwise"""
    if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
        return False
    return grid_cells[x + y*cols]

# creating instances of classes
def create_game(sc, human_start, human_finish, bot_start, bot_finish):
    board = Board(sc)
    board.generate_labyrinth()

    # Создаем игрока-человека
    human = Human(sc, HUMANCOLOR, HUMANSTFI, HUMANSTFI, human_start[0], human_start[1], human_finish[0], human_finish[1])
    human.find_path(human_start[0], human_start[1])
    # Создаем игрока-бота
    bot = Bot(sc, BOTCOLOR, BOTSTFI, BOTSTFI, bot_start[0], bot_start[1], bot_finish[0], bot_finish[1])
    bot.find_path(bot_start[0], bot_start[1])

    return board, human, bot
