# built in libraries
import threading
import itertools
import cProfile
import pstats

# tamcolors libraries
from tamcolors.tam_io.io_tam import MODE_2


class TAMLoopIOHandler:
    def __init__(self,
                 io,
                 name=None,
                 identifier_id=None,
                 color_change_key="ESCAPE",
                 start_data=None,
                 loop_data=None,
                 tam_color_defaults=True,
                 highest_mode_lock=False,
                 preferred_mode=None):
        """
        info: Makes a TAMLoopIOHandler Object
        :param io: IO
        :param name: str or None
        :param identifier_id: bytes or None
        :param color_change_key: char: key that will change color mode
        :param start_data: object
        :param loop_data: object
        :param tam_color_defaults: bool
        :param highest_mode_lock: bool: will disable change key and put IO in its highest color mode
        :param preferred_mode: tuple or None: will take the first mode that is supported. fallback is mode 2
        """

        if start_data is None:
            start_data = {}

        if loop_data is None:
            loop_data = {}

        self._color_modes = itertools.cycle(io.get_modes())
        if highest_mode_lock:
            self._color_modes = itertools.cycle(self._io.get_modes()[0:1])

        if preferred_mode is not None:
            preferred_mode = list(preferred_mode)
            preferred_mode.append(MODE_2)
            for mode in preferred_mode:
                if mode in io.get_modes():
                    self._color_modes = itertools.cycle((mode,))
                    break

        self._io = io
        self._name = name
        self._identifier_id = identifier_id
        self._color_change_key = color_change_key
        self._start_data = start_data
        self._loop_data = loop_data
        self._tam_color_defaults = tam_color_defaults
        self._highest_mode_lock = highest_mode_lock
        self._preferred_mode = preferred_mode

        self._running = None
        self._key_loop_thread = None
        self._error = None

        self._input_keys = []

        self._full_name = (self._name, self._identifier_id)

    def get_name(self):
        """
        info: get name
        :return: str or None
        """
        return self._name

    def get_identifier_id(self):
        """
        info: get identifier id
        :return: bytes or None
        """
        return self._identifier_id

    def get_full_name(self):
        """
        info: get full name
        :return: tuple
        """
        return self._full_name

    def get_start_data(self):
        """
        info: get start data
        :return: object
        """
        return self._start_data

    def set_start_data(self, start_data):
        """
        info: set start data
        :param start_data: object
        :return: None
        """
        self._start_data = start_data

    def get_loop_data(self):
        """
        info: get loop data
        :return: object
        """
        return self._loop_data

    def set_loop_data(self, loop_data):
        """
        info: set loop data
        :param loop_data: object
        :return: None
        """
        self._loop_data = loop_data

    def __call__(self):
        """
        info: will run tam loop
        :return: None
        """
        if self.is_running() is not None:
            return
        self._running = True
        self._io.set_tam_color_defaults()
        self._io.start()
        self._io.set_mode(next(self._color_modes))
        self._key_loop_thread = threading.Thread(target=self._key_loop, daemon=True)
        self._key_loop_thread.start()

    def done(self, reset_colors_to_console_defaults=True):
        """
        info: will stop tam loop
        :param: reset_colors_to_console_defaults: bool
        :return: None
        """
        if self.is_running():
            self._running = False
            if reset_colors_to_console_defaults:
                self._io.reset_colors_to_console_defaults()
            self._io.done()
            self._key_loop_thread.join(timeout=5)

    def run(self):
        """
        info: will call tam loop
        :return: None
        """
        self()

    def run_with_profiler(self):
        """
        info: will run with a profiler and print out data when done
        :return: None
        """
        profile = cProfile.Profile()
        profile.runcall(self)
        ps = pstats.Stats(profile)
        ps.sort_stats(pstats.SortKey.TIME)
        ps.print_stats()

    def is_running(self):
        """
        info: None has not ran, True is running, False has ran
        :return: bool or None
        """

        return self._running

    def _key_loop(self):
        """
        info: will get key input
        :return:
        """

        try:
            while self.is_running():
                key = self._io.wait_key()
                if key is not False:
                    if key[0] == self._color_change_key:
                        self._io.set_mode(next(self._color_modes))
                    else:
                        self._input_keys.append(key)
        except BaseException as error:
            self._error = error

    def get_keyboard_name(self, default_to_us_english=True):
        """
        info: Will get the keyboard language name
        :param default_to_us_english: bool
        :return: str
        """
        return self._io.get_keyboard_name(default_to_us_english)

    def get_color_2(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: RGBA
        """
        return self._io.get_color_2(spot)

    def get_color_16_pal_256(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: RGBA
        """
        raise self._io.get_color_16_pal_256(spot)

    def get_color_16(self, spot):
        """
        info: Will get color from color palette 16
        :param spot: int
        :return: RGBA
        """
        return self._io.get_color_16(spot)

    def get_color_256(self, spot):
        """
        info: Will get color from color palette 256
        :param spot: int
        :return: RGBA
        """
        return self._io.get_color_256(spot)

    def set_color_2(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        self._io.set_color_2(spot, color)

    def set_color_16_pal_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: int
        :return: None
        """
        self._io.set_color_16_pal_256(spot, color)

    def set_color_16(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        self._io.set_color_16(spot, color)

    def set_color_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        self._io.set_color_256(spot, color)

    def reset_colors_to_console_defaults(self):
        """
        info: will reset colors to console defaults
        :return: None
        """
        self._io.reset_colors_to_console_defaults()

    def set_tam_color_defaults(self):
        """
        info: will set console colors to tam defaults
        :return: None
        """
        self._io.set_tam_color_defaults()

    def pump_keys(self):
        """
        info: will get keys from the key queue
        :return: list
        """
        keys = self._input_keys.copy()
        self._input_keys.clear()
        return keys

    def get_io(self):
        """
        infl: will get the IO
        :return: IO
        """
        return self._io

    def set_key_state_mode(self, enable=True):
        """
        info: Will enable or disable key state mode
        :param enable: bool
        :return: None
        """
        self._io.set_key_state_mode(enable)

    def is_key_state_mode_enabled(self):
        """
        info: Will get the status of key_state
        :return: bool
        """
        return self._io.is_key_state_mode_enabled()
