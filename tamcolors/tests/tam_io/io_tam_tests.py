# built in libraries
import sys
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


class IOTAMTest(unittest.TestCase):
    def test__draw_onto(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)
        buffer3 = tam_io.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)

        tam_io.io_tam.IO._draw_onto(buffer, buffer2)
        buffer3.draw_onto(buffer2, 1, 1)

        self.assertEqual(str(buffer), str(buffer3))

    def test__draw_onto_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)
        buffer3 = tam_io.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)

        buffer2.set_spot(0, 0, "C", 4, 5)
        buffer2.set_spot(1, 0, "D", 4, 5)
        buffer2.set_spot(2, 1, "E", 4, 5)
        buffer2.set_spot(2, 3, "F", 4, 5)
        buffer2.set_spot(1, 1, "G", 4, 5)

        tam_io.io_tam.IO._draw_onto(buffer, buffer2)
        buffer3.draw_onto(buffer2, 1, 1)

        self.assertEqual(str(buffer), str(buffer3))

    def test__draw_onto_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(50, 60, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(30, 40, "B", 1, 2)
        buffer3 = tam_io.tam_buffer.TAMBuffer(50, 60, "A", 1, 2)

        buffer2.set_spot(0, 0, "C", 4, 5)
        buffer2.set_spot(1, 0, "D", 4, 5)
        buffer2.set_spot(2, 1, "E", 4, 5)
        buffer2.set_spot(2, 3, "F", 4, 5)
        buffer2.set_spot(1, 1, "G", 4, 5)

        tam_io.io_tam.IO._draw_onto(buffer, buffer2)

        buffer3.draw_onto(buffer2, 10, 10)

        self.assertEqual(str(buffer), str(buffer3))

    @staticmethod
    def test__write_to_output_stream():
        with unittest.mock.patch.object(sys.stdout, "write") as write_stdout:
            with unittest.mock.patch.object(sys.stdout, "flush") as flush_stdout:
                with unittest.mock.patch.object(sys.stderr, "write") as write_stderr:
                    with unittest.mock.patch.object(sys.stderr, "flush") as flush_stderr:
                        tam_io.io_tam.IO._write_to_output_stream("cats", True, False)
                        write_stdout.assert_called_once_with("cats")
                        flush_stdout.assert_called_once_with()
                        write_stderr.assert_not_called()
                        flush_stderr.assert_not_called()

    @staticmethod
    def test__write_to_output_stream_2():
        with unittest.mock.patch.object(sys.stdout, "write") as write_stdout:
            with unittest.mock.patch.object(sys.stdout, "flush") as flush_stdout:
                with unittest.mock.patch.object(sys.stderr, "write") as write_stderr:
                    with unittest.mock.patch.object(sys.stderr, "flush") as flush_stderr:
                        tam_io.io_tam.IO._write_to_output_stream("dogs", False, True)
                        write_stdout.assert_not_called()
                        flush_stdout.assert_not_called()
                        write_stderr.assert_called_once_with("dogs")
                        flush_stderr.assert_not_called()


class SingletonIOTest(unittest.TestCase):
    def test_same_instance(self):
        class DUMMYIO(tam_io.io_tam.SingletonIO):
            @classmethod
            def able_to_execute(cls):
                return True

        instance = DUMMYIO()
        self.assertIsInstance(instance, DUMMYIO)
        self.assertIs(instance, DUMMYIO())
        self.assertIs(instance, DUMMYIO())

    def test_same_instance_2(self):
        class DUMMYIO2(tam_io.io_tam.SingletonIO):
            @classmethod
            def able_to_execute(cls):
                return True

        instance = DUMMYIO2()
        self.assertIsInstance(instance, DUMMYIO2)
        self.assertIs(instance, DUMMYIO2())
        self.assertIs(instance, DUMMYIO2())

    def test_not_able_to_execute(self):
        class DUMMYIO(tam_io.io_tam.SingletonIO):
            @classmethod
            def able_to_execute(cls):
                return False

        instance = DUMMYIO()
        self.assertIsNone(instance)
        self.assertIs(instance, DUMMYIO())
        self.assertIs(instance, DUMMYIO())
