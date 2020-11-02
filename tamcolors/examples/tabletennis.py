from tamcolors import tam, tam_tools, tam_io
from random import randint


class Ball:
    def __init__(self, tam_buffer, way=False):
        self._tam_buffer = tam_buffer
        self._x = tam_buffer.get_dimensions()[0]//2
        self._y = tam_buffer.get_dimensions()[1]//2

        self._x_way = way
        self._y_way = None
        self._winner = None

        self._update = True

    def update(self):
        if isinstance(self._winner, bool):
            return

        self._update = not self._update
        if not self._update:
            return

        self._tam_buffer.set_spot(self._x, self._y, " ", tam_io.tam_colors.WHITE, tam_io.tam_colors.BLACK)

        while True:
            nx, ny = self._x, self._y
            if isinstance(self._x_way, bool):
                if self._x_way:
                    nx += 1
                else:
                    nx += -1

            if isinstance(self._y_way, bool) and bool(randint(0, 399)):
                if self._y_way:
                    ny += 1
                else:
                    ny += -1

            if nx == -1:
                self._winner = True
                break
            elif nx == self._tam_buffer.get_dimensions()[0]:
                self._winner = False
                break

            if self._tam_buffer.get_spot(nx, ny) is None:
                self._y_way = not self._y_way
                continue
            if self._tam_buffer.get_spot(nx, ny)[0] != " ":
                self._x_way = not self._x_way
                if self._y_way is None:
                    self._y_way = bool(randint(0, 2))
                continue

            if self._y_way is True and self._tam_buffer.get_spot(nx, ny - 1) is not None:
                if self._tam_buffer.get_spot(nx, ny - 1)[0] != " ":
                    self._x_way = not self._x_way
                    self._y_way = not self._y_way
                    continue
            elif self._y_way is False and  self._tam_buffer.get_spot(nx, ny + 1) is not None:
                if self._tam_buffer.get_spot(nx, ny + 1)[0] != " ":
                    self._x_way = not self._x_way
                    self._y_way = not self._y_way
                    continue

            self._x, self._y = nx, ny
            break
        self._tam_buffer.set_spot(self._x, self._y, "*", tam_io.tam_colors.LIGHT_AQUA, tam_io.tam_colors.BLACK)

    def get_y(self):
        return self._y

    def winner(self):
        return self._winner


class Racket:
    def __init__(self, x, ball, tam_buffer, ai=False):
        self._x = x
        self._y = tam_buffer.get_dimensions()[1]//2
        self._ball = ball
        self._tam_buffer = tam_buffer
        self._ai = ai

    def update(self, key_manager):
        self._tam_buffer.set_spot(self._x, self._y, " ", tam_io.tam_colors.WHITE, tam_io.tam_colors.BLACK)
        self._tam_buffer.set_spot(self._x, self._y + 1, " ", tam_io.tam_colors.WHITE, tam_io.tam_colors.BLACK)

        if self._ai and randint(0, 99) >= 40:
            if self._ball.get_y() < self._y:
                self._y += -1
            elif self._ball.get_y() > self._y:
                self._y += 1
            self._y = max(self._y - 1, 0)
            self._y = min(self._y + 1, self._tam_buffer.get_dimensions()[1] - 2)
        else:
            if key_manager.get_key_state("q"):
                self._y = max(self._y - 1, 0)
            if key_manager.get_key_state("a"):
                self._y = min(self._y + 1, self._tam_buffer.get_dimensions()[1] - 2)
        self._tam_buffer.set_spot(self._x, self._y, "#", tam_io.tam_colors.LIGHT_AQUA, tam_io.tam_colors.LIGHT_AQUA)
        self._tam_buffer.set_spot(self._x, self._y + 1, "#", tam_io.tam_colors.LIGHT_AQUA, tam_io.tam_colors.LIGHT_AQUA)


class TableTennis(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=24,
                         char=" ",
                         foreground_color=tam_io.tam_colors.WHITE,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=53, max_width=53, min_height=22, max_height=22)
        self._keys_manager = tam_tools.tam_key_manager.TAMKeyManager()
        self._board = tam_io.tam_buffer.TAMBuffer(51, 15, " ", tam_io.tam_colors.WHITE, tam_io.tam_colors.BLACK)
        self._box = tam_io.tam_buffer.TAMBuffer(53, 17, "#", tam_io.tam_colors.WHITE, tam_io.tam_colors.BLACK)
        self._text_box = tam_tools.tam_text_box.TAMTextBox("Press q and a to play.\nPress backspace to quit.",
                                                           53,
                                                           4,
                                                           "#",
                                                           tam_io.tam_colors.WHITE,
                                                           tam_io.tam_colors.BLACK,
                                                           1,
                                                           False)
        self._score = [0, 0]

        self._ball = Ball(self._board)
        self._racket_1 = Racket(2, self._ball, self._board)
        self._racket_2 = Racket(48, self._ball, self._board, True)

    def update(self, tam_loop, keys, loop_data):
        if self._ball.winner() is not None:
            self._score[int(self._ball.winner())] += 1

            if max(self._score) == 10:
                self._score = [0, 0]

            self._ball = Ball(self._board, self._ball.winner())
            self._racket_1 = Racket(2, self._ball, self._board)
            self._racket_2 = Racket(48, self._ball, self._board, True)
            self._board.clear()

        self._keys_manager.update(keys)
        self._text_box.update()

        if self._keys_manager.get_key_state("BACKSPACE"):
            tam_loop.done()

        self._ball.update()
        self._racket_1.update(self._keys_manager)
        self._racket_2.update(self._keys_manager)

    def draw(self, tam_buffer, loop_data):
        tam_buffer.clear()
        tam_buffer.draw_onto(self._box, 0, 2)
        tam_buffer.draw_onto(self._board, 1, 3)
        self._text_box.draw(tam_buffer, 0, 18)
        score_box = tam_tools.tam_text_box.TAMTextBox("{} | {}".format(*self._score),
                                                      53,
                                                      3,
                                                      "#",
                                                      tam_io.tam_colors.WHITE,
                                                      tam_io.tam_colors.BLACK,
                                                      center_horizontal=True)
        score_box.draw(tam_buffer, 0, 0)


def run():
    tam.tam_loop.TAMLoop(TableTennis()).run()
