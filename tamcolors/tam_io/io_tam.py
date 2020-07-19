"""
IO
defines standards for all terminal IO
"""


class IO:
    def __init__(self):
        pass

    @classmethod
    def get_io(cls):
        raise NotImplementedError()

    def set_mode(self, mode):
        raise NotImplementedError()

    def get_mode(self):
        raise NotImplementedError()

    def get_modes(self):
        raise NotImplementedError()

    def draw(self, tam_buffer):
        raise NotImplementedError()

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

    def printc(self, value, color):
        raise NotImplementedError()

    def inputc(self, output, color):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

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
