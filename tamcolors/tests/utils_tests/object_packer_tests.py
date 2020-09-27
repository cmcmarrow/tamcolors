# built in libraries
import unittest

# tamcolors libraries
from tamcolors.tam_io import tam_buffer, tam_colors
from tamcolors.utils import object_packer


class ObjectPackerFunctionsTests(unittest.TestCase):
    def test_save_and_load_int_1(self):
        self.assertEqual(object_packer.load_int(bytearray(object_packer.save_int(0))), 0)

    def test_save_and_load_int_2(self):
        self.assertEqual(object_packer.load_int(bytearray(object_packer.save_int(255))), 255)

    def test_save_and_load_int_3(self):
        number = 230984570984312578190234719803475980273549023875092385471111111111111111110000001234141241242141241234
        self.assertEqual(object_packer.load_int(bytearray(object_packer.save_int(number))), number)

    def test_save_and_load_int_4(self):
        for number in range(100000):
            self.assertEqual(object_packer.load_int(bytearray(object_packer.save_int(number))), number)

    def test_save_and_load_data_1(self):
        data = bytes()
        self.assertEqual(object_packer.load_data(bytearray(object_packer.save_data(data))), data)

    def test_save_and_load_data_2(self):
        data = bytes((1, 2, 3, 4, 5, 56))
        self.assertEqual(object_packer.load_data(bytearray(object_packer.save_data(data))), data)

    def test_save_and_load_data_3(self):
        data = bytes((0, 0, 4, 5, 200, 255, 1, 2, 3, 4))
        self.assertEqual(object_packer.load_data(bytearray(object_packer.save_data(data))), data)

    def test_save_and_load_data_4(self):
        data = bytes([i % 256 for i in range(10000)])
        self.assertEqual(object_packer.load_data(bytearray(object_packer.save_data(data))), data)


class FastHandObjectPackerTests(unittest.TestCase):
    def test_tam_color_1(self):
        self.assertEqual(tam_colors.Color.start_from_bytes(tam_colors.RED.to_bytes()), tam_colors.RED)

    def test_tam_color_2(self):
        self.assertEqual(tam_colors.Color.start_from_bytes(tam_colors.BLUE.to_bytes()), tam_colors.BLUE)

    def test_tam_buffer_1(self):
        buffer = tam_buffer.TAMBuffer(98, 591, "A", tam_colors.COLOR_142, tam_colors.COLOR_149)
        buffer.set_spot(10, 9, "C", tam_colors.RED, tam_colors.AQUA)
        buffer.set_spot(55, 300, "V", tam_colors.AQUA, tam_colors.COLOR_68)

        self.assertEqual(tam_buffer.TAMBuffer.start_from_bytes(buffer.to_bytes()), buffer)

    def test_tam_buffer_2(self):
        buffer = tam_buffer.TAMBuffer(70, 91, "B", tam_colors.COLOR_145, tam_colors.COLOR_100)
        buffer.set_spot(15, 9, "C", tam_colors.RED, tam_colors.AQUA)
        buffer.set_spot(55, 0, "V", tam_colors.AQUA, tam_colors.COLOR_68)

        self.assertEqual(tam_buffer.TAMBuffer.start_from_bytes(buffer.to_bytes()), buffer)

    def test_dunder_bytes(self):
        self.assertEqual(tam_colors.GREEN.to_bytes(), bytes(tam_colors.GREEN))


class ObjectPackerJsonTests(unittest.TestCase):
    def test_none(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, None)

    def test_bool(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, True)

    def test_str(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, "cats")

    def test_int(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, -44)

    def test_float(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, -44.0)

    def test_tuple(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, (-44, 44.0, "cats", None, True, False))

    def test_list(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, [-44, 44.0, "cats", None, True, False])

    def test_set(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, {-44, 44.0, "cats", None, True, False})

    def test_dict(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, {-44: -44, 44.0: "lol", "cats": "dogs", None: "None", True: False, False: True})

    def test_bytes(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, bytes((1, 200, 3, 44, 5)))

    def test_bytearray(self):
        op = object_packer.ObjectPackerJson()
        self._dump_and_check(op, bytearray((100, 2, 3, 4, 55)))

    def test_fast_hand_object(self):
        op = object_packer.ObjectPackerJson((tam_buffer.TAMBuffer, tam_colors.Color, tam_colors.RGBA))
        self._dump_and_check(op, tam_buffer.TAMBuffer(55, 67, "!", tam_colors.RED, tam_colors.GREEN))
        self._dump_and_check(op, tam_buffer.TAMBuffer(21, 53, "C", tam_colors.BLUE, tam_colors.YELLOW))

    def test_large_data(self):
        op = object_packer.ObjectPackerJson((tam_buffer.TAMBuffer, tam_colors.Color, tam_colors.RGBA))
        data = [{"dict": {"buffer 1": tam_buffer.TAMBuffer(55, 67, "!", tam_colors.RED, tam_colors.GREEN),
                          "data": (bytearray((4, 5, 6, 7, 90)), bytes(), bytearray()),
                          "buffer 2": tam_buffer.TAMBuffer(53, 1, ")", tam_colors.LIGHT_YELLOW, tam_colors.GRAY)}},
                {1, 2, 3, 4, "1", "4.4", None, (True, False)},
                [tam_colors.COLOR_145, tam_colors.COLOR_142, tam_colors.COLOR_149, "cats and dogs"],
                (4, 5, (90, -3, "3", [])),
                None,
                False,
                True,
                "this is a test",
                0.00001,
                tam_colors.COLOR_142,
                bytes((1, 2, 3, 4, 5, 6, 66, 55, 88, 12))]

        self._dump_and_check(op, data)

    def _dump_and_check(self, object_packer_json, data):
        data_ret = object_packer_json.loads(object_packer_json.dumps(data))
        self.assertEqual(type(data), type(data_ret))
        self.assertEqual(object_packer_json.loads(object_packer_json.dumps(data)), data)
