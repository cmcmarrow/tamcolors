# built in libraries
import unittest
import unittest.mock

# tamcolors libraries
from tamcolors import tam


class TAMLoopTestTests(unittest.TestCase):
    def test_loop_init(self):
        frame = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)

        self.assertIsInstance(loop, tam.tam_loop_test.TAMLoopTest)

    def test_loop_call(self):
        frame = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        self.assertEqual(loop.get_running(), None)
        loop()
        self.assertEqual(loop.get_running(), True)
        loop.done()
        loop()
        self.assertEqual(loop.get_running(), False)
        loop()
        self.assertEqual(loop.get_running(), False)

    def test_done(self):
        frame = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        self.assertEqual(loop.get_running(), None)
        loop.done()
        self.assertEqual(loop.get_running(), None)
        loop()
        loop.done()
        self.assertEqual(loop.get_running(), False)

    def test_run(self):
        frame = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        self.assertEqual(loop.get_running(), None)
        loop.run()
        self.assertEqual(loop.get_running(), True)
        loop.done()
        loop.run()
        self.assertEqual(loop.get_running(), False)
        loop.run()
        self.assertEqual(loop.get_running(), False)

    def test_get_runner(self):
        frame = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        self.assertEqual(loop.get_running(), None)
        loop()
        self.assertEqual(loop.get_running(), True)

    def test_add_frame_stack(self):
        frame_1 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        frame_2 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        frame_3 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame_1)

        loop.add_frame_stack(frame_2)
        loop.add_frame_stack(frame_3)

        self.assertIs(loop.pop_frame_stack(), frame_3)
        self.assertIs(loop.pop_frame_stack(), frame_2)
        self.assertIs(loop.pop_frame_stack(), frame_1)
        self.assertIs(loop.pop_frame_stack(), None)

    def test_pop_frame_stack(self):
        frame = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)

        self.assertIs(loop.pop_frame_stack(), frame)
        self.assertIs(loop.pop_frame_stack(), None)

    def test_update(self):
        class Dummy(tam.tam_loop.TAMFrame):
            def __init__(self, update_func, draw_func, done_func, *args):
                super().__init__(*args)

                self.__update_func = update_func
                self.__draw_func = draw_func
                self.__done_func = done_func

            def update(self, tam_loop, keys, loop_data):
                self.__update_func()

            def draw(self, tam_buffer, loop_data):
                self.__draw_func()

            def done(self, tam_loop, loop_data):
                self.__done_func()

        update_func = unittest.mock.Mock()
        draw_func = unittest.mock.Mock()
        done_func = unittest.mock.Mock()
        frame = Dummy(update_func, draw_func, done_func, 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)

        loop()
        buffer_1 = loop.update((), 26, 35)[0]

        update_func.assert_called_once_with()
        draw_func.assert_called_once_with()
        self.assertEqual(done_func.call_count, 0)

        self.assertEqual(buffer_1.get_dimensions(), (26, 35))

        loop.update((), 26, 35)

        self.assertEqual(update_func.call_count, 2)
        self.assertEqual(draw_func.call_count, 2)
        self.assertEqual(done_func.call_count, 0)

        loop.update((), 0, 0)

        self.assertEqual(update_func.call_count, 3)
        self.assertEqual(draw_func.call_count, 3)
        self.assertEqual(done_func.call_count, 0)

        loop.done()
        loop.update((), 3, 4)

        self.assertEqual(update_func.call_count, 3)
        self.assertEqual(draw_func.call_count, 3)
        self.assertEqual(done_func.call_count, 1)

        loop.update((), 3, 4)

        self.assertEqual(update_func.call_count, 3)
        self.assertEqual(draw_func.call_count, 3)
        self.assertEqual(done_func.call_count, 1)

    def test_update_2(self):
        class Dummy(tam.tam_loop.TAMFrame):
            def __init__(self, update_func, draw_func, done_func, *args):
                super().__init__(*args)

                self.__update_func = update_func
                self.__draw_func = draw_func
                self.__done_func = done_func

            def update(self, tam_loop, keys, loop_data):
                self.__update_func()

            def draw(self, tam_buffer, loop_data):
                self.__draw_func()
                raise TypeError()

            def done(self, tam_loop, loop_data):
                self.__done_func()

        update_func = unittest.mock.Mock()
        draw_func = unittest.mock.Mock()
        done_func = unittest.mock.Mock()
        frame = Dummy(update_func, draw_func, done_func, 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)

        loop()
        self.assertRaises(TypeError, loop.update, (), 34, 34)

        self.assertEqual(update_func.call_count, 1)
        self.assertEqual(draw_func.call_count, 1)
        self.assertEqual(done_func.call_count, 1)

        loop.update((), 34, 34)

        self.assertEqual(update_func.call_count, 1)
        self.assertEqual(draw_func.call_count, 1)
        self.assertEqual(done_func.call_count, 1)

    def test_update_3(self):
        class Dummy(tam.tam_loop.TAMFrame):
            def __init__(self, *args):
                super().__init__(*args)

            def update(self, tam_loop, keys, loop_data):
                for key in keys:
                    if key == ("Q", "NORMAL"):
                        tam_loop.done()

            def draw(self, tam_buffer, loop_data):
                pass

        frame = Dummy(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        loop()

        loop.update((), 23, 23)
        self.assertTrue(loop.get_running())

        loop.update((("q", "NORMAL"), ("1", "NORMAL")), 23, 23)
        self.assertTrue(loop.get_running())

        loop.update((("q", "NORMAL"),), 23, 23)
        self.assertTrue(loop.get_running())

        loop.update((("Q", "NORMAL"),), 23, 23)
        self.assertFalse(loop.get_running())

    def test_update_4(self):
        frame_1 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        frame_2 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        frame_3 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)

        loop = tam.tam_loop_test.TAMLoopTest(frame_1)

        loop()
        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_1)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_1)

        loop.add_frame_stack(frame_2)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        loop.add_frame_stack(frame_3)
        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_3)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_3)

        loop.pop_frame_stack()

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        loop.pop_frame_stack()

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_1)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_1)

        loop.pop_frame_stack()

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, None)

    @staticmethod
    def _get_dummy_frame(*args, **kwargs):
        class Dummy(tam.tam_loop.TAMFrame):
            def __init__(self):
                super().__init__(*args, **kwargs)

            def update(self, tam_loop, keys, loop_data):
                pass

            def draw(self, tam_buffer, loop_data):
                pass

        return Dummy()

    def test_get_color(self):
        frame_1 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame_1)
        loop()
        for spot in range(16):
            color = loop.get_color(spot)
            self.assertIsInstance(color, (list, tuple))
            self.assertEqual(len(color), 3)
            for value in range(3):
                self.assertIsInstance(color[value], int)

    def test_set_color(self):
        frame_1 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame_1)
        loop()

        loop.set_color(5, (55, 66, 77))
        color = loop.get_color(5)

        self.assertEqual(color, (55, 66, 77))
        loop.set_tam_color_defaults()

    def test_set_color_2(self):
        frame_1 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame_1)
        loop()

        loop.set_color(1, (155, 166, 177))
        color = loop.get_color(1)

        self.assertEqual(color, (155, 166, 177))
        loop.set_tam_color_defaults()

    def test_reset_colors_to_console_defaults(self):
        frame_1 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame_1)
        loop()
        loop.reset_colors_to_console_defaults()

    def test_set_tam_color_defaults(self):
        frame_1 = self._get_dummy_frame(5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame_1)
        loop()
        loop.set_tam_color_defaults()
