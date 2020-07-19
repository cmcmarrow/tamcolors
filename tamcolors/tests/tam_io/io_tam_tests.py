# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam
from tamcolors import tam_io


class IOTAMTest(unittest.TestCase):
    def test__draw_onto(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)
        buffer3 = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)

        tam_io.io_tam.IO._draw_onto(buffer, buffer2)
        buffer3.draw_onto(buffer2, 1, 1)

        self.assertEqual(str(buffer), str(buffer3))

    def test__draw_onto_2(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)
        buffer3 = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)

        buffer2.set_spot(0, 0, "C", 4, 5)
        buffer2.set_spot(1, 0, "D", 4, 5)
        buffer2.set_spot(2, 1, "E", 4, 5)
        buffer2.set_spot(2, 3, "F", 4, 5)
        buffer2.set_spot(1, 1, "G", 4, 5)

        tam_io.io_tam.IO._draw_onto(buffer, buffer2)
        buffer3.draw_onto(buffer2, 1, 1)

        self.assertEqual(str(buffer), str(buffer3))

    def test__draw_onto_3(self):
        buffer = tam.tam_buffer.TAMBuffer(50, 60, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(30, 40, "B", 1, 2)
        buffer3 = tam.tam_buffer.TAMBuffer(50, 60, "A", 1, 2)

        buffer2.set_spot(0, 0, "C", 4, 5)
        buffer2.set_spot(1, 0, "D", 4, 5)
        buffer2.set_spot(2, 1, "E", 4, 5)
        buffer2.set_spot(2, 3, "F", 4, 5)
        buffer2.set_spot(1, 1, "G", 4, 5)

        tam_io.io_tam.IO._draw_onto(buffer, buffer2)

        buffer3.draw_onto(buffer2, 10, 10)

        self.assertEqual(str(buffer), str(buffer3))
