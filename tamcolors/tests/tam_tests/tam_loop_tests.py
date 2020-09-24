# built in libraries
import threading
import unittest
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors import tam
from tamcolors.tam_io.tam_colors import *


class TAMLoopTests(unittest.TestCase):
    def test_loop_init(self):
        frame = self._get_dummy_frame(5, "A", YELLOW, BLUE, 25, 35, 26, 36)
        tam.tam_loop.TAMLoop(frame, only_any_os=True)

    def test_run(self):
        frame = self._get_dummy_frame(5, "A", YELLOW, BLUE, 25, 35, 26, 36)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(threading.Thread, "start", return_value=None) as start:
            with unittest.mock.patch.object(threading.Thread, "join", return_value=None) as join:
                with unittest.mock.patch.object(frame, "done", return_value=None) as done:
                    loop.run()

                    self.assertEqual(start.call_count, 1)
                    self.assertEqual(start.mock_calls[0], unittest.mock.call())

                    self.assertEqual(join.call_count, 1)
                    self.assertEqual(join.mock_calls[0], unittest.mock.call())

                    done.assert_called_once_with(loop, {})

    def test_stack(self):
        frame = self._get_dummy_frame(5, "A", YELLOW, BLUE, 25, 35, 26, 36)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        frame2 = self._get_dummy_frame(5, "B", YELLOW, BLUE, 25, 35, 26, 36)

        with unittest.mock.patch.object(frame2, "done", return_value=True) as done:
            loop.add_frame_stack(frame2)
            loop.pop_frame_stack()

            done.assert_called_once_with(loop, {})

    @staticmethod
    def _get_dummy_frame(*args, **kwargs):
        class Dummy(tam.tam_loop.TAMFrame):
            def __init__(self):
                super().__init__(*args, **kwargs)

            def update(self, tam_loop, keys, loop_data):
                tam_loop.done()

            def draw(self, tam_buffer, loop_data):
                pass

        return Dummy()

    def test_reset_colors_to_console_defaults(self):
        frame_1 = self._get_dummy_frame(5, "A", YELLOW, BLUE, 25, 35, 26, 36)
        loop = tam.tam_loop.TAMLoop(frame_1, only_any_os=True)
        loop()
        loop.reset_colors_to_console_defaults()

    def test_set_tam_color_defaults(self):
        frame_1 = self._get_dummy_frame(5, "A", YELLOW, BLUE, 25, 35, 26, 36)
        loop = tam.tam_loop.TAMLoop(frame_1, only_any_os=True)
        loop()
        loop.set_tam_color_defaults()

    def test_step(self):
        class Dummy(tam.tam_loop.TAMFrame):
            def __init__(self):
                super().__init__(5, "A", YELLOW, BLUE, 25, 35, 26, 36)
                self._q = False

            def update(self, tam_loop, keys, loop_data):
                self._q = bool(len(keys))

            def draw(self, tam_buffer, loop_data):
                tam_buffer.clear()
                if self._q:
                    tam_buffer.set_spot(0, 0, "C", RED, GREEN)

            def done(self, tam_loop, loop_data):
                pass

        frame = Dummy()
        with unittest.mock.patch.object(frame, "done", return_value=None) as done:
            loop = tam.tam_loop.TAMLoop(frame, test_mode=True)
            self.assertIsNone(loop.step())
            loop()
            self.assertIsInstance(loop.step(), tam_io.tam_buffer.TAMBuffer)
            buffer = loop.step(("A", "NORMAL"))
            self.assertIsInstance(buffer, tam_io.tam_buffer.TAMBuffer)
            self.assertEqual(buffer.get_spot(0, 0), ("C", RED, GREEN))
            buffer = loop.step()
            self.assertIsInstance(buffer, tam_io.tam_buffer.TAMBuffer)
            self.assertEqual(buffer.get_spot(0, 0), ("A", YELLOW, BLUE))
            loop.done()
            done.assert_called_once()
            self.assertIsNone(loop.step())


class TAMFrameTests(unittest.TestCase):
    def test_frame_init(self):
        self._get_dummy_frame(5, "A", YELLOW, BLUE, 25, 35, 26, 36)

    def test_get_fps(self):
        frame = self._get_dummy_frame(5, "A", YELLOW, BLUE, 25, 35, 26, 36)
        self.assertEqual(frame.get_fps(), 5)

    def test_get_fps_2(self):
        frame = self._get_dummy_frame(10, "A", YELLOW, BLUE, 25, 35, 26, 36)
        self.assertEqual(frame.get_fps(), 10)

    def test_get_defaults(self):
        frame = self._get_dummy_frame(10, "A", YELLOW, BLUE, 25, 35, 26, 36)
        self.assertEqual(frame.get_defaults(), ("A", YELLOW, BLUE))

    def test_get_defaults_2(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 25, 35, 26, 36)
        self.assertEqual(frame.get_defaults(), ("C", PURPLE, GRAY))

    def test_get_width_min_and_max(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 25, 35, 26, 36)
        self.assertEqual(frame.get_width_min_and_max(), (25, 35))

    def test_get_width_min_and_max_2(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 15, 45, 26, 36)
        self.assertEqual(frame.get_width_min_and_max(), (15, 45))

    def test_get_height_min_and_max(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 25, 35, 26, 36)
        self.assertEqual(frame.get_height_min_and_max(), (26, 36))

    def test_get_height_min_and_max_2(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 15, 45, 47, 58)
        self.assertEqual(frame.get_height_min_and_max(), (47, 58))

    def test_make_buffer_ready(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 15, 45, 47, 58)
        buffer = tam_io.tam_buffer.TAMBuffer(30, 32, "C", RED, GREEN)
        frame.make_buffer_ready(buffer, 46, 59)
        self.assertEqual(buffer.get_dimensions(), (45, 58))

    def test_make_buffer_ready_2(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 15, 45, 47, 58)
        buffer = tam_io.tam_buffer.TAMBuffer(30, 32, "C", RED, GREEN)
        frame.make_buffer_ready(buffer, 1, 2)
        self.assertEqual(buffer.get_dimensions(), (15, 47))

    def test_make_buffer_ready_3(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 15, 45, 47, 58)
        buffer = tam_io.tam_buffer.TAMBuffer(30, 32, "C", RED, GREEN)
        frame.make_buffer_ready(buffer, 33, 48)
        self.assertEqual(buffer.get_dimensions(), (33, 48))

    def test_update(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 15, 45, 47, 58)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(frame, "update", return_value=None) as update:
            frame.update(loop, (), {})
            update.assert_called_once_with(loop, (), {})

    def test_draw(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 15, 45, 47, 58)
        buffer = tam_io.tam_buffer.TAMBuffer(30, 32, "C", RED, GREEN)
        with unittest.mock.patch.object(frame, "draw", return_value=None) as draw:
            frame.draw(buffer, {})
            draw.assert_called_once_with(buffer, {})

    def test__done(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 15, 45, 47, 58)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(frame, "done", return_value=None) as done:
            frame._done(loop, {})
            done.assert_called_once_with(loop, {})

    def test__done_2(self):
        frame = self._get_dummy_frame(10, "C", PURPLE, GRAY, 15, 45, 47, 58)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(frame, "done", return_value=None) as done:
            frame._done(loop, {})
            frame._done(loop, {})
            done.assert_called_once_with(loop, {})

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
