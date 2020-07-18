# built in libraries
import traceback
import threading
import time
import sys
import itertools

# Charles McMarrow libraries
from tamcolors import checks
from tamcolors.tests import stability_check
from .tma_buffer import TMABuffer
from . import any_tma
from . import tma_loop_test

# Charles McMarrow

"""
TMALoop
Handlers FPS, Key input, drawing, updating and TMAFrame stack

TMAFrame
Holds information about frame
Colors, min and max size
"""


class TMALoopError(Exception):
    pass


class TMALoop:
    def __init__(self,
                 tma_frame,
                 io_list=None,
                 any_os=False,
                 only_any_os=False,
                 buffer_count=3,
                 color_change_key="ESCAPE",
                 loop_data=None):
        """
        info: makes a TMALoop object
        :param tma_frame: TMAFrame: first frame in tam loop
        :param io_list: list, tuple, None: ios that can be used
        :param any_os: bool: will use ANYIO if no other IO can be used if True
        :param only_any_os: bool: will only use ANYIO if True
        :param buffer_count: int: 1 - inf
        :param color_change_key: char: key that will change color mode
        :param loop_data: dict
        """

        if loop_data is None:
            loop_data = {}

        # checks
        checks.checks.instance_check(tma_frame, TMAFrame, TMALoopError)
        checks.checks.instance_check(any_os, bool, TMALoopError)
        checks.checks.range_check(buffer_count, 1, None, TMALoopError)
        checks.checks.instance_check(color_change_key, str, TMALoopError)
        checks.checks.instance_check(loop_data, dict, TMALoopError)

        if not stability_check.tma_stability_check():
            test_results = stability_check.tma_stability_check(ret_bool=False)
            raise TMALoopError("TMA is corrupted! {0} out of {1} tests passed".format(*test_results))

        self.__running = None
        self.__draw_loop_thread = None
        self.__key_loop_thread = None
        self.__error = None

        if only_any_os:
            self.__io = any_tma.AnyIO.get_io()
        else:
            self.__io = any_tma.get_io(io_list=io_list, any_os=any_os)
            if self.__io is None:
                raise TMALoopError("tam io is None")

        self.__frame_stack = [tma_frame]
        self.__loop_data = loop_data
        self.__input_keys = []

        self.__update_ready_buffers = [TMABuffer(0, 0, " ", 0, 0) for _ in range(buffer_count)]
        self.__draw_ready_buffers = []

        self.__color_change_key = color_change_key
        self.__color_modes = itertools.cycle(self.__io.get_modes())

    def __call__(self):
        """
        info: will run tam loop
        :return:
        """
        if self.__running is not None:
            return

        self.__running = True
        self.__io.start()

        self.__draw_loop_thread = threading.Thread(target=self._draw_loop, daemon=True)
        self.__key_loop_thread = threading.Thread(target=self._key_loop, daemon=True)

        self.__draw_loop_thread.start()
        self.__key_loop_thread.start()

        self._update_loop()

        if self.__error is not None:
            raise self.__error

    def done(self):
        """
        info: will stop tam loop
        :return:
        """
        if self.__running:
            self.__running = False

            self.__draw_loop_thread.join()
            self.__key_loop_thread.join()
            self.__io.done()

    def run(self):
        """
        info: will call tam loop
        :return:
        """
        self()

    @staticmethod
    def run_application(*args, **kwargs):
        """
        info: will run tam loop as an application
        note:
            when tam loop is done running the program will quit
            if tam loop has an error and the frame does not catch it
            the error will be printed onto the screen and the program will quit
            after user input
        :param args:
        :param kwargs:
        :return:
        """
        try:
            loop = TMALoop(*args, **kwargs)
            loop()
        except KeyboardInterrupt:
            pass
        except BaseException as error:
            try:
                traceback.print_exception(error.__class__, error, sys.exc_info()[2])
                time.sleep(1)
                input("Press Enter To Continue . . .")
            except KeyboardInterrupt:
                pass
        finally:
            sys.exit()

    def get_running(self):
        """
        info: None has not ran, True is running, False has ran
        :return: bool or None
        """

        return self.__running

    def add_frame_stack(self, frame):
        """
        info: will add a TMAFrame to stack
        :param frame: TMAFrame
        :return:
        """

        # checks
        checks.checks.instance_check(frame, TMAFrame, TMALoopError)

        self.__frame_stack.append(frame)

    def pop_frame_stack(self):
        """
        info: will remove TMAFrame from stack
        :return: TMAFrame or None
        """

        if len(self.__frame_stack) != 0:
            frame = self.__frame_stack.pop()
            frame.done(self, self.__loop_data)
            return frame

    def _update_loop(self):
        """
        info: will update frame and call draw
        :return:
        """

        frame = None
        try:
            while self.__running and self.__error is None and len(self.__frame_stack) != 0:
                start_time = time.time()
                frame = self.__frame_stack[-1]
                frame_time = 1/frame.get_fps()
                keys = self.__input_keys.copy()
                self.__input_keys.clear()

                frame.update(self, keys, self.__loop_data)

                if len(self.__update_ready_buffers) != 0:
                    tma_buffer = frame.make_buffer_ready(self.__update_ready_buffers.pop(0),
                                                         *self.__io.get_dimensions())
                    frame.draw(tma_buffer, self.__loop_data)
                    self.__draw_ready_buffers.append(tma_buffer)

                time.sleep(max(frame_time - (time.time() - start_time), 0))
        except BaseException as error:
            self.__error = error
            self.done()
        finally:
            if frame is not None:
                frame.done(self, self.__loop_data)
            self.done()

    def _draw_loop(self):
        """
        info: will draw TMABuffer
        :return:
        """

        try:
            while self.__running:
                if len(self.__draw_ready_buffers) != 0:
                    tma_buffer = self.__draw_ready_buffers.pop(0)
                    self.__io.draw(tma_buffer)
                    self.__update_ready_buffers.append(tma_buffer)
                time.sleep(0.0001)
        except BaseException as error:
            self.__error = error

    def _key_loop(self):
        """
        info: will get key input
        :return:
        """

        try:
            while self.__running:
                key = self.__io.get_key()
                if key is not False:
                    if key[0] == self.__color_change_key:
                        self.__io.set_mode(next(self.__color_modes))
                    else:
                        self.__input_keys.append(key)
                time.sleep(0.0001)
        except BaseException as error:
            self.__error = error


class TMAFrame:
    def __init__(self,
                 frame,
                 fps,
                 char,
                 foreground_color,
                 background_color,
                 min_width=0,
                 max_width=1000,
                 min_height=0,
                 max_height=1000):
        """
        info: makes a TMAFrame object
        :param frame: object
        :param fps: int or float: 0.0 - inf
        :param char: str: len of 1
        :param foreground_color: int: 0 - inf
        :param background_color: int: 0 - inf
        :param min_width: int: 0 - inf
        :param max_width: int: min_width - inf
        :param min_height: int: 0 - inf
        :param max_height: int: min_height - inf
        """
        # checks
        checks.checks.in_instances_check(fps, (int, float), TMALoopError)
        checks.checks.range_check(int(fps), 0, None)
        checks.checks.single_block_char_check(char, TMALoopError)
        checks.checks.range_check(foreground_color, 0, None, TMALoopError)
        checks.checks.range_check(background_color, 0, None, TMALoopError)
        checks.checks.range_check(max_width, 0, None, TMALoopError)
        checks.checks.range_check(max_height, 0, None, TMALoopError)
        checks.checks.range_check(min_width, 0, max_width + 1, TMALoopError)
        checks.checks.range_check(min_height, 0, max_height + 1, TMALoopError)

        self.__frame = frame
        self.__fps = fps

        self.__char = char
        self.__foreground_color = foreground_color
        self.__background_color = background_color

        self.__min_width = min_width
        self.__max_width = max_width

        self.__min_height = min_height
        self.__max_height = max_height

        self.__done_called = False

    def get_fps(self):
        """
        info: returns the frame fps
        :return: int
        """
        return self.__fps

    def get_defaults(self):
        """
        info: gets defaults
        :return: (str, int, int)
        """
        return self.__char, self.__foreground_color, self.__background_color

    def get_width_min_and_max(self):
        """
        info: returns min and max width
        :return: (int, int)
        """
        return self.__min_width, self.__max_width

    def get_height_min_and_max(self):
        """
        info: returns min and max height
        :return: (int, int)
        """
        return self.__min_height, self.__max_height

    def make_buffer_ready(self, tma_buffer, screen_width, screen_height):
        """
        info: will make buffer ready for frame
        :param tma_buffer: TMABuffer
        :param screen_width: int: 0 - inf
        :param screen_height: int: 0 - inf
        :return:
        """
        # checks
        checks.checks.instance_check(tma_buffer, TMABuffer, TMALoopError)
        checks.checks.range_check(screen_width, 0, None, TMALoopError)
        checks.checks.range_check(screen_height, 0, None, TMALoopError)

        if (self.__char, self.__foreground_color, self.__background_color) != tma_buffer.get_defaults():
            tma_buffer.set_defaults_and_clear(self.__char, self.__foreground_color, self.__background_color)

        width = min(max(self.__min_width, screen_width), self.__max_width)
        height = min(max(self.__min_height, screen_height), self.__max_height)
        if (width, height) != tma_buffer.get_dimensions():
            tma_buffer.set_dimensions_and_clear(width, height)

        return tma_buffer

    def update(self, tma_loop, keys, loop_data):
        """
        info: will update terminal
        :param tma_loop: TMALoop
        :param keys: list, tuple
        :param loop_data: dict
        :return:
        """
        # checks
        checks.checks.in_instances_check(tma_loop, (TMALoop, tma_loop_test.TMALoopTest), TMALoopError)
        checks.checks.instance_check(keys, (list, tuple), TMALoopError)
        checks.checks.instance_check(loop_data, dict, TMALoopError)
        # check self.__frame.update
        checks.checks.has_method_check(self.__frame, "update", TMALoopError)

        self.__frame.update(tma_loop, keys, loop_data)

    def draw(self, tma_buffer, loop_data):
        """
        info: will draw frame onto terminal
        :param tma_buffer: TMABuffer
        :param loop_data: dict
        :return:
        """
        # checks
        checks.checks.instance_check(tma_buffer, TMABuffer, TMALoopError)
        checks.checks.instance_check(loop_data, dict, TMALoopError)
        # check self.__frame.draw
        checks.checks.has_method_check(self.__frame, "draw", TMALoopError)

        self.__frame.draw(tma_buffer, loop_data)

    def done(self, tma_loop, loop_data):
        """
        info: will clean up the frame and can only be called once
        :param tma_loop: TMALoop
        :param loop_data: dict
        :return:
        """
        # checks
        checks.checks.in_instances_check(tma_loop, (TMALoop, tma_loop_test.TMALoopTest), TMALoopError)
        checks.checks.instance_check(loop_data, dict, TMALoopError)
        # check self.__frame.done
        checks.checks.has_method_check(self.__frame, "done", TMALoopError)

        if not self.__done_called:
            self.__done_called = True
            self.__frame.done(tma_loop, loop_data)
