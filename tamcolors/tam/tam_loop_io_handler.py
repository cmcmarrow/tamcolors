from concurrent.futures import ThreadPoolExecutor


class TAMLoopIOHandler:
    def __init__(self, io, name, threading=True):
        """
        info: Makes a TAMLoopIOHandler object
        :param io: IO
        :param name: str
        :param threading: bool
        """
        self._io = io
        self._name = name
        self._works = None
        if threading:
            self._works = ThreadPoolExecutor(max_workers=5)

    def start(self, timeout):   # TODO write
        pass

    def done(self):   # TODO write
        pass
