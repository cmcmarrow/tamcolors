# tamcolors libraries
from tamcolors import checks
from tamcolors import tma
from . import tma_str

"""
TMATextBox
can center text
can have a single char placed at a time
can set colors
"""


class TMATextBoxError(Exception):
    pass


class TMATextBox:
    def __init__(self,
                 text,
                 width,
                 height,
                 char,
                 foreground_color,
                 background_color,
                 clock=-1,
                 center_vertical=True,
                 center_horizontal=False,
                 vertical_space=1,
                 vertical_start=1,
                 char_background=" "):

        """
        info: makes TMATextBox Object
        :param text: str
        :param width: int: 0 - inf
        :param height: int: 0 - inf
        :param char: str: len == 1
        :param foreground_color: int: 0 - inf
        :param background_color: int: 0 - inf
        :param clock: int: -1 or 1 - inf
        :param center_vertical: bool,
        :param center_horizontal: bool
        :param vertical_space: 1 - inf
        :param char_background: str: len == 1
        """

        # checks
        checks.checks.instance_check(text, str, TMATextBoxError)
        checks.checks.range_check(width, 0, None, TMATextBoxError)
        checks.checks.range_check(height, 0, None, TMATextBoxError)
        checks.checks.single_block_char_check(char, TMATextBoxError)
        checks.checks.range_check(foreground_color, 0, None, TMATextBoxError)
        checks.checks.range_check(background_color, 0, None, TMATextBoxError)
        checks.checks.instance_check(clock, int, TMATextBoxError)
        checks.checks.instance_check(center_vertical, bool, TMATextBoxError)
        checks.checks.instance_check(center_horizontal, bool, TMATextBoxError)
        checks.checks.range_check(vertical_space, 1, None, TMATextBoxError)
        checks.checks.instance_check(vertical_start, int, TMATextBoxError)
        checks.checks.single_block_char_check(char_background, TMATextBoxError)

        if clock != -1:
            checks.checks.range_check(clock, 1, None, TMATextBoxError)

        self.__text = tma_str.make_tma_str(text)
        self.__width = width
        self.__height = height
        self.__char = char
        self.__foreground_color = foreground_color
        self.__background_color = background_color
        self.__char_background = char_background

        self.__buffer = tma.tma_buffer.TMABuffer(width, height, char_background, foreground_color, background_color)

        self.__clock = clock
        self.__clock_at = clock
        self.__tick_count = 0
        self.__done = False

        self.__center_vertical = center_vertical
        self.__vertical_space = vertical_space
        self.__vertical_start = vertical_start
        self.__center_horizontal = center_horizontal

        self.__generator = self.__update_generator()

    def __str__(self):
        """
        info: gets text
        :return: str
        """
        return self.__text

    def update(self):
        """
        info updates the text box
        :return:
        """
        if self.__done:
            return None
        elif self.__clock == -1:
            while not self.__done:
                try:
                    next(self.__generator)
                except StopIteration:
                    self.__done = True
        else:
            try:
                if self.__clock_at == self.__clock:
                    next(self.__generator)
                    self.__clock_at = 0
            except StopIteration:
                self.__done = True

        self.__clock_at += 1
        self.__tick_count += 1

    def __update_generator(self):
        """
        info: puts the next char onto the text box
        :return:
        """
        if self.__width != 0 and self.__height != 0:
            # draw the outline of the text box
            for x in range(self.__width):
                self.__buffer.set_spot(x, 0, self.__char, self.__foreground_color, self.__background_color)
                self.__buffer.set_spot(x,
                                       self.__height - 1,
                                       self.__char,
                                       self.__foreground_color,
                                       self.__background_color)

            for y in range(1, self.__height - 1):
                self.__buffer.set_spot(0, y, self.__char, self.__foreground_color, self.__background_color)
                self.__buffer.set_spot(self.__width - 1,
                                       y,
                                       self.__char,
                                       self.__foreground_color,
                                       self.__background_color)
            yield None
            # find the height
            height = self.__vertical_start
            if self.__center_vertical:
                text_height = (len(self.__text.split("\n")) - 1) * self.__vertical_space + 1
                height = (self.__height - text_height)//2

            for line in self.__text.split("\n"):
                # find the width
                width = 2
                if self.__center_horizontal:
                    width = (self.__width - len(line))//2
                for spot, char in enumerate(line):
                    self.__buffer.set_spot(width + spot, height, char, self.__foreground_color, self.__background_color)
                    yield None
                height += self.__vertical_space

    def draw(self,
             tma_buffer,
             start_x=0,
             start_y=0):

        """
        info: draws the text box on to another buffer
        :param tma_buffer: TMABuffer
        :param start_x: int
        :param start_y: int
        :return:
        """
        checks.checks.instance_check(tma_buffer, tma.tma_buffer.TMABuffer, TMATextBoxError)
        checks.checks.instance_check(start_x, int, TMATextBoxError)
        checks.checks.instance_check(start_y, int, TMATextBoxError)

        tma_buffer.draw_onto(self.__buffer, start_x, start_y)

    def done(self):
        """
        info: True if text box has placed all chars onto to its self
        :return: bool
        """
        return self.__done

    def set_colors(self, foreground_color, background_color):
        """
        info: sets textbox colors
        :param foreground_color: 0 - inf
        :param background_color: 0 - inf
        :return:
        """
        checks.checks.range_check(foreground_color, 0, None, TMATextBoxError)
        checks.checks.range_check(background_color, 0, None, TMATextBoxError)

        self.__foreground_color = foreground_color
        self.__background_color = background_color

        self.__rebuild()

    def set_char(self, char):
        """
        info: sets char
        :return:
        """
        checks.checks.single_block_char_check(char, TMATextBoxError)
        self.__char = char
        self.__rebuild()

    def get_char(self):
        """
        info: gets char
        :return: str
        """
        return self.__char

    def get_colors(self):
        """
        info: gets textbox color
        :return: (int, int)
        """
        return self.__foreground_color, self.__background_color

    def get_text(self):
        """
        info: gets text
        :return: str
        """
        return self.__text

    def get_dimensions(self):
        """
        info: gets buffer dimensions
        :return: (int, int)
        """
        return self.__width, self.__height

    def __rebuild(self):
        """
        info: makes the text box again
        :return:
        """

        self.__buffer = tma.tma_buffer.TMABuffer(self.__width,
                                                 self.__height,
                                                 self.__char_background,
                                                 self.__foreground_color,
                                                 self.__background_color)

        if self.__clock == -1:
            self.__clock_at = self.__clock
            self.__tick_count = 0
            self.__done = False
            self.__generator = self.__update_generator()
            self.update()
        else:
            tick_count = self.__tick_count
            self.__clock_at = self.__clock
            self.__tick_count = 0
            self.__done = False
            self.__generator = self.__update_generator()
            for _ in range(tick_count):
                self.update()
