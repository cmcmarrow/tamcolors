# Charles McMarrow libraries
import checks
import tma
import tma_tools

# Charles McMarrow

"""
TMAMenu
A way for user to give input/pick an option
"""


class TMAMenuError(Exception):
    pass


class TMAMenu:
    def __init__(self, buttons, call_key, goto_map, on=0):
        """
        info: Makes a TMAMenu object
        :param buttons: list or tuple: (TMAButtonRule, TMAButtonRule, ...)
        :param call_key: str
        :param goto_map: dict: {int: {str: int}}
        :param on: int: 0 - (len(buttons) - 1)
        """
        # checks
        for button in buttons:
            checks.checks.instance_check(button, TMAButtonRule, TMAMenuError)
        checks.checks.instance_check(call_key, str, TMAMenuError)
        checks.checks.instance_check(goto_map, dict, TMAMenuError)
        for key in goto_map:
            checks.checks.instance_check(key, int, TMAMenuError)
            checks.checks.instance_check(goto_map[key], dict, TMAMenuError)
            for key2 in goto_map[key]:
                checks.checks.instance_check(key2, str, TMAMenuError)
                checks.checks.range_check(goto_map[key][key2], 0, len(buttons), TMAMenuError)

        if on != 0:
            checks.checks.range_check(on, 0, len(buttons), TMAMenuError)

        self.__buttons = {spot: button for spot, button in enumerate(buttons)}
        self.__call_key = call_key
        self.__goto_map = goto_map

        self.__on = on

        if len(self.__buttons) != self.__on:
            self.__buttons[self.__on].on()

    def update(self, keys):
        """
        info: update the menu
        :param keys: list or tuple: [(str, str), (str, str, ...), ...]
        :return:
        """
        # checks
        checks.checks.in_instances_check(keys, (list, tuple), TMAMenuError)
        for key_data in keys:
            checks.checks.in_instances_check(keys, (list, tuple), TMAMenuError)
            checks.checks.range_check(len(key_data), 2, None, TMAMenuError)
            checks.checks.instance_check(key_data[0], str, TMAMenuError)
            checks.checks.instance_check(key_data[1], str, TMAMenuError)

        if len(self.__buttons) == 0:
            return None

        repeat_keys = set()
        for key, _ in keys:
            if key in repeat_keys:
                continue

            if key == self.__call_key:
                self.__buttons[self.__on]()
                break

            if key in self.__goto_map[self.__on]:
                self.__buttons[self.__on].off()
                self.__on = self.__goto_map[self.__on][key]
                self.__buttons[self.__on].on()

            repeat_keys.add(key)

        for key in self.__buttons:
            self.__buttons[key].update()

    def draw(self, buffer):
        """
        info: draw all the buttons of the menu
        :param buffer: TMABuffer
        :return:
        """
        for key in self.__buttons:
            self.__buttons[key].draw(buffer)

    def get_call_key(self):
        """
        info: gets the call key
        :return: str
        """
        return self.__call_key

    def get_on(self):
        """
        info: gets the on value
        :return: int
        """
        return self.__on, self.__buttons.get(self.__on, None)

    def get_goto_map(self):
        """
        info: gets the goto map
        :return: dict
        """
        return self.__goto_map

    def get_buttons(self):
        """
        info: gets the buttons
        :return: list
        """
        return [self.__buttons[spot] for spot in range(len(self.__buttons))]

    @staticmethod
    def simple_menu_builder(buttons, call_on, up_keys=("UP",), down_keys=("DOWN",), on=0):
        """
        info: a simple way of making a TMAMenu
        :param buttons: TMAButtonRule
        :param call_on: str
        :param up_keys: list or tuple: (str, ...)
        :param down_keys: list or tuple: (str, ...)
        :param on: int
        :return: TMAMenu
        """
        checks.checks.in_instances_check(buttons, (list, tuple), buttons)
        for button in buttons:
            checks.checks.instance_check(button, TMAButtonRule, TMAMenuError)

        checks.checks.instance_check(call_on, str, TMAMenuError)

        checks.checks.in_instances_check(up_keys, (set, list, tuple), TMAMenuError)
        for key in up_keys:
            checks.checks.instance_check(key, str, TMAMenuError)

        checks.checks.in_instances_check(down_keys, (set, list, tuple), TMAMenuError)
        for key in down_keys:
            checks.checks.instance_check(key, str, TMAMenuError)

        checks.checks.instance_check(on, int, TMAMenuError)

        goto_map = {}
        for spot in range(len(buttons)):
            button_dict = {}
            if spot == 0:
                for key in up_keys:
                    button_dict[key] = len(buttons) - 1
            else:
                for key in up_keys:
                    button_dict[key] = spot - 1

            if spot + 1 == len(buttons):
                for key in down_keys:
                    button_dict[key] = 0
            else:
                for key in down_keys:
                    button_dict[key] = spot + 1

            goto_map[spot] = button_dict

        return TMAMenu(buttons, call_on, goto_map, on)


class TMAButtonRule:
    def __init__(self):
        pass

    def __call__(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def draw(self, buffer):
        raise NotImplementedError()

    def on(self):
        raise NotImplementedError()

    def off(self):
        raise NotImplementedError()

    def run_action(self):
        raise NotImplementedError()

    def set_action(self, func):
        raise NotImplementedError()

    def get_action(self):
        raise NotImplementedError()

    def get_position(self):
        raise NotImplementedError()

    def set_position(self, x, y):
        raise NotImplementedError()


class TMATextButton(TMAButtonRule):
    def __init__(self,
                 text,
                 x,
                 y,
                 foreground_color,
                 background_color,
                 action_func,
                 on_foreground_color,
                 on_background_color,
                 on_chars="* "):
        """
        info: Makes a TMATextButton
        :param text: str
        :param x: int
        :param y: int
        :param foreground_color: 0 - inf
        :param background_color: 0 - inf
        :param action_func: function
        :param on_foreground_color: 0 - inf
        :param on_background_color: 0 - inf
        :param on_chars: str
        """
        # checks
        checks.checks.instance_check(text, str, TMAMenuError)
        checks.checks.instance_check(x, int, TMAMenuError)
        checks.checks.instance_check(y, int, TMAMenuError)
        checks.checks.range_check(foreground_color, 0, None, TMAMenuError)
        checks.checks.range_check(background_color, 0, None, TMAMenuError)
        checks.checks.is_function_check(action_func, TMAMenuError)
        checks.checks.range_check(on_foreground_color, 0, None, TMAMenuError)
        checks.checks.range_check(on_background_color, 0, None, TMAMenuError)
        checks.checks.instance_check(on_chars, str, TMAMenuError)

        super().__init__()

        self.__text = text
        self.__x = x
        self.__y = y
        self.__foreground_color = foreground_color
        self.__background_color = background_color

        self.__action_func = action_func

        self.__on_foreground_color = on_foreground_color
        self.__on_background_color = on_background_color
        self.__on_chars = on_chars

        self.__draw_args = ((self.__x, self.__y, self.__text, self.__foreground_color, self.__background_color),)

        self.__on = False

    def __call__(self):
        """
        info: calls the action function
        :return:
        """
        self.__action_func()

    def __str__(self):
        """
        info: gets the text
        :return: str
        """
        return self.__text

    def update(self):
        """
        info: updates the button
        :return:
        """
        pass

    def draw(self, buffer):
        """
        info: draws button onto buffer
        :param buffer:
        :return:
        """
        checks.checks.instance_check(buffer, tma.tma_buffer.TMABuffer, TMAMenuError)
        for draw_args in self.__draw_args:
            tma_tools.tma_print.tma_print(buffer, *draw_args)

    def on(self):
        """
        info: puts the button onto the on state
        :return:
        """
        if not self.__on:
            self.__draw_args = [(self.__x - len(self.__on_chars),
                                self.__y,
                                self.__on_chars + self.__text.split("\n")[0],
                                self.__on_foreground_color,
                                self.__on_background_color)]

            self.__draw_args.append((self.__x,
                                     self.__y + 1,
                                     "\n".join(self.__text.split("\n")[1:]),
                                     self.__on_foreground_color,
                                     self.__on_background_color))
            self.__on = True

    def off(self):
        """
        info: puts the button onto the off state
        :return:
        """
        if self.__on:
            self.__draw_args = ((self.__x, self.__y, self.__text, self.__foreground_color, self.__background_color),)
            self.__on = False

    def run_action(self):
        """"
        info: calls the action function
        :return:
        """
        self()

    def set_action(self, func):
        """
        info: sets the actions
        :param func: function
        :return:
        """
        # checks
        checks.checks.is_function_check(func, TMAMenuError)

        self.__action_func = func

    def get_action(self):
        """
        info: gets action function
        :return: fuction
        """

        return self.__action_func

    def get_position(self):
        """
        info: gets the position
        :return:
        """
        return self.__x, self.__y

    def set_position(self, x, y):
        """
        info: sets the position
        :param x: int
        :param y: int
        :return:
        """

        checks.checks.instance_check(x, int, TMAMenuError)
        checks.checks.instance_check(y, int, TMAMenuError)

        self.__x = x
        self.__y = y

        self.__on = not self.__on
        if self.__on:
            self.off()
        else:
            self.on()


class TMATextBoxButton(TMAButtonRule):
    def __init__(self,
                 text,
                 x,
                 y,
                 width,
                 height,
                 char,
                 foreground_color,
                 background_color,
                 action_func,
                 on_foreground_color,
                 on_background_color,
                 on_char="/",
                 clock=-1,
                 center_vertical=True,
                 center_horizontal=False,
                 vertical_space=1,
                 vertical_start=1,
                 char_background=" "):

        # checks
        checks.checks.instance_check(text, str, TMAMenuError)
        checks.checks.range_check(width, 0, None, TMAMenuError)
        checks.checks.range_check(height, 0, None, TMAMenuError)
        checks.checks.single_block_char_check(char, TMAMenuError)
        checks.checks.range_check(foreground_color, 0, None, TMAMenuError)
        checks.checks.range_check(background_color, 0, None, TMAMenuError)
        checks.checks.instance_check(clock, int, TMAMenuError)
        checks.checks.instance_check(center_vertical, bool, TMAMenuError)
        checks.checks.instance_check(center_horizontal, bool, TMAMenuError)
        checks.checks.range_check(vertical_space, 1, None, TMAMenuError)
        checks.checks.instance_check(vertical_start, int, TMAMenuError)
        checks.checks.single_block_char_check(char_background, TMAMenuError)

        if clock != -1:
            checks.checks.range_check(clock, 1, None, TMAMenuError)

        checks.checks.instance_check(x, int, TMAMenuError)
        checks.checks.instance_check(y, int, TMAMenuError)
        checks.checks.is_function_check(action_func, TMAMenuError)
        checks.checks.range_check(on_foreground_color, 0, None, TMAMenuError)
        checks.checks.range_check(on_background_color, 0, None, TMAMenuError)
        checks.checks.single_block_char_check(on_char, TMAMenu)

        super().__init__()

        self.__text_box = tma_tools.tma_text_box.TMATextBox(text,
                                                            width,
                                                            height,
                                                            char,
                                                            foreground_color,
                                                            background_color,
                                                            clock=clock,
                                                            center_vertical=center_vertical,
                                                            center_horizontal=center_horizontal,
                                                            vertical_space=vertical_space,
                                                            vertical_start=vertical_start,
                                                            char_background=char_background)

        self.__text = text
        self.__x = x
        self.__y = y
        self.__char = char
        self.__foreground_color = foreground_color
        self.__background_color = background_color

        self.__action_func = action_func

        self.__on_char = on_char
        self.__on_foreground_color = on_foreground_color
        self.__on_background_color = on_background_color

        self.__on = False

        self.update()

    def __call__(self):
        """
        info: calls the action function
        :return:
        """
        self.__action_func()

    def __str__(self):
        """
        info: gets the text
        :return: str
        """
        return self.__text

    def update(self):
        """
        info: updates the button
        :return:
        """
        self.__text_box.update()

    def draw(self, buffer):
        """
        info: draws button onto buffer
        :param buffer:
        :return:
        """
        self.__text_box.draw(buffer, self.__x, self.__y)

    def on(self):
        """
        info: puts the button onto the on state
        :return:
        """
        if not self.__on:
            self.__text_box.set_char(self.__on_char)
            self.__text_box.set_colors(self.__on_foreground_color, self.__on_background_color)
            self.__on = True

    def off(self):
        """
        info: puts the button onto the off state
        :return:
        """
        if self.__on:
            self.__text_box.set_char(self.__char)
            self.__text_box.set_colors(self.__foreground_color, self.__background_color)
            self.__on = False

    def run_action(self):
        """"
        info: calls the action function
        :return:
        """
        self()

    def set_action(self, func):
        """
        info: sets the actions
        :param func: function
        :return:
        """
        # checks
        checks.checks.is_function_check(func, TMAMenuError)

        self.__action_func = func

    def get_action(self):
        """
        info: gets action function
        :return: fuction
        """
        return self.__action_func

    def get_position(self):
        """
        info: gets the position
        :return:
        """
        return self.__x, self.__y

    def set_position(self, x, y):
        """
        info: sets the position
        :param x: int
        :param y: int
        :return:
        """

        checks.checks.instance_check(x, int, TMAMenuError)
        checks.checks.instance_check(y, int, TMAMenuError)

        self.__x = x
        self.__y = y

        self.__on = not self.__on
        if self.__on:
            self.off()
        else:
            self.on()
