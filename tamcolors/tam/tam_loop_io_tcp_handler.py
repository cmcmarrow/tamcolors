from tamcolors.tam.tam_loop_io_handler import TAMLoopIOHandler


class TAMLoopIOTCPHandler(TAMLoopIOHandler):
    def done(self):
        """
        info: will stop tam loop
        :return: None
        """
        if self.is_running():
            super().done()
        self._io.close()

    def is_running(self):
        if self._io.is_open():
            return super(TAMLoopIOTCPHandler, self).is_running()
        return False
