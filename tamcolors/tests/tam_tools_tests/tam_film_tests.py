# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors import tam_tools
from tamcolors.tam_io.tam_colors import *


class TAMFilmTests(unittest.TestCase):
    def test_init_film(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=True)

        self.assertTrue(film.get_circular())

    def test_setitem(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        tam_buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "T", LIGHT_RED, RED)
        film[1] = tam_buffer

        self.assertIs(film[1], tam_buffer)

    def test_setitem_2(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        self.assertRaises(tam_tools.tam_film.TAMFilmError,
                          film.__setitem__,
                          "key",
                          tam_io.tam_buffer.TAMBuffer(8, 5, "B", RED, LIGHT_RED))

    def test_setitem_3(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        self.assertRaises(tam_tools.tam_film.TAMFilmError,
                          film.__setitem__,
                          -1,
                          tam_io.tam_buffer.TAMBuffer(8, 5, "B", RED, LIGHT_RED))

    def test_getitem(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)
        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=False)

        self.assertIs(film[0], tam_buffer)
        self.assertIs(film[1], tam_buffer_2)
        self.assertIs(film[2], tam_buffer_3)

    def test_getitem_2(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", YELLOW, BLUE)
        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2), circular=False)

        self.assertIs(film[0], tam_buffer)
        self.assertIs(film[1], tam_buffer_2)

        self.assertRaises(tam_tools.tam_film.TAMFilmError, film.__getitem__, "id")

    def test_getitem_3(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2), circular=False)

        self.assertIs(film[0], tam_buffer)
        self.assertIs(film[1], tam_buffer_2)

        self.assertRaises(tam_tools.tam_film.TAMFilmError, film.__getitem__, 2)

    def test_next(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)

        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=False)

        self.assertIs(tam_buffer, next(film))
        self.assertIs(tam_buffer_2, next(film))
        self.assertIs(tam_buffer_3, next(film))
        self.assertIs(tam_buffer_3, next(film))

    def test_next_2(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)

        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=True)

        self.assertIs(tam_buffer, next(film))
        self.assertIs(tam_buffer_2, next(film))
        self.assertIs(tam_buffer_3, next(film))
        self.assertIs(tam_buffer, next(film))

    def test_len(self):
        film = tam_tools.tam_film.TAMFilm([], circular=True)

        self.assertEqual(len(film), 0)

    def test_len_2(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        self.assertEqual(len(film), 2)

    def test_set(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        tam_buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "T", LIGHT_RED, RED)
        film.set(1, tam_buffer)

        self.assertIs(film.get(1), tam_buffer)

    def test_set_2(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        self.assertRaises(tam_tools.tam_film.TAMFilmError,
                          film.set,
                          "key",
                          tam_io.tam_buffer.TAMBuffer(8, 5, "B", RED, LIGHT_RED))

    def test_set_3(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        self.assertRaises(tam_tools.tam_film.TAMFilmError,
                          film.set,
                          -1,
                          tam_io.tam_buffer.TAMBuffer(8, 5, "B", RED, LIGHT_RED))

    def test_get(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)
        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=False)

        self.assertIs(film.get(0), tam_buffer)
        self.assertIs(film.get(1), tam_buffer_2)
        self.assertIs(film.get(2), tam_buffer_3)

    def test_get_2(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2), circular=False)

        self.assertIs(film.get(0), tam_buffer)
        self.assertIs(film.get(1), tam_buffer_2)

        self.assertRaises(tam_tools.tam_film.TAMFilmError, film.get, "id")

    def test_get_3(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2), circular=False)

        self.assertIs(film.get(0), tam_buffer)
        self.assertIs(film.get(1), tam_buffer_2)

        self.assertRaises(tam_tools.tam_film.TAMFilmError, film.get, 2)

    def test_slide(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)

        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=False)

        self.assertIs(tam_buffer, film.slide())
        self.assertIs(tam_buffer_2, film.slide())
        self.assertIs(tam_buffer_3, film.slide())
        self.assertIs(tam_buffer_3, film.slide())

    def test_slide_2(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)

        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=True)

        self.assertIs(tam_buffer, film.slide())
        self.assertIs(tam_buffer_2, film.slide())
        self.assertIs(tam_buffer_3, film.slide())
        self.assertIs(tam_buffer, film.slide())

    def test_peak(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)

        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=False)

        self.assertIs(tam_buffer, film.peak())
        self.assertIs(tam_buffer, film.peak())
        self.assertIs(tam_buffer, film.slide())

        self.assertIs(tam_buffer_2, film.peak())
        self.assertIs(tam_buffer_2, film.peak())
        self.assertIs(tam_buffer_2, film.slide())

        self.assertIs(tam_buffer_3, film.peak())
        self.assertIs(tam_buffer_3, film.peak())
        self.assertIs(tam_buffer_3, film.slide())

        self.assertIs(tam_buffer_3, film.peak())
        self.assertIs(tam_buffer_3, film.peak())
        self.assertIs(tam_buffer_3, film.slide())

    def test_peak_2(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)

        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=True)

        self.assertIs(tam_buffer, film.peak())
        self.assertIs(tam_buffer, film.peak())
        self.assertIs(tam_buffer, film.slide())

        self.assertIs(tam_buffer_2, film.peak())
        self.assertIs(tam_buffer_2, film.peak())
        self.assertIs(tam_buffer_2, film.slide())

        self.assertIs(tam_buffer_3, film.peak())
        self.assertIs(tam_buffer_3, film.peak())
        self.assertIs(tam_buffer_3, film.slide())

        self.assertIs(tam_buffer, film.peak())
        self.assertIs(tam_buffer, film.peak())
        self.assertIs(tam_buffer, film.slide())

    def test_peak_3(self):
        film = tam_tools.tam_film.TAMFilm((), circular=True)
        self.assertIs(None, film.peak())

    def test_append(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        self.assertEqual(len(film), 2)
        film.append(tam_io.tam_buffer.TAMBuffer(3, 2, "Q", AQUA, WHITE))
        self.assertEqual(len(film), 3)

        film.append(tam_io.tam_buffer.TAMBuffer(3, 2, "P", AQUA, WHITE))
        self.assertEqual(len(film), 4)

    def test_pop(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)

        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=True)

        self.assertIs(film.pop(), tam_buffer_3)
        self.assertIs(film.pop(), tam_buffer_2)
        self.assertIs(film.pop(), tam_buffer)
        self.assertIs(film.pop(), None)

    def test_get_circular(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        self.assertFalse(film.get_circular())

    def test_get_circular_2(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=True)

        self.assertTrue(film.get_circular())

    def test_set_circular(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=True)

        film.set_circular(False)
        self.assertFalse(film.get_circular())

    def test_done(self):
        film = tam_tools.tam_film.TAMFilm([tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA),
                                           tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)],
                                          circular=False)

        self.assertFalse(film.done())

    def test_done_2(self):
        tam_buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", PURPLE, AQUA)
        tam_buffer_2 = tam_io.tam_buffer.TAMBuffer(4, 5, "B", BLUE, YELLOW)
        tam_buffer_3 = tam_io.tam_buffer.TAMBuffer(4, 5, "C", BLUE, YELLOW)

        film = tam_tools.tam_film.TAMFilm((tam_buffer, tam_buffer_2, tam_buffer_3), circular=False)

        self.assertFalse(film.done())
        self.assertIs(tam_buffer, next(film))
        self.assertFalse(film.done())
        self.assertIs(tam_buffer_2, next(film))
        self.assertFalse(film.done())
        self.assertIs(tam_buffer_3, next(film))
        self.assertTrue(film.done())
        self.assertIs(tam_buffer_3, next(film))

    def test_done_3(self):
        film = tam_tools.tam_film.TAMFilm((), circular=False)

        self.assertTrue(film.done())
        self.assertRaises(StopIteration, next, film)
