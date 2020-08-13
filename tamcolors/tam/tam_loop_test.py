# tamcolors libraries
from tamcolors.tam_io.any_tam import AnyIO
from tamcolors.tam_io.tam_buffer import TAMBuffer


"""
TAMLoop
Handlers FPS, Key input, drawing, updating and TAMFrame stack
"""


class TAMLoopTest:
    def __init__(self,
                 tam_frame,
                 io_list=None,
                 any_os=False,
                 only_any_os=False,
                 color_change_key="ESCAPE",
                 loop_data=None):
        """
        info: makes a TAMLoop object
        :param tam_frame: TAMFrame: first frame in tam loop
        :param io_list: list, tuple, None: ios that can be used
        :param any_os: bool: will use ANYIO if no other IO can be used if True
        :param only_any_os: bool: will only use ANYIO if True
        :param color_change_key: char: key that will change color mode
        :param loop_data: dict
        """

        if loop_data is None:
            loop_data = {}

        self.__running = None

        self.__frame_stack = [tam_frame]
        self.__loop_data = loop_data
        self.__color_change_key = color_change_key
        self.__io = AnyIO()

        self.__buffer = TAMBuffer(0, 0, " ", 0, 0)

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

    def update(self, keys, width, height):
        """
        info: will update TAMLoopTest
        :param keys: list or tuple: ((str, str), ...)
        :param width: int, 0 - inf
        :param height: int, 0 - inf
        :return: (None or TAMBuffer, None or TAMFrame)
        """
        buffer, frame = None, None
        if self.__running and len(self.__frame_stack) != 0:
            new_keys = []
            for key in keys:
                if key[0] != self.__color_change_key:
                    new_keys.append(key)

            try:
                frame = self.__frame_stack[-1]
                frame.update(self, new_keys, self.__loop_data)

                frame.make_buffer_ready(self.__buffer, width, height)
                frame.draw(self.__buffer, self.__loop_data)
            except BaseException as error:
                self.done()
                if frame is not None:
                    frame._done(self, self.__loop_data)
                raise error
        else:
            self.done()

        if not self.__running and len(self.__frame_stack) != 0:
            frame = self.__frame_stack[-1]
            frame._done(self, self.__loop_data)

        return self.__buffer, frame

    def get_color(self, spot):
        return self.__io.get_color(spot)

    def set_color(self, spot, color):
        self.__io.set_color(spot, color)

    def reset_colors_to_console_defaults(self):
        self.__io.reset_colors_to_console_defaults()

    def set_tam_color_defaults(self):
        self.__io.set_tam_color_defaults()
