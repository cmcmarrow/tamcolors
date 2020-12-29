# tamcolors libraries
from tamcolors import tam_io
from . import tam_str

"""
TAMTextBox
can center text
can have a single char placed at a time
can set colors
"""


class TAMTextBox:
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
        info: makes TAMTextBox Object
        :param text: str
        :param width: int: 0 - inf
        :param height: int: 0 - inf
        :param char: str: len == 1
        :param foreground_color: Color
        :param background_color: Color
        :param clock: int: -1 or 1 - inf
        :param center_vertical: bool,
        :param center_horizontal: bool
        :param vertical_space: int: 1 - inf
        :param char_background: str: len == 1
        """
        self._text = tam_str.make_tam_str(text)
        self._width = width
        self._height = height
        self._char = char
        self._foreground_color = foreground_color
        self._background_color = background_color
        self._char_background = char_background

        self._surface = tam_io.tam_surface.TAMSurface(width, height, char_background, foreground_color, background_color)

        self._clock = clock
        self._clock_at = clock
        self._tick_count = 0
        self._done = False

        self._center_vertical = center_vertical
        self._vertical_space = vertical_space
        self._vertical_start = vertical_start
        self._center_horizontal = center_horizontal

        self._generator = self._update_generator()

        if self._clock == -1:
            self.update()

    def __str__(self):
        """
        info: gets text
        :return: str
        """
        return self._text

    def update(self):
        """
        info updates the text box
        :return:
        """
        if self._done:
            return None
        elif self._clock == -1:
            while not self._done:
                try:
                    next(self._generator)
                except StopIteration:
                    self._done = True
        else:
            try:
                if self._clock_at == self._clock:
                    next(self._generator)
                    self._clock_at = 0
            except StopIteration:
                self._done = True

        self._clock_at += 1
        self._tick_count += 1

    def _update_generator(self):
        """
        info: puts the next char onto the text box
        :return:
        """
        if self._width != 0 and self._height != 0:
            # draw the outline of the text box
            for x in range(self._width):
                self._surface.set_spot(x, 0, self._char, self._foreground_color, self._background_color)
                self._surface.set_spot(x,
                                       self._height - 1,
                                       self._char,
                                       self._foreground_color,
                                       self._background_color)

            for y in range(1, self._height - 1):
                self._surface.set_spot(0, y, self._char, self._foreground_color, self._background_color)
                self._surface.set_spot(self._width - 1,
                                       y,
                                       self._char,
                                       self._foreground_color,
                                       self._background_color)
            yield None
            # find the height
            height = self._vertical_start
            if self._center_vertical:
                text_height = (len(self._text.split("\n")) - 1) * self._vertical_space + 1
                height = (self._height - text_height) // 2

            for line in self._text.split("\n"):
                # find the width
                width = 2
                if self._center_horizontal:
                    width = (self._width - len(line)) // 2
                for spot, char in enumerate(line):
                    self._surface.set_spot(width + spot, height, char, self._foreground_color, self._background_color)
                    yield None
                height += self._vertical_space

    def draw(self,
             tam_surface,
             start_x=0,
             start_y=0):

        """
        info: draws the text box on to another surface
        :param tam_surface: TAMSurface
        :param start_x: int
        :param start_y: int
        :return:
        """
        tam_surface.draw_onto(self._surface, start_x, start_y)

    def done(self):
        """
        info: True if text box has placed all chars onto to its self
        :return: bool
        """
        return self._done

    def set_colors(self, foreground_color, background_color):
        """
        info: sets textbox colors
        :param foreground_color: 0 - inf
        :param background_color: 0 - inf
        :return:
        """
        self._foreground_color = foreground_color
        self._background_color = background_color

        self._rebuild()

    def set_char(self, char):
        """
        info: sets char
        :return:
        """
        self._char = char
        self._rebuild()

    def get_char(self):
        """
        info: gets char
        :return: str
        """
        return self._char

    def get_colors(self):
        """
        info: gets textbox color
        :return: (int, int)
        """
        return self._foreground_color, self._background_color

    def get_text(self):
        """
        info: gets text
        :return: str
        """
        return self._text

    def get_dimensions(self):
        """
        info: gets surface dimensions
        :return: (int, int)
        """
        return self._width, self._height

    def _rebuild(self):
        """
        info: makes the text box again
        :return:
        """

        self._surface = tam_io.tam_surface.TAMSurface(self._width,
                                                      self._height,
                                                      self._char_background,
                                                      self._foreground_color,
                                                      self._background_color)

        if self._clock == -1:
            self._clock_at = self._clock
            self._tick_count = 0
            self._done = False
            self._generator = self._update_generator()
            self.update()
        else:
            tick_count = self._tick_count
            self._clock_at = self._clock
            self._tick_count = 0
            self._done = False
            self._generator = self._update_generator()
            for _ in range(tick_count):
                self.update()
