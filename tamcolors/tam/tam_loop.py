# built in libraries
import traceback
import threading
import time
import sys
import itertools

# tamcolors libraries
from tamcolors.tests import all_tests
from tamcolors.tam_io.tam_buffer import TAMBuffer
from tamcolors.tam_io import tam_identifier
from tamcolors.utils import timer


"""
TAMLoop
Handlers FPS, Key input, drawing, updating and TAMFrame stack

TAMFrame
Holds information about frame
Colors, min and max size
"""


class TAMLoopError(Exception):
    pass


class TAMLoop:
    def __init__(self,
                 tam_frame,
                 io=None,
                 only_any_os=False,
                 color_change_key="ESCAPE",
                 loop_data=None,
                 stability_check=False,
                 tam_color_defaults=True,
                 highest_mode_lock=False,
                 test_mode=False):
        """
        info: makes a TAMLoop object
        :param tam_frame: TAMFrame: first frame in tam loop
        :param io: IO
        :param only_any_os: bool: will only use Any Drivers if True
        :param color_change_key: char: key that will change color mode
        :param loop_data: dict: will hold context so all TAMFrames can see
        :param stability_check: bool: raises and error if a test did not pass
        :param tam_color_defaults: bool
        :param highest_mode_lock: bool: will disable change key and put IO in its highest color mode
        :param test_mode: bool: Will enable the method step and only any os
        """

        if loop_data is None:
            loop_data = {}

        if stability_check and not all_tests.stability_check():
            test_results = all_tests.stability_check(ret_bool=False)
            raise TAMLoopError("TAM is corrupted! {0} out of {1} tests passed".format(*test_results))

        self.__running = None
        self.__draw_loop_thread = None
        self.__key_loop_thread = None
        self.__error = None

        if only_any_os or test_mode:
            self.__io = tam_identifier.ANY_IO
        else:
            self.__io = io
            if io is None:
                self.__io = tam_identifier.IO

            if self.__io is None:
                raise TAMLoopError("tam io is None")

        self.__frame_stack = [tam_frame]
        self.__loop_data = loop_data
        self.__input_keys = []

        self.__color_change_key = color_change_key
        self.__color_modes = itertools.cycle(self.__io.get_modes())
        if highest_mode_lock:
            self.__color_modes = itertools.cycle(self.__io.get_modes()[0:1])

        self.__test_mode = test_mode

        if tam_color_defaults and not self.__test_mode:
            self.__io.set_tam_color_defaults()

    def __call__(self):
        """
        info: will run tam loop
        :return:
        """
        if self.__running is not None:
            return

        self.__running = True
        if not self.__test_mode:
            self.__io.start()

            self.__key_loop_thread = threading.Thread(target=self._key_loop, daemon=True)
            self.__key_loop_thread.start()

            self._update_loop()

            if self.__error is not None:
                raise self.__error

    def done(self, reset_colors_to_console_defaults=True):
        """
        info: will stop tam loop
        :param: reset_colors_to_console_defaults: bool
        :return:
        """
        if self.__running:
            self.__running = False
            for frame in self.__frame_stack[::-1]:
                frame._done(self, self.__loop_data)
            if not self.__test_mode:
                self.__key_loop_thread.join()
                self.__io.done()
                if reset_colors_to_console_defaults:
                    self.__io.reset_colors_to_console_defaults()

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
            loop = TAMLoop(*args, **kwargs)
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
        info: will add a TAMFrame to stack
        :param frame: TAMFrame
        :return:
        """

        self.__frame_stack.append(frame)

    def pop_frame_stack(self):
        """
        info: will remove TAMFrame from stack
        :return: TAMFrame or None
        """

        if len(self.__frame_stack) != 0:
            frame = self.__frame_stack.pop()
            frame._done(self, self.__loop_data)
            return frame

    def _update_loop(self):
        """
        info: will update frame and call draw
        :return:
        """
        buffer = TAMBuffer(0, 0, " ", 0, 0)
        frame_skip = 0
        clock = timer.Timer()
        try:
            while self.__running and self.__error is None and len(self.__frame_stack) != 0:
                frame = self.__frame_stack[-1]
                frame_time = 1/frame.get_fps()
                keys = self.__input_keys.copy()
                self.__input_keys.clear()

                frame.update(self, keys, self.__loop_data)

                if self.__running and self.__error is None:
                    if frame_skip == 0:
                        frame.make_buffer_ready(buffer, *self.__io.get_dimensions())
                        frame.draw(buffer, self.__loop_data)
                        self.__io.draw(buffer)

                    _, run_time = clock.offset_sleep(max(frame_time - frame_skip, 0))

                    if run_time >= frame_time + frame_time/10 and frame_skip == 0:
                        frame_skip = run_time - frame_time
                    else:
                        frame_skip = 0

        except BaseException as error:
            self.__error = error
        finally:
            self.done()

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

    def get_color_2(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: RGBA
        """
        return self.__io.get_color_2(spot)

    def get_color_16(self, spot):
        """
        info: Will get color from color palette 16
        :param spot: int
        :return: RGBA
        """
        return self.__io.get_color_16(spot)

    def get_color_256(self, spot):
        """
        info: Will get color from color palette 256
        :param spot: int
        :return: RGBA
        """
        return self.__io.get_color_256(spot)

    def set_color_2(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        self.__io.set_color_2(spot, color)

    def set_color_16(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        self.__io.set_color_16(spot, color)

    def set_color_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        self.__io.set_color_256(spot, color)

    def reset_colors_to_console_defaults(self):
        """
        info: will reset colors to console defaults
        :return: None
        """
        self.__io.reset_colors_to_console_defaults()

    def set_tam_color_defaults(self):
        """
        info: will set console colors to tam defaults
        :return: None
        """
        self.__io.set_tam_color_defaults()

    def step(self, keys=()):
        """
        info: only works in test mode but lets you update and draw in tests
        :param keys: tuple: ((str, str), ...)
        :return: TAMBuffer or None
        """
        if self.__test_mode and self.__running:
            buffer = TAMBuffer(0, 0, " ", 0, 0)
            frame = self.__frame_stack[-1]
            try:
                frame.update(self, keys, self.__loop_data)
                frame.make_buffer_ready(buffer, *self.__io.get_dimensions())
                frame.draw(buffer, self.__loop_data)
                return buffer
            except BaseException:
                frame._done(self, self.__loop_data)
        return


class TAMFrame:
    def __init__(self,
                 fps,
                 char,
                 foreground_color,
                 background_color,
                 min_width=0,
                 max_width=1000,
                 min_height=0,
                 max_height=1000):
        """
        info: makes a TAMFrame object
        :param fps: int or float: 0.0 - inf
        :param char: str: len of 1
        :param foreground_color: int: 0 - inf
        :param background_color: int: 0 - inf
        :param min_width: int: 0 - inf
        :param max_width: int: min_width - inf
        :param min_height: int: 0 - inf
        :param max_height: int: min_height - inf
        """
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

    def make_buffer_ready(self, tam_buffer, screen_width, screen_height):
        """
        info: will make buffer ready for frame
        :param tam_buffer: TAMBuffer
        :param screen_width: int: 0 - inf
        :param screen_height: int: 0 - inf
        :return:
        """
        if (self.__char, self.__foreground_color, self.__background_color) != tam_buffer.get_defaults():
            tam_buffer.set_defaults_and_clear(self.__char, self.__foreground_color, self.__background_color)

        width = min(max(self.__min_width, screen_width), self.__max_width)
        height = min(max(self.__min_height, screen_height), self.__max_height)
        if (width, height) != tam_buffer.get_dimensions():
            tam_buffer.set_dimensions_and_clear(width, height)

        return tam_buffer

    def update(self, tam_loop, keys, loop_data):
        """
        info: will update terminal
        :param tam_loop: TAMLoop
        :param keys: list, tuple
        :param loop_data: dict
        :return:
        """
        raise NotImplementedError()

    def draw(self, tam_buffer, loop_data):
        """
        info: will draw frame onto terminal
        :param tam_buffer: TAMBuffer
        :param loop_data: dict
        :return:
        """
        raise NotImplementedError()

    def _done(self, tam_loop, loop_data):
        """
        info: will clean up the frame and can only be called once
        :param tam_loop: TAMLoop
        :param loop_data: dict
        :return:
        """
        if not self.__done_called:
            self.__done_called = True
            self.done(tam_loop, loop_data)

    def done(self, tam_loop, loop_data):
        """
        info: will clean up the frame and can only be called once
        :param tam_loop: TAMLoop
        :param loop_data: dict
        :return:
        """
        pass
