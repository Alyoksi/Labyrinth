import random
import pygame as pg
import time
from constants import *


class Game:

    def __init__(self, width, height, window, width_window, height_window):
        self.n = width
        self.m = height

        self.wwidth = width_window
        self.wheight = height_window

        self.font = pg.font.Font("fonts/FiraCodeNerdFont-Regular.ttf", 15)
        #self.font = pg.font.Font(None, 25)

        self.start_time = 0
        self.time = 0

        self.score = 0
        self.record_time = 9999

        self.game_on = True
        self.lost = False

        self.reach_matrix = []
        self.transition_matrix = []
        self.matrix_base = []

        self.window = window

        self.start = ()
        self.finish = ()

        self.player = []
        self.trace = False

    def start_point_generate(self):
        """Функция выбора точки начала лабиринта"""

        # Если True, то рандомим y, иначе x
        if random.choice([True, False]):
            if random.choice([True, False]):
                game_start = (0, random.randint(0, self.m - 1))
            else:
                game_start = (self.n - 1, random.randint(0, self.m - 1))
        else:
            if random.choice([True, False]):
                game_start = (random.randint(0, self.n - 1), 0)
            else:
                game_start = (random.randint(0, self.n - 1), self.m - 1)

        return game_start

    def finish_point_generate(self):
        """Выбор точки конца лабиринта"""
        return self.n - 1 - self.start[0], self.m - 1 - self.start[1]

    def transition_choice(self, x, y, reach_matrix):
        """Функция выбора дальнейшего пути в генерации лабиринта"""

        # Создаем массив точек, в которые можем перейти
        choice_list = []
        if x > 0:
            if not reach_matrix[x - 1][y]:
                choice_list.append((x - 1, y))
        if x < len(reach_matrix) - 1:
            if not reach_matrix[x + 1][y]:
                choice_list.append((x + 1, y))
        if y > 0:
            if not reach_matrix[x][y - 1]:
                choice_list.append((x, y - 1))
        if y < len(reach_matrix[0]) - 1:
            if not reach_matrix[x][y + 1]:
                choice_list.append((x, y + 1))

        # Из созданного списка случайно выбираем точку, в которую пойдем,
        # иначе возвращаем несуществующую точку
        if choice_list:
            nx, ny = random.choice(choice_list)
            if x == nx:
                if ny > y:
                    tx, ty = x * 2, ny * 2 - 1
                else:
                    tx, ty = x * 2, ny * 2 + 1
            else:
                if nx > x:
                    tx, ty = nx * 2 - 1, y * 2
                else:
                    tx, ty = nx * 2 + 1, y * 2
            # nx, ny - координаты в матрице достижимости
            # tx, ty - координаты в матрице перехода
            return nx, ny, tx, ty
        else:
            return -1, -1, -1, -1

    def create_labyrinth(self):
        """Генерация лабиринта"""
        n = self.n
        m = self.m
        # создаем начальную матрицу достижимости ячеек
        self.reach_matrix = []
        for i in range(n):
            self.reach_matrix.append([])
            for j in range(m):
                self.reach_matrix[i].append(False)

        self.transition_matrix = []
        # начальное заполнение матрицы переходов
        for i in range(n * 2 - 1):
            self.transition_matrix.append([])
            for j in range(m * 2 - 1):
                if i % 2 == 0 and j % 2 == 0:
                    self.transition_matrix[i].append(True)
                else:
                    self.transition_matrix[i].append(False)
        # print("Hi")
        # for j in range(len(self.transition_matrix)):
        #     for k in range(len(self.transition_matrix[j])):
        #         print(self.transition_matrix[j][k], end=' ')
        #     print()
        # print("Bye")

        # генерируем стартовую и финишную точки
        self.start = self.start_point_generate()
        self.finish = self.finish_point_generate()

        # создаем маршрутный список, который хранит путь, по которому мы прошли,
        # чтобы в случае тупика мы смогли вернуться
        list_transition = [self.start]
        x, y = self.start
        self.reach_matrix[x][y] = True
        x, y, tx, ty = self.transition_choice(x, y, self.reach_matrix)
        for i in range(1, m * n):
            while not (x >= 0 and y >= 0):
                # если зашли в тупик, то возвращаемся
                x, y = list_transition[-1]
                list_transition.pop()
                # перегенерируем следующую точку
                x, y, tx, ty = self.transition_choice(x, y, self.reach_matrix)

            # отмечаем, что точка подошла
            self.reach_matrix[x][y] = True
            list_transition.append((x, y))
            self.transition_matrix[tx][ty] = True

            # создаем потенциально следующую точку
            x, y, tx, ty = self.transition_choice(x, y, self.reach_matrix)

    # параметры: матрица переходов, начало, конец, толщина проходов, стен, цвет проходов, стен,
    # толщина границы лабиринта, цвет начальной точки, конечной точки

    def draw_labyrinth(self):
        """Рисование лабиринта"""
        matrix = self.transition_matrix
        width = (len(matrix) // 2 + 1) * width_line + (len(matrix) // 2) * width_walls + border * 2
        height = (len(matrix[0]) // 2 + 1) * width_line + (len(matrix[0]) // 2) * width_walls + border * 2

        # рисуем границы лабиринта
        for i in range(width):
            for j in range(height):
                if i < border or width - i <= border or j < border or height - j <= border:
                    pg.draw.line(self.window, color_wall, [i, j], [i, j], 1)
                else:
                    if (i - border) % (width_line + width_walls) <= width_line:
                        x = (i - border) // (width_line + width_walls) * 2
                    else:
                        x = (i - border) // (width_line + width_walls) * 2 + 1
                    if (j - border) % (width_line + width_walls) <= width_line:
                        y = (j - border) // (width_line + width_walls) * 2
                    else:
                        y = (j - border) // (width_line + width_walls) * 2 + 1
                    if matrix[x][y]:
                        pg.draw.line(self.window, color_way, [i, j], [i, j], 1)
                    else:
                        pg.draw.line(self.window, color_wall, [i, j], [i, j], 1)

        # рисуем место старта
        pg.draw.rect(self.window, color_start, (
            border + self.start[0] * (width_line + width_walls), border + self.start[1] * (width_line + width_walls), width_line,
            width_line))

        # рисуем место финиша
        pg.draw.rect(self.window, color_finish, (
            border + self.finish[0] * (width_line + width_walls), border + self.finish[1] * (width_line + width_walls),
            width_line,
            width_line))

    def draw_score(self):
        pg.draw.rect(self.window, (0, 0, 0), (0, self.wheight-25, self.wwidth, 25))
        text2 = self.font.render("Время: " + str(int(self.time)), True, (255, 255, 255))
        self.window.blit(text2, [5, self.wheight - 20])

    def delete_player(self):
        """Функция удаления игрока при движении и оставления следов"""
        player = self.player
        if (player[0], player[1]) == self.start:
            pg.draw.circle(self.window, color_start,
                               (border + player[0] * (width_line + width_walls) + width_line // 2,
                                border + player[1] * (width_line + width_walls) + width_line // 2),
                               width_line // 2 - 3)
        elif (player[0], player[1]) == self.finish:
            pg.draw.circle(self.window, color_finish,
                           (border + player[0] * (width_line + width_walls) + width_line // 2,
                            border + player[1] * (width_line + width_walls) + width_line // 2),
                           width_line // 2 - 3)
        else:
            pg.draw.circle(self.window, color_way,
                               (border + player[0] * (width_line + width_walls) + width_line // 2,
                                border + player[1] * (width_line + width_walls) + width_line // 2),
                               width_line // 2 - 3)
        if self.trace:
            pg.draw.circle(self.window, color_trace,
                               (border + player[0] * (width_line + width_walls) + width_line // 2,
                                border + player[1] * (width_line + width_walls) + width_line // 2),
                               width_line // 3 - 3)

    def draw_player(self):
        """Отрисовка игрока на экране"""
        pg.draw.circle(self.window, color_player,
                           (border + self.player[0] * (width_line + width_walls) + width_line // 2,
                            border + self.player[1] * (width_line + width_walls) + width_line // 2),
                           width_line // 2 - 3)

    def tick(self):
        """Cекудномер"""
        self.time = time.time() - self.start_time

    def click_RIGHT(self):
        """Движение вправо"""
        if len(self.transition_matrix) > self.player[0] * 2 + 2:
            if self.transition_matrix[self.player[0] * 2 + 1][self.player[1] * 2]:
                self.player[0] += 1

    def click_LEFT(self):
        """Движение влево"""
        if -1 < self.player[0] * 2 - 2:
            if self.transition_matrix[self.player[0] * 2 - 1][self.player[1] * 2]:
                self.player[0] -= 1

    def click_DOWN(self):
        """Движение вниз"""
        if len(self.transition_matrix[0]) > self.player[1] * 2 + 2:
            if self.transition_matrix[self.player[0] * 2][self.player[1] * 2 + 1]:
                self.player[1] += 1

    def click_UP(self):
        """Движение вверх"""
        if -1 < self.player[1] * 2 - 2:
            if self.transition_matrix[self.player[0] * 2][self.player[1] * 2 - 1]:
                self.player[1] -= 1

    def setting_trace(self):
        """Изменение флага оставления следов"""
        if self.trace:
            self.trace = False
        else:
            self.trace = True

    def start_game(self):
        self.window.fill((0, 0, 0))
        self.start_time = time.time()
        pg.draw.rect(self.window, (0, 0, 0), (0, self.wheight - 70, self.wwidth, 70))
        self.create_labyrinth()
        k = 0
        while self.transition_matrix in self.matrix_base or self.start[0] == self.finish[0] \
                or self.start[1] == self.finish[1]:
            self.create_labyrinth()
            k += 1
            if k > 20:
                print('Не найдено лабиринтов без повторения')
                break

        self.matrix_base.append(self.transition_matrix)
        self.player = list(self.start)
        self.draw_labyrinth()
        self.draw_player()

    def show_path(self):
        pass