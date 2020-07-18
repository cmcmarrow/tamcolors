# Charles McMarrow libraries
from tamcolors import checks
from .tma_buffer import TMABuffer
from . import tma_loop

# Charles McMarrow

"""
TMALoop
Handlers FPS, Key input, drawing, updating and TMAFrame stack
"""


class TMALoopTestError(Exception):
    pass


class TMALoopTest:
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
        checks.checks.instance_check(tma_frame, tma_loop.TMAFrame, TMALoopTestError)
        checks.checks.instance_check(any_os, bool, TMALoopTestError)
        checks.checks.range_check(buffer_count, 1, None, TMALoopTestError)
        checks.checks.instance_check(color_change_key, str, TMALoopTestError)
        checks.checks.instance_check(loop_data, dict, TMALoopTestError)

        self.__running = None

        self.__frame_stack = [tma_frame]
        self.__loop_data = loop_data

        self.__update_ready_buffers = [TMABuffer(0, 0, " ", 0, 0) for _ in range(buffer_count)]
        self.__draw_ready_buffers = []

        self.__color_change_key = color_change_key

    def __call__(self):
        """
        info: will run tam loop
        :return:
        """
        if self.__running is not None:
            return

        self.__running = True

    def done(self):
        """
        info: will stop tam loop
        :return:
        """
        if self.__running:
            self.__running = False

    def run(self):
        """
        info: will call tam loop
        :return:
        """
        self()

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
        checks.checks.instance_check(frame, tma_loop.TMAFrame, TMALoopTestError)

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

    def update(self, keys, width, height):
        """
        info: will update TMALoopTest
        :param keys: list or tuple: ((str, str), ...)
        :param width: int, 0 - inf
        :param height: int, 0 - inf
        :return: (None or TMABuffer, None or TMAFrame)
        """

        # checks
        checks.checks.in_instances_check(keys, (list, tuple), TMALoopTestError)
        for key in keys:
            checks.checks.in_instances_check(key, (list, tuple), TMALoopTestError)
            checks.checks.is_equal_check(len(key), 2, TMALoopTestError)
            checks.checks.instance_check(key[0], str, TMALoopTestError)
            checks.checks.instance_check(key[1], str, TMALoopTestError)
        checks.checks.range_check(width, 0, None, TMALoopTestError)
        checks.checks.range_check(height, 0, None, TMALoopTestError)

        buffer, frame = None, None
        if self.__running and len(self.__frame_stack) != 0:
            new_keys = []
            for key in keys:
                if key[0] != self.__color_change_key:
                    new_keys.append(key)

            try:
                frame = self.__frame_stack[-1]
                frame.update(self, new_keys, self.__loop_data)

                if len(self.__update_ready_buffers) != 0:
                    tma_buffer = frame.make_buffer_ready(self.__update_ready_buffers.pop(0), width, height)
                    frame.draw(tma_buffer, self.__loop_data)
                    self.__draw_ready_buffers.append(tma_buffer)

                    buffer = self.__draw_ready_buffers.pop(0)
                    self.__update_ready_buffers.append(buffer)

            except BaseException as error:
                self.done()
                if frame is not None:
                    frame.done(self, self.__loop_data)
                raise error
        else:
            self.done()

        if not self.__running and len(self.__frame_stack) != 0:
            frame = self.__frame_stack[-1]
            frame.done(self, self.__loop_data)

        return buffer, frame
