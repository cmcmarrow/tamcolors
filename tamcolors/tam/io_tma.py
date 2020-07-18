# Charles McMarrow libraries
from .tma_buffer import TMABuffer

# Charles McMarrow

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

    def draw(self, tma_buffer):
        raise NotImplementedError()

    def _draw_2(self, tma_buffer):
        raise NotImplementedError()

    def _draw_16(self, tma_buffer):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def done(self):
        raise NotImplementedError()

    def get_key(self):
        raise NotImplementedError()

    def get_dimensions(self):
        raise NotImplementedError()

    @staticmethod
    def get_key_dict():
        raise NotImplementedError()

    @staticmethod
    def _draw_onto(tma_buffer, tma_buffer2):
        """
        info: will draw tma_buffer2 in the center of tma_buffer
        :param tma_buffer: TMABuffer
        :param tma_buffer2: TMABuffer
        :return:
        """
        buffer_size_x, buffer_size_y = tma_buffer.get_dimensions()
        width, height = tma_buffer2.get_dimensions()
        start_x = (buffer_size_x // 2) - (width // 2)
        start_y = (buffer_size_y // 2) - (height // 2)
        tma_buffer.draw_onto(tma_buffer2, max(start_x, 0), max(start_y, 0))
