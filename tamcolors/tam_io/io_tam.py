import sys


"""
IO
defines standards for all terminal IO
"""


class IO:
    def __init__(self, mode_2=True, mode_16=True):
        """
        Makes a IO object
        :param mode_2: bool
        :param mode_16: bool
        """
        self._modes = []
        if mode_2:
            self._modes.append(2)
        if mode_16:
            self._modes.append(16)

        if 16 in self._modes:
            self._mode = 16
        else:
            self._mode = self._modes[0]

        self._modes = tuple(self._modes)

    @classmethod
    def able_to_execute(cls):
        raise NotImplementedError()

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        self._mode = mode

    def get_mode(self):
        """
        info: will return the current color mode
        :return: int
        """
        return self._mode

    def get_modes(self):
        """
        info: will return a tuple of all color modes
        :return: (int, int, ...)
        """
        return self._modes

    def draw(self, tam_buffer):
        tam_buffer.replace_alpha_chars()
        self._get_mode_draw()(tam_buffer)

    def _draw_2(self, tam_buffer):
        raise NotImplementedError()

    def _draw_16(self, tam_buffer):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def done(self):
        raise NotImplementedError()

    def get_key(self):
        raise NotImplementedError()

    def get_dimensions(self):
        raise NotImplementedError()

    def printc(self, value, color, flush, stderr):
        raise NotImplementedError()

    def inputc(self, output, color):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def _get_mode_draw(self):
        return getattr(self, "_draw_{}".format(self._mode))

    @staticmethod
    def get_key_dict():
        raise NotImplementedError()

    @staticmethod
    def _draw_onto(tam_buffer, tam_buffer2):
        """
        info: will draw tam_buffer2 in the center of tam_buffer
        :param tam_buffer: TAMBuffer
        :param tam_buffer2: TAMBuffer
        :return:
        """
        buffer_size_x, buffer_size_y = tam_buffer.get_dimensions()
        width, height = tam_buffer2.get_dimensions()
        start_x = (buffer_size_x // 2) - (width // 2)
        start_y = (buffer_size_y // 2) - (height // 2)
        tam_buffer.draw_onto(tam_buffer2, max(start_x, 0), max(start_y, 0))

    @staticmethod
    def _write_to_output_stream(output, flush, stderr):
        """
        info: will write to the right stream
        :param stderr: bool
        :return: stdout or stderr
        """
        file = sys.stdout
        if stderr:
            file = sys.stderr

        file.write(output)

        if flush:
            file.flush()


class SingletonIO(IO):
    """
    Only lets one IO instance exist
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = None
            if cls.able_to_execute():
                cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
