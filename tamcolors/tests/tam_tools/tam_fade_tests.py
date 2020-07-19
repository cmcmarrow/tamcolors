# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam
from tamcolors import tam_tools


class TAMFilmFadeInTests(unittest.TestCase):
    def test_tam_fade_in(self):
        buffer = tam.tam_buffer.TAMBuffer(4, 5, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(4, 5, "&", 3, 7)
        film = tam_tools.tam_fade.tam_fade_in(buffer, "&", 3, 7)

        self.assertEqual(len(film), 24)
        self.assertEqual(buffer2, film[0])
        self.assertEqual(buffer, film[23])

    def test_tam_fade_in_2(self):
        buffer = tam.tam_buffer.TAMBuffer(4, 5, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(4, 5, "&", 3, 7)
        film = tam_tools.tam_fade.tam_fade_in(buffer, "&", 3, 7, reverse=True)

        self.assertEqual(len(film), 24)
        self.assertEqual(buffer, film[0])
        self.assertEqual(buffer2, film[23])

    def test_tam_fade_in_3(self):
        buffer = tam.tam_buffer.TAMBuffer(2, 3, "A", 1, 2)
        buffer.set_spot(1, 1, "B", 6, 9)
        buffer2 = tam.tam_buffer.TAMBuffer(2, 3, "&", 3, 7)
        film = tam_tools.tam_fade.tam_fade_in(buffer, "&", 3, 7)

        self.assertEqual(len(film), 10)
        self.assertEqual(buffer2, film[0])
        self.assertEqual(buffer, film[9])

    def test_tam_fade_in_4(self):
        buffer = tam.tam_buffer.TAMBuffer(2, 3, "A", 1, 2)
        buffer.set_spot(1, 1, "B", 6, 9)
        buffer2 = tam.tam_buffer.TAMBuffer(2, 3, "&", 3, 7)
        film = tam_tools.tam_fade.tam_fade_in(buffer, "&", 3, 7, rand=[True])

        self.assertEqual(len(film), 9)
        self.assertEqual(buffer2, film[0])
        self.assertEqual(buffer, film[8])
