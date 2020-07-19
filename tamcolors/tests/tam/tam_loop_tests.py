# built in libraries
import threading
import unittest
import unittest.mock

# tamcolors libraries
from tamcolors import tam


class TAMLoopTests(unittest.TestCase):
    def test_loop_init(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        tam.tam_loop.TAMLoop(frame, only_any_os=True)

    def test_run(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(threading.Thread, "start", return_value=None) as start:
            with unittest.mock.patch.object(threading.Thread, "join", return_value=None) as join:
                with unittest.mock.patch.object(dummy, "done", return_value=None) as done:
                    loop.run()

                    self.assertEqual(start.call_count, 2)
                    self.assertEqual(start.mock_calls[0], unittest.mock.call())
                    self.assertEqual(start.mock_calls[1], unittest.mock.call())

                    self.assertEqual(join.call_count, 2)
                    self.assertEqual(join.mock_calls[0], unittest.mock.call())
                    self.assertEqual(join.mock_calls[1], unittest.mock.call())

                    done.assert_called_once_with(loop, {})

    def test_stack(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        dummy2 = self._get_dummy_frame()
        frame2 = tam.tam_loop.TAMFrame(dummy2, 5, "B", 3, 4, 25, 35, 26, 36)

        with unittest.mock.patch.object(dummy2, "done", return_value=True) as done:
            loop.add_frame_stack(frame2)
            loop.pop_frame_stack()

            done.assert_called_once_with(loop, {})

    @staticmethod
    def _get_dummy_frame():
        class Dummy:
            def __init__(self):
                pass

            def update(self, tam_loop, keys, loop_data):
                tam_loop.done()

            def draw(self, tam_buffer, loop_data):
                pass

            def done(self, tam_loop, loop_data):
                pass

        return Dummy()


class TAMFrameTests(unittest.TestCase):
    def test_frame_init(self):
        tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)

    def test_get_fps(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        self.assertEqual(frame.get_fps(), 5)

    def test_get_fps_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "A", 3, 4, 25, 35, 26, 36)
        self.assertEqual(frame.get_fps(), 10)

    def test_get_defaults(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "A", 3, 4, 25, 35, 26, 36)
        self.assertEqual(frame.get_defaults(), ("A", 3, 4))

    def test_get_defaults_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 25, 35, 26, 36)
        self.assertEqual(frame.get_defaults(), ("C", 5, 8))

    def test_get_width_min_and_max(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 25, 35, 26, 36)
        self.assertEqual(frame.get_width_min_and_max(), (25, 35))

    def test_get_width_min_and_max_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 26, 36)
        self.assertEqual(frame.get_width_min_and_max(), (15, 45))

    def test_get_height_min_and_max(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 25, 35, 26, 36)
        self.assertEqual(frame.get_height_min_and_max(), (26, 36))

    def test_get_height_min_and_max_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 47, 58)
        self.assertEqual(frame.get_height_min_and_max(), (47, 58))

    def test_make_buffer_ready(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 47, 58)
        buffer = tam.tam_buffer.TAMBuffer(30, 32, "C", 1, 2)
        frame.make_buffer_ready(buffer, 46, 59)
        self.assertEqual(buffer.get_dimensions(), (45, 58))

    def test_make_buffer_ready_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 47, 58)
        buffer = tam.tam_buffer.TAMBuffer(30, 32, "C", 1, 2)
        frame.make_buffer_ready(buffer, 1, 2)
        self.assertEqual(buffer.get_dimensions(), (15, 47))

    def test_make_buffer_ready_3(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 47, 58)
        buffer = tam.tam_buffer.TAMBuffer(30, 32, "C", 1, 2)
        frame.make_buffer_ready(buffer, 33, 48)
        self.assertEqual(buffer.get_dimensions(), (33, 48))

    def test_update(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 10, "C", 5, 8, 15, 45, 47, 58)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(dummy, "update", return_value=None) as update:
            frame.update(loop, (), {})
            update.assert_called_once_with(loop, (), {})

    def test_draw(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 10, "C", 5, 8, 15, 45, 47, 58)
        buffer = tam.tam_buffer.TAMBuffer(30, 32, "C", 1, 2)
        with unittest.mock.patch.object(dummy, "draw", return_value=None) as draw:
            frame.draw(buffer, {})
            draw.assert_called_once_with(buffer, {})

    def test_done(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 10, "C", 5, 8, 15, 45, 47, 58)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(dummy, "done", return_value=None) as done:
            frame.done(loop, {})
            done.assert_called_once_with(loop, {})

    def test_done_2(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 10, "C", 5, 8, 15, 45, 47, 58)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(dummy, "done", return_value=None) as done:
            frame.done(loop, {})
            frame.done(loop, {})
            done.assert_called_once_with(loop, {})

    @staticmethod
    def _get_dummy_frame():
        class Dummy:
            def __init__(self):
                pass

            def update(self, tam_loop, keys, loop_data):
                pass

            def draw(self, tam_buffer, loop_data):
                pass

            def done(self, tam_loop, loop_data):
                pass

        return Dummy()
