# built in library
import copy


"""
TMABUFFER
stores char and colors for spot
can get/set spots
can clear 
can format to be outputted
"""


class TMABufferError(Exception):
    pass


class TMABuffer:
    def __init__(self,
                 width,
                 height,
                 char,
                 foreground_color,
                 background_color):
        """
        info: makes a TMABuffer object
        :param width: int: 0 - inf
        :param height: int: 0 - inf
        :param char: str: len of 1
        :param foreground_color: int: 0 - inf
        :param background_color: int: 0 - inf
        """

        # save data
        self.__width = width
        self.__height = height
        self.__char = char
        self.__foreground_color = foreground_color
        self.__background_color = background_color

        # setup buffers
        length = width * height
        self.__char_buffer = [char] * length
        self.__foreground_buffer = [foreground_color] * length
        self.__background_buffer = [background_color] * length

    def __str__(self):
        """
        info: formats TMABuffer to string  to be printed
        :return: str: TMABuffer as string
        """
        rows = []
        for y in range(self.__height):
            rows.append("".join(self.__char_buffer[y * self.__width:(y + 1) * self.__width]))

        return "\n".join(rows)

    def __len__(self):
        """
        info: gets the number of spot in the buffer
        :return:
        """
        return len(self.__char_buffer)

    def __eq__(self, other):
        """
        info: self == other
        :param other: Object
        :return: bool
        """
        if isinstance(other, TMABuffer):
            return self.get_raw_buffers() == other.get_raw_buffers()
        return False

    def __ne__(self, other):
        """
        info: self != other
        :param other: Object
        :return: bool
        """
        return not self.__eq__(other)

    def clear(self):
        """
        info: clears TMABuffer
        :return:
        """
        length = self.__width * self.__height
        self.__char_buffer = [self.__char] * length
        self.__foreground_buffer = [self.__foreground_color] * length
        self.__background_buffer = [self.__background_color] * length

    def get_dimensions(self):
        """
        info: gets buffer dimensions
        :return: (int, int)
        """
        return self.__width, self.__height

    def set_dimensions_and_clear(self, width, height):
        """
        info: clears and resizes TMABuffer
        :param width: int: 0 - inf
        :param height: int: 0 - inf
        :return:
        """
        self.__width = width
        self.__height = height

        length = width * height
        self.__char_buffer = [self.__char] * length
        self.__foreground_buffer = [self.__foreground_color] * length
        self.__background_buffer = [self.__background_color] * length

    def get_defaults(self):
        """
        info: gets defaults
        :return: (str, int, int)
        """
        return self.__char, self.__foreground_color, self.__background_color

    def set_defaults_and_clear(self, char, foreground_color, background_color):
        """
        info: clears buffer and resets defaults
        :param char: str: len of 1
        :param foreground_color: int: 0 - inf
        :param background_color: int: 0 - inf
        :return:
        """
        self.__char = char
        self.__foreground_color = foreground_color
        self.__background_color = background_color

        length = self.__width * self.__height
        self.__char_buffer = [self.__char] * length
        self.__foreground_buffer = [self.__foreground_color] * length
        self.__background_buffer = [self.__background_color] * length

    def get_raw_buffers(self):
        """
        info: gets raw buffers
        :return: (list, list, list)
        """
        return self.__char_buffer, self.__foreground_buffer, self.__background_buffer

    def copy(self):
        """
        info: copy's TMABuffer
        :return: TMABuffer
        """
        return copy.deepcopy(self)

    def get_raw_spot(self, x, y):
        """
        info: return -1 if not a spot
        :param x: int
        :param y: int
        :return: int
        """
        if x < 0 or x >= self.__width:
            return -1
        if y < 0 or y >= self.__height:
            return -1
        return x + y * self.__width

    def set_spot(self, x, y, char, foreground_color, background_color):
        """
        info: sets a single spot on the buffer
        :param x: int
        :param y: int
        :param char: str: len of 1
        :param foreground_color: int: -1 - inf: use current foreground_color
        :param background_color: int: -1 - inf: use current background_color
        :return:
        """

        spot = self.get_raw_spot(x, y)
        if spot != -1:
            self.__char_buffer[spot] = char
            if foreground_color != -1:
                self.__foreground_buffer[spot] = foreground_color
            if background_color != -1:
                self.__background_buffer[spot] = background_color

    def get_spot(self, x, y):
        """
        info: gets spot info
        :param x: int
        :param y: int
        :return: (int, int, int) or None
        """

        spot = self.get_raw_spot(x, y)
        if spot != -1:
            return self.__char_buffer[spot], self.__foreground_buffer[spot], self.__background_buffer[spot]
        return None

    def get_from_raw_spot(self, spot):
        """
        info: gets spot info
        :param spot: x: int: 0 - (len(tma_buffer) - 1)
        :return: (int, int, int) or None
        """
        if 0 <= spot < len(self.__char_buffer):
            return self.__char_buffer[spot], self.__foreground_buffer[spot], self.__background_buffer[spot]
        return None

    def draw_onto(self,
                  tma_buffer,
                  start_x=0,
                  start_y=0,
                  buffer_start_x=0,
                  buffer_start_y=0,
                  buffer_size_x=-1,
                  buffer_size_y=-1):
        """
        info: will draw tma_buffer or part of a TMABuffer onto another TMABuffer
        :param tma_buffer: TMABuffer
        :param start_x: int
        :param start_y: int
        :param buffer_start_x: int
        :param buffer_start_y: int
        :param buffer_size_x: int: 0 - inf
        :param buffer_size_y: int: 0 - inf
        :return:
        """

        start_x, \
        start_y, \
        buffer_start_x, \
        buffer_start_y, \
        buffer_size_x, \
        buffer_size_y = self.get_cross_rect(tma_buffer,
                                            start_x,
                                            start_y,
                                            buffer_start_x,
                                            buffer_start_y,
                                            buffer_size_x,
                                            buffer_size_y)

        char_buffer, foreground_buffer, background_buffer = tma_buffer.get_raw_buffers()
        this_char_buffer, this_foreground_buffer, this_background_buffer = self.get_raw_buffers()
        for y in range(buffer_size_y):
            to_spot = self.get_raw_spot(start_x, start_y + y)
            draw_spot = tma_buffer.get_raw_spot(buffer_start_x, buffer_start_y + y)
            for ts, ds in zip(range(to_spot, to_spot + buffer_size_x), range(draw_spot, draw_spot + buffer_size_x)):
                this_char_buffer[ts] = char_buffer[ds]
                this_foreground_buffer[ts] = foreground_buffer[ds]
                this_background_buffer[ts] = background_buffer[ds]

    def get_cross_rect(self,
                       tma_buffer,
                       start_x=0,
                       start_y=0,
                       buffer_start_x=0,
                       buffer_start_y=0,
                       buffer_size_x=-1,
                       buffer_size_y=-1):
        """
        info: will draw tma_buffer or part of a TMABuffer onto another TMABuffer
        :param tma_buffer: TMABuffer
        :param start_x: int
        :param start_y: int
        :param buffer_start_x: int
        :param buffer_start_y: int
        :param buffer_size_x: int: 0 - inf
        :param buffer_size_y: int: 0 - inf
        :return:
        """
        width, height = tma_buffer.get_dimensions()
        if buffer_size_x == -1:
            buffer_size_x = width
        if buffer_size_y == -1:
            buffer_size_y = height

        if start_x < 0:
            buffer_start_x += abs(start_x)
            buffer_size_x = max(buffer_size_x + start_x, 0)
            start_x = 0

        if start_y < 0:
            buffer_start_y += abs(start_y)
            buffer_size_y = max(buffer_size_y + start_y, 0)
            start_y = 0

        if buffer_start_x < 0:
            start_x += abs(buffer_start_x)
            buffer_size_x = max(buffer_size_x + buffer_start_x, 0)
            buffer_start_x = 0

        if buffer_start_y < 0:
            start_y += abs(buffer_start_y)
            buffer_size_y = max(buffer_size_y + buffer_start_y, 0)
            buffer_start_y = 0

        buffer_size_x = max(min(buffer_size_x, width - buffer_start_x, self.__width - start_x), 0)
        buffer_size_y = max(min(buffer_size_y, height - buffer_start_y, self.__height - start_y), 0)

        return start_x, start_y, buffer_start_x, buffer_start_y, buffer_size_x, buffer_size_y
