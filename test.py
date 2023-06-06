import pytest

import Classes
from Classes import *
import pygame as pg
from Constants import *
from extra_functions import *

pg.init()
sc = pg.display.set_mode((10, 10))


class TestTest:

    def test_checkClasses(self):
        board = Board(sc)
        assert isinstance(board, Board)

        cell = Cell(sc, 0, 0)
        assert isinstance(cell, Cell)

        human = Human(sc, HUMANCOLOR, HUMANSTFI, HUMANSTFI, 0, 0, 1, 1)
        assert isinstance(human, Human)

        bot = Bot(sc, HUMANCOLOR, HUMANSTFI, HUMANSTFI, 0, 0, 1, 1)
        assert isinstance(bot, Bot)

    def test_checkCreateGame(self):
        board, human, bot = create_game(sc, (0, 0), (1, 1), (2, 2), (3, 3))
        assert isinstance(board, Board)
        assert isinstance(human, Human)
        assert isinstance(bot, Bot)

    def test_checkGenerateStart(self):
        s1, s2 = generate_start_point(10, 10)
        assert 0 <= s1 <= 10
        assert 0 <= s2 <= 10

        s1, s2 = generate_start_point(20, 150)
        assert 0 <= s1 <= 20
        assert 0 <= s2 <= 150

    def test_checkGenerateFinish(self):
        s1, s2 = generate_start_point(10, 10)
        f1, f2 = generate_finish_point(10, 10, (s1, s2))
        assert 9-s1 == f1
        assert 9-s2 == f2

        s1, s2 = generate_start_point(20, 150)
        f1, f2 = generate_finish_point(20, 150, (s1, s2))
        assert 19-s1 == f1
        assert 149-s2 == f2

    def test_checkHumanStartFinish(self):
        hs, hf = generate_human_start_finish(10, 10)
        assert 0 <= hs[0] <= 10
        assert 0 <= hs[1] <= 10

        assert 9-hs[0] == hf[0]
        assert 9-hs[1] == hf[1]

        hs, hf = generate_human_start_finish(20, 150)
        assert 0 <= hs[0] <= 20
        assert 0 <= hs[1] <= 150

        assert 19-hs[0] == hf[0]
        assert 149-hs[1] == hf[1]

    def test_checkBotStartFinish(self):
        hs, hf = generate_human_start_finish(10, 10)
        bs, bf = generate_bot_start_finish(10, 10, hs, hf)

        assert bs != hs
        assert 0 <= bs[0] <= 10
        assert 0 <= bs[1] <= 10

        assert bf != hf
        assert 0 <= bf[0] <= 10
        assert 0 <= bf[1] <= 10

        hs, hf = generate_human_start_finish(20, 150)
        bs, bf = generate_bot_start_finish(20, 150, hs, hf)

        assert bs != hs
        assert 0 <= bs[0] <= 20
        assert 0 <= bs[1] <= 150

        assert bf != hf
        assert 0 <= bf[0] <= 20
        assert 0 <= bf[1] <= 150

    def test_removewalls(self):
        c1 = Cell(sc, 0, 0)
        c2 = Cell(sc, 0, 1)
        remove_walls(c1, c2)
        assert not c1.walls["bottom"]
        assert not c2.walls["top"]

        c1 = Cell(sc, 0, 0)
        c2 = Cell(sc, 1, 0)
        remove_walls(c1, c2)
        assert not c1.walls["right"]
        assert not c2.walls["left"]

        c1 = Cell(sc, 1, 0)
        c2 = Cell(sc, 0, 0)
        remove_walls(c1, c2)
        assert not c1.walls["left"]
        assert not c2.walls["right"]

        c1 = Cell(sc, 0, 1)
        c2 = Cell(sc, 0, 0)
        remove_walls(c1, c2)
        assert not c1.walls["top"]
        assert not c2.walls["bottom"]

        c1 = Cell(sc, 0, 0)
        c2 = Cell(sc, 10, 10)
        remove_walls(c1, c2)
        assert c1.walls["top"]
        assert c1.walls["bottom"]
        assert c1.walls["right"]
        assert c1.walls["left"]

        assert c2.walls["left"]
        assert c2.walls["left"]
        assert c2.walls["left"]
        assert c2.walls["left"]

