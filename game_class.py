import random
import pygame as pg
import time
from constants import *


class Game:

    def __init__(self, width, height, window, width_window, height_window):
        self.__n = width
        self.__m = height

        self.__wwidth = width_window
        self.__wheight = height_window

        self.__font = pg.font.Font("fonts/FiraCodeNerdFont-Regular.ttf", 15)

        self.__start_time = 0
        self.__time = 0

        self.game_on = True
        self.lost = False

        self.__reach_matrix = []
        self.__transition_matrix = []
        self.__matrix_base = []

        self.__window = window

        self.start = ()
        self.finish = ()

        self.player = []
        self.__trace = False

    def __start_point_generate(self):
        """Функция выбора точки начала лабиринта"""

        # Если True, то рандомим y, иначе x
        if random.choice([True, False]):
            if random.choice([True, False]):
                game_start = (0, random.randint(0, self.__m - 1))
            else:
                game_start = (self.__n - 1, random.randint(0, self.__m - 1))
        else:
            if random.choice([True, False]):
                game_start = (random.randint(0, self.__n - 1), 0)
            else:
                game_start = (random.randint(0, self.__n - 1), self.__m - 1)

        return game_start

    def __finish_point_generate(self):
        """Выбор точки конца лабиринта"""
        return self.__n - 1 - self.start[0], self.__m - 1 - self.start[1]

    def __transition_choice(self, x, y, reach_matrix):
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
        n = self.__n
        m = self.__m
        # создаем начальную матрицу достижимости ячеек
        self.__reach_matrix = []
        for i in range(n):
            self.__reach_matrix.append([])
            for j in range(m):
                self.__reach_matrix[i].append(False)

        self.__transition_matrix = []
        # начальное заполнение матрицы переходов
        for i in range(n * 2 - 1):
            self.__transition_matrix.append([])
            for j in range(m * 2 - 1):
                if i % 2 == 0 and j % 2 == 0:
                    self.__transition_matrix[i].append(True)
                else:
                    self.__transition_matrix[i].append(False)
        # print("Hi")
        # for j in range(len(self.transition_matrix)):
        #     for k in range(len(self.transition_matrix[j])):
        #         print(self.transition_matrix[j][k], end=' ')
        #     print()
        # print("Bye")

        # генерируем стартовую и финишную точки
        self.start = self.__start_point_generate()
        self.finish = self.__finish_point_generate()

        # создаем маршрутный список, который хранит путь, по которому мы прошли,
        # чтобы в случае тупика мы смогли вернуться
        list_transition = [self.start]
        x, y = self.start
        self.__reach_matrix[x][y] = True
        x, y, tx, ty = self.__transition_choice(x, y, self.__reach_matrix)
        for i in range(1, m * n):
            while not (x >= 0 and y >= 0):
                # если зашли в тупик, то возвращаемся
                x, y = list_transition[-1]
                list_transition.pop()
                # перегенерируем следующую точку
                x, y, tx, ty = self.__transition_choice(x, y, self.__reach_matrix)

            # отмечаем, что точка подошла
            self.__reach_matrix[x][y] = True
            list_transition.append((x, y))
            self.__transition_matrix[tx][ty] = True

            # создаем потенциально следующую точку
            x, y, tx, ty = self.__transition_choice(x, y, self.__reach_matrix)

    # параметры: матрица переходов, начало, конец, толщина проходов, стен, цвет проходов, стен,
    # толщина границы лабиринта, цвет начальной точки, конечной точки

    def draw_labyrinth(self):
        """Рисование лабиринта"""
        matrix = self.__transition_matrix
        width = (len(matrix) // 2 + 1) * width_line + (len(matrix) // 2) * width_walls + border * 2
        height = (len(matrix[0]) // 2 + 1) * width_line + (len(matrix[0]) // 2) * width_walls + border * 2

        # рисуем границы лабиринта
        for i in range(width):
            for j in range(height):
                if i < border or width - i <= border or j < border or height - j <= border:
                    pg.draw.line(self.__window, color_wall, [i, j], [i, j], 1)
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
                        pg.draw.line(self.__window, color_way, [i, j], [i, j], 1)
                    else:
                        pg.draw.line(self.__window, color_wall, [i, j], [i, j], 1)

        # рисуем место старта
        pg.draw.rect(self.__window, color_start, (
            border + self.start[0] * (width_line + width_walls), border + self.start[1] * (width_line + width_walls), width_line,
            width_line))

        # рисуем место финиша
        pg.draw.rect(self.__window, color_finish, (
            border + self.finish[0] * (width_line + width_walls), border + self.finish[1] * (width_line + width_walls),
            width_line,
            width_line))

    def draw_score(self):
        pg.draw.rect(self.__window, (0, 0, 0), (0, self.__wheight - 25, self.__wwidth, 25))
        text2 = self.__font.render("Время: " + str(int(self.__time)), True, (255, 255, 255))
        self.__window.blit(text2, [5, self.__wheight - 20])

    def delete_player(self):
        """Функция удаления игрока при движении и оставления следов"""
        player = self.player
        if (player[0], player[1]) == self.start:
            pg.draw.circle(self.__window, color_start,
                           (border + player[0] * (width_line + width_walls) + width_line // 2,
                                border + player[1] * (width_line + width_walls) + width_line // 2),
                           width_line // 2 - 3)
        elif (player[0], player[1]) == self.finish:
            pg.draw.circle(self.__window, color_finish,
                           (border + player[0] * (width_line + width_walls) + width_line // 2,
                            border + player[1] * (width_line + width_walls) + width_line // 2),
                           width_line // 2 - 3)
        else:
            pg.draw.circle(self.__window, color_way,
                           (border + player[0] * (width_line + width_walls) + width_line // 2,
                                border + player[1] * (width_line + width_walls) + width_line // 2),
                           width_line // 2 - 3)
        if self.__trace:
            pg.draw.circle(self.__window, color_trace,
                           (border + player[0] * (width_line + width_walls) + width_line // 2,
                                border + player[1] * (width_line + width_walls) + width_line // 2),
                           width_line // 3 - 3)

    def draw_player(self):
        """Отрисовка игрока на экране"""
        pg.draw.circle(self.__window, color_player,
                       (border + self.player[0] * (width_line + width_walls) + width_line // 2,
                            border + self.player[1] * (width_line + width_walls) + width_line // 2),
                       width_line // 2 - 3)

    def tick(self):
        """Cекудномер"""
        self.__time = time.time() - self.__start_time

    def click_RIGHT(self):
        """Движение вправо"""
        if len(self.__transition_matrix) > self.player[0] * 2 + 2:
            if self.__transition_matrix[self.player[0] * 2 + 1][self.player[1] * 2]:
                self.player[0] += 1

    def click_LEFT(self):
        """Движение влево"""
        if -1 < self.player[0] * 2 - 2:
            if self.__transition_matrix[self.player[0] * 2 - 1][self.player[1] * 2]:
                self.player[0] -= 1

    def click_DOWN(self):
        """Движение вниз"""
        if len(self.__transition_matrix[0]) > self.player[1] * 2 + 2:
            if self.__transition_matrix[self.player[0] * 2][self.player[1] * 2 + 1]:
                self.player[1] += 1

    def click_UP(self):
        """Движение вверх"""
        if -1 < self.player[1] * 2 - 2:
            if self.__transition_matrix[self.player[0] * 2][self.player[1] * 2 - 1]:
                self.player[1] -= 1

    def setting_trace(self):
        """Изменение флага оставления следов"""
        if self.__trace:
            self.__trace = False
        else:
            self.__trace = True

    def start_game(self):
        self.__window.fill((0, 0, 0))
        self.__start_time = time.time()
        pg.draw.rect(self.__window, (0, 0, 0), (0, self.__wheight - 70, self.__wwidth, 70))
        self.create_labyrinth()
        k = 0
        while self.__transition_matrix in self.__matrix_base or self.start[0] == self.finish[0] \
                or self.start[1] == self.finish[1]:
            self.create_labyrinth()
            k += 1
            if k > 20:
                print('Не найдено лабиринтов без повторения')
                break

        self.__matrix_base.append(self.__transition_matrix)
        self.player = list(self.start)
        self.draw_labyrinth()
        self.draw_player()

    def show_path(self):
        pass