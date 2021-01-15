from tamcolors.tam.tam_loop_io_handler import TAMLoopIOHandler


class TAMLoopIOTCPHandler(TAMLoopIOHandler):
    def done(self, reset_colors_to_console_defaults=True):
        """
        info: will stop tam loop
        :param: reset_colors_to_console_defaults: bool
        :return: None
        """
        if self.is_running():
            super().done(reset_colors_to_console_defaults)
        self._io.close()

    def is_running(self):
        if self._io.is_open():
            return super(TAMLoopIOTCPHandler, self).is_running()
        return False
