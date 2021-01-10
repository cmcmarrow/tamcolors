

class TAMLoopReceiver:
    def __init__(self, name):
        self._name = name
        self._running = True
        self._receiver_settings = None

    def get_name(self):
        """
        info: Will get the receiver name
        :return: str
        """
        return self._name

    def get_handler(self):
        """
        info: Will get an io if available
        :return: TAMLoopIOHandler or None
        """
        raise NotImplementedError()

    def done(self):
        """
        info: Will stop the receiver
        :return: None
        """
        self._running = False

    def get_running(self):
        """
        info: Checks if receiver is running
        :return: bool
        """
        return self._running

    def set_receiver_settings(self, settings):
        """
        info: will set the receiver io settings
        :param settings: dict
        :return: None
        """
        self._receiver_settings = settings

    def get_receiver_settings(self):
        """
        info: will get the receiver io settings
        :return: dict or None
        """
        return self._receiver_settings
