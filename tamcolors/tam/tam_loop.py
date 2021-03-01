# built in libraries
import traceback
import time
import sys
from concurrent.futures import ThreadPoolExecutor


# tamcolors libraries
from tamcolors.tam_io.tam_surface import TAMSurface
from tamcolors.tests import all_tests
from tamcolors.tam_io import tam_identifier
from tamcolors.tam.tam_loop_io_handler import TAMLoopIOHandler
from tamcolors.utils import timer
from tamcolors.tam_io.tam_colors import GREEN, BLACK
from tamcolors.tam_io import tam_keys
from tamcolors.utils.identifier import get_identifier_bytes
from tamcolors.utils import log


"""
TAMLoop
Handlers FPS, Key input, drawing, updating and TAMFrame stack

TAMFrame
Holds information about frame
Colors, min and max size
"""


class TAMLoopError(Exception):
    pass


class TAMLoop(TAMLoopIOHandler):
    def __init__(self,
                 tam_frame,
                 io=None,
                 only_any_os=False,
                 color_change_key=tam_keys.KEY_ESCAPE,
                 loop_data=None,
                 stability_check=False,
                 tam_color_defaults=True,
                 highest_mode_lock=False,
                 preferred_mode=None,
                 name=None,
                 identifier_id=None,
                 start_data=None,
                 receivers=None,
                 other_handlers=None,
                 thread_count=20,
                 enable_loop_log=False,
                 loop_log_key=tam_keys.KEY_F1,
                 loop_log_level=log.DEBUG,
                 enable_loop_fps=True,
                 loop_fps_key=tam_keys.KEY_F2):
        """
        info: makes a TAMLoop object
        :param tam_frame: TAMFrame: first frame in tam loop
        :param io: IO
        :param only_any_os: bool: will only use Any Drivers if True
        :param color_change_key: tuple: key that will change color mode
        :param loop_data: dict: will hold context so all TAMFrames can see
        :param stability_check: bool: raises and error if a test did not pass
        :param tam_color_defaults: bool
        :param highest_mode_lock: bool: will disable change key and put IO in its highest color mode
        :param preferred_mode: tuple or None: will take the first mode that is supported. fallback is mode 2
        :param name: str or None
        :param identifier_id: bytes or None
        :param start_data: object
        :param receivers: tuple or None
        :param other_handlers: tuple or None
        :param thread_count: int: number of threads to handle other handlers, should have 2 per handler
        :param enable_loop_log: bool: will enable tam loop log
        :param loop_log_key: tuple: key that will switch to log
        :param loop_log_level: int
        :param enable_loop_fps: bool
        :param loop_fps_key: tuple
        """

        self._receiver_settings = {"color_change_key": color_change_key,
                                   "loop_data": loop_data,
                                   "stability_check": stability_check,
                                   "tam_color_defaults": tam_color_defaults,
                                   "highest_mode_lock": highest_mode_lock,
                                   "preferred_mode": preferred_mode}

        if stability_check and not all_tests.stability_check():
            test_results = all_tests.stability_check(ret_bool=False)
            raise TAMLoopError("TAM is corrupted! {0} out of {1} tests passed".format(*test_results))

        if only_any_os:
            io = tam_identifier.ANY_IO
        else:
            if io is None:
                io = tam_identifier.IO

            if io is None:
                raise TAMLoopError("tam io is None")

        self._frame_stack = [tam_frame]

        if name is None:
            name = "MAIN"

        if identifier_id is None:
            identifier_id = get_identifier_bytes()

        if receivers is None:
            receivers = ()
        self._receivers = {receiver.get_name(): receiver for receiver in receivers}

        if other_handlers is None:
            other_handlers = ()
        self._other_handlers = {other_handler.get_full_name(): other_handler for other_handler in other_handlers}

        self._workers = ThreadPoolExecutor(max_workers=thread_count)

        self._enable_loop_log = enable_loop_log
        self._loop_log_key = loop_log_key

        if self._enable_loop_log:
            log.enable_logging(loop_log_level)

        self._log_on = False
        self._log_at = 0
        self._log_bottom = True

        self._enable_loop_fps = enable_loop_fps
        self._fps_on = False
        self._fps_ticker = timer.TickRateTracker()
        self._ups_ticker = timer.TickRateTracker()
        self._fps_key = loop_fps_key

        super().__init__(io=io,
                         name=name,
                         identifier_id=identifier_id,
                         color_change_key=color_change_key,
                         start_data=start_data,
                         loop_data=loop_data,
                         tam_color_defaults=tam_color_defaults,
                         highest_mode_lock=highest_mode_lock,
                         preferred_mode=preferred_mode)

    def __call__(self):
        """
        info: will run tam loop
        :return: None
        """
        super().__call__()
        if self.is_running():
            for other_handlers in self._other_handlers:
                self.thread_task(other_handlers.__call__)
            self._update_loop()
            if self._error is not None:
                raise self._error

    def add_receiver(self, receiver):
        self._receivers[receiver.get_name()] = receiver

    def remove_receiver(self, receiver_name):
        del self._receivers[receiver_name]

    def get_all_receiver_names(self):
        return tuple(self._receivers)

    def done(self):
        """
        info: will stop tam loop
        :return: None
        """
        if self.is_running():
            try:
                for frame in self._frame_stack[::-1]:
                    frame._done(self,
                                self._loop_data,
                                self._other_handlers,
                                {other_handler: self._other_handlers[other_handler].get_loop_data() for other_handler in self._other_handlers})

                for other_handler in self._other_handlers:
                    log.debug("removed handler: {}".format(other_handler))
                    self.thread_task(self._other_handlers[other_handler].done)

                for receiver_name in self._receivers:
                    self.thread_task(self._receivers[receiver_name].done)
            finally:
                super().done()
                self._workers.shutdown(wait=False)

    def get_receiver_settings(self):
        """
        info: gets the receiver settings
        :return: dict
        """
        return self._receiver_settings

    @classmethod
    def run_application(cls, *args, **kwargs):
        """
        info: will run tam loop as an application
        note:
        when tam loop is done running the program will quit
        if tam loop has an error and the frame does not catch it
        the error will be printed onto the screen and the program will quit
        after user input
        :param args:
        :param kwargs:
        :return:
        """
        try:
            loop = cls(*args, **kwargs)
            loop()
        except KeyboardInterrupt:
            log.critical("Caught KeyboardInterrupt")
        except BaseException as error:
            try:
                log.critical("TAMLoop Error: {}".format(error))
                traceback.print_exception(error.__class__, error, sys.exc_info()[2])
                time.sleep(1)
                input("Press Enter To Continue . . .")
            except KeyboardInterrupt:
                log.critical("Caught KeyboardInterrupt")
        finally:
            sys.exit()

    def add_frame_stack(self, frame):
        """
        info: will add a TAMFrame to stack
        :param frame: TAMFrame
        :return:
        """
        log.debug("add_frame_stack: added {}".format(frame.__class__.__name__))
        self._frame_stack.append(frame)

    def pop_frame_stack(self):
        """
        info: will remove TAMFrame from stack
        :return: TAMFrame or None
        """

        if len(self._frame_stack) != 0:
            frame = self._frame_stack.pop()
            frame._frame_done(self,
                              self._loop_data,
                              self._other_handlers,
                              {other_handler: self._other_handlers[other_handler].get_loop_data() for other_handler in self._other_handlers})
            log.debug("pop_frame_stack: popped {}".format(frame.__class__.__name__))
            return frame
        log.warning("pop_frame_stack: no frame to pop")

    def _update_loop(self):
        """
        info: will update frame and call draw
        :return:
        """
        surface = TAMSurface(0, 0, " ", BLACK, BLACK)
        frame_skip = 0
        clock = timer.Timer()

        other_keys = {}
        other_surfaces = {}
        log_keys = []

        try:
            while self.is_running() and self._error is None and len(self._frame_stack) != 0:
                if self._fps_on:
                    self._ups_ticker.tick()
                # get frame and fps
                frame = self._frame_stack[-1]
                frame_time = 1 / frame.get_fps()

                # check if new handlers have come
                for receiver_name in self._receivers:
                    new_handler = self._receivers[receiver_name].get_handler()
                    if new_handler is not None:
                        if new_handler.get_full_name() not in self._other_handlers:
                            self.thread_task(new_handler.__call__)
                            log.debug("new handler accepted: {}".format(new_handler.get_full_name()))
                            self._other_handlers[new_handler.get_full_name()] = new_handler
                            other_keys[new_handler.get_full_name()] = []
                            other_surfaces[new_handler.get_full_name()] = TAMSurface(0, 0, " ", BLACK, BLACK)
                        else:
                            # new handler cant join it has the same name as another handler
                            log.warning("new handler can't join: {}".format(new_handler.get_full_name()))
                            self.thread_task(new_handler.done)

                self._remove_dead_handlers(other_keys, other_surfaces)

                # get other handler keys and update dimensions
                for other_handler in self._other_handlers:
                    other_keys[other_handler] = self._other_handlers[other_handler].pump_keys()

                keys = self.pump_keys()

                # update log
                if self._enable_loop_log:
                    if self._loop_log_key in keys:
                        self._log_on = not self._log_on

                    if self._log_on:
                        keys = list(keys)
                        while self._loop_log_key in keys:
                            keys.remove(self._loop_log_key)
                        keys = tuple(keys)
                        log_keys = keys
                        keys = []

                # update fps
                if self._enable_loop_fps and self._fps_key in keys:
                    self._fps_on = not self._fps_on
                    while self._fps_key in keys:
                        keys.remove(self._fps_key)

                # update
                frame.update(self, keys,
                             self.get_loop_data(),
                             self._other_handlers,
                             other_keys,
                             {other_handler: self._other_handlers[other_handler].get_loop_data() for other_handler in self._other_handlers})

                # check if still running and for errors
                if self.is_running() and self._error is None:
                    self._remove_dead_handlers(other_keys, other_surfaces)
                    if frame_skip == 0:
                        frame.make_surface_ready(surface, *self.get_dimensions())
                        for other_handler in self._other_handlers:
                            frame.make_surface_ready(other_surfaces[other_handler], *self._other_handlers[other_handler].get_dimensions())
                        frame.draw(surface,
                                   self.get_loop_data(),
                                   other_surfaces,
                                   {other_handler: self._other_handlers[other_handler].get_loop_data() for other_handler in self._other_handlers})
                        if self._fps_on:
                            self._fps_ticker.tick()
                            self._draw_fps(surface)
                        if self._log_on:
                            # draw log to screen
                            self._io.draw(self._update_log(log_keys))
                        else:
                            # draw to scree
                            self._io.draw(surface)

                        for other_handler in self._other_handlers:
                            self.thread_task(self._other_handlers[other_handler].get_io().draw, other_surfaces[other_handler])

                    _, run_time = clock.offset_sleep(max(frame_time - frame_skip, 0))

                    if run_time >= frame_time + frame_time/10 and frame_skip == 0:
                        frame_skip = run_time - frame_time
                    else:
                        frame_skip = 0

        except BaseException as error:
            self._error = error
        finally:
            self.done()

    def _remove_dead_handlers(self, other_keys, other_surfaces):
        """
        info: removes all dead handlers
        :param other_keys: dict
        :param other_surfaces: dict
        :return: None
        """
        # remove dead handlers
        dead_handlers = []
        for other_handler in self._other_handlers:
            if self._other_handlers[other_handler].is_running() is False:
                self.thread_task(self._other_handlers[other_handler].done)
                dead_handlers.append(other_handler)

        for dead_handler in dead_handlers:
            log.debug("dead handler removed: {}".format(dead_handler))
            del self._other_handlers[dead_handler]
            del other_keys[dead_handler]
            del other_surfaces[dead_handler]

    def thread_task(self, func, *args, **kwargs):
        self._workers.submit(self._thread_task, func, *args, **kwargs)

    @staticmethod
    def _thread_task(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            if hasattr(func, "__name__"):
                log.warning("_thread_task {} error: {}".format(func.__name__, error))
            else:
                log.warning("_thread_task error: {}".format(error))

    def _update_log(self, keys):
        """
        info: will update the log and draw the log
        :param keys: tuple
        :return: TAMSurface
        """
        width, height = self.get_dimensions()
        surface = TAMSurface(width, height, " ", GREEN, BLACK)

        if log.LOG.last_msg_id() > self._log_at:
            self._log_at = log.LOG.last_msg_id()

        if self._log_bottom:
            self._log_at = log.LOG.first_msg_id()

        for key in keys:
            if key == tam_keys.KEY_UP:
                self._log_at += -1
                self._log_bottom = False
            elif key == tam_keys.KEY_DOWN:
                self._log_at += 1
            elif key == tam_keys.KEY_LEFT:
                self._log_at = log.LOG.last_msg_id()
                self._log_bottom = False
            elif key == tam_keys.KEY_RIGHT:
                self._log_at = log.LOG.first_msg_id()
                self._log_bottom = True

        if log.LOG.last_msg_id() > self._log_at:
            self._log_at = log.LOG.last_msg_id()

        if log.LOG.first_msg_id() < self._log_at:
            self._log_at = log.LOG.first_msg_id()

        self._log_bottom = log.LOG.first_msg_id() == self._log_at
        for spot, line_number in enumerate(range(self._log_at, self._log_at + height)):
            line = log.LOG.read(line_number)
            at_x = 0
            for c in line:
                if c == "\t":
                    at_x += 4
                elif c != "\n":
                    surface.set_spot(at_x, spot, c, GREEN, BLACK)
                    at_x += 1

        return surface

    def _draw_fps(self, surface):
        """
        info: will draw fps and ups on to the top left
        :param surface: TAMSurface
        :return: surface
        """
        fps_str = "F:{}, U:{}".format(self._fps_ticker.tick_rate(), self._ups_ticker.tick_rate())
        for spot, c in enumerate(fps_str):
            surface.set_spot(spot, 0, c, GREEN, BLACK)
        return surface


class TAMFrame:
    def __init__(self,
                 fps,
                 char,
                 foreground_color,
                 background_color,
                 min_width=0,
                 max_width=1000,
                 min_height=0,
                 max_height=1000):
        """
        info: makes a TAMFrame object
        :param fps: int or float: 0.0 - inf
        :param char: str: len of 1
        :param foreground_color: int: 0 - inf
        :param background_color: int: 0 - inf
        :param min_width: int: 0 - inf
        :param max_width: int: min_width - inf
        :param min_height: int: 0 - inf
        :param max_height: int: min_height - inf
        """
        self.__fps = fps

        self.__char = char
        self.__foreground_color = foreground_color
        self.__background_color = background_color

        self.__min_width = min_width
        self.__max_width = max_width

        self.__min_height = min_height
        self.__max_height = max_height

        self.__done_called = False
        self.__frame_done_called = False

    def get_fps(self):
        """
        info: returns the frame fps
        :return: int
        """
        return self.__fps

    def get_defaults(self):
        """
        info: gets defaults
        :return: (str, int, int)
        """
        return self.__char, self.__foreground_color, self.__background_color

    def get_width_min_and_max(self):
        """
        info: returns min and max width
        :return: (int, int)
        """
        return self.__min_width, self.__max_width

    def get_height_min_and_max(self):
        """
        info: returns min and max height
        :return: (int, int)
        """
        return self.__min_height, self.__max_height

    def make_surface_ready(self, tam_surface, screen_width, screen_height):
        """
        info: will make surface ready for frame
        :param tam_surface: TAMSurface
        :param screen_width: int: 0 - inf
        :param screen_height: int: 0 - inf
        :return:
        """
        if (self.__char, self.__foreground_color, self.__background_color) != tam_surface.get_defaults():
            tam_surface.set_defaults_and_clear(self.__char, self.__foreground_color, self.__background_color)

        width = min(max(self.__min_width, screen_width), self.__max_width)
        height = min(max(self.__min_height, screen_height), self.__max_height)
        if (width, height) != tam_surface.get_dimensions():
            tam_surface.set_dimensions_and_clear(width, height)

        return tam_surface

    def update(self, tam_loop, keys, loop_data, other_handlers, other_keys, other_data):
        """
        info: will update terminal
        :param tam_loop: TAMLoop
        :param keys: list, tuple
        :param loop_data: objects
        :param other_handlers: dict
        :param other_keys: dict
        :param other_data: dict
        :return:
        """
        raise NotImplementedError()

    def draw(self, tam_surface, loop_data, other_surfaces, other_data):
        """
        info: will draw frame onto terminal
        :param tam_surface: TAMSurface
        :param loop_data: object
        :param other_surfaces: dict
        :param other_data: dict
        :return:
        """
        raise NotImplementedError()

    def _frame_done(self, tam_loop, loop_data, other_handlers, other_data):
        """
        info: called when clean up the frame and can only be called once
        :param tam_loop: TAMLoop
        :param loop_data: object
        :param other_handlers: dict
        :param other_data: dict
        :return:
        """
        if not self.__frame_done_called:
            self.__frame_done_called = True
            self.frame_done(tam_loop, loop_data, other_handlers, other_data)

    def frame_done(self, tam_loop, loop_data, other_handlers, other_data):
        """
        info: called when clean up the frame and can only be called once
        :param tam_loop: TAMLoop
        :param loop_data: dict
        :param other_handlers: dict
        :param other_data: dict
        :return:
        """
        pass

    def _done(self, tam_loop, loop_data, other_handlers, other_data):
        """
        info: called when TAMLoop is terminating and can only be called once
        :param tam_loop: TAMLoop
        :param loop_data: object
        :param other_handlers: dict
        :param other_data: dict
        :return:
        """
        if not self.__done_called:
            self.__done_called = True
            self.done(tam_loop, loop_data, other_handlers, other_data)

    def done(self, tam_loop, loop_data, other_handlers, other_data):
        """
        info: called when TAMLoop is terminating and can only be called once
        :param tam_loop: TAMLoop
        :param loop_data: dict
        :param other_handlers: dict
        :param other_data: dict
        :return:
        """
        pass
