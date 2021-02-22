
from tamcolors.tam_io import tam_identifier
from tamcolors.utils import id_manager

IO = tam_identifier.IO


class Sound:
    _manager = id_manager.IDManager()

    def __init__(self, file):
        self._id = self.__class__._manager.get_id()
        self._file = file
        IO.open_sound(self._file, self._id)
        self._open = True

    def __str__(self):
        return str(self._file)

    def __repr__(self):
        return "(Sound: {})".format(self._id)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def is_open(self):
        return self._open

    def close(self):
        if hasattr(self, "_open") and self._open:
            self._open = False
            IO.close_sound(self._id)
            self.__class__._manager.free_id(self._id)

    def play(self, reset_sound=True):
        """
        info: will play sound
        :param reset_sound: bool
        :return: None
        """
        IO.play_sound(self._id, reset_sound)

    def pause(self):
        """
        info: will pause sound
        :return: None
        """
        IO.pause_sound(self._id)

    def get_length(self):
        """
        info: will get sound length
        :return: int
        """
        return IO.get_sound_length(self._id)

    def is_playing(self):
        """
        info: will check if sound is playing
        :return: bool
        """
        return IO.is_sound_playing(self._id)

    def get_position(self):
        """
        info: will get the time spot of the song
        :return: int
        """
        return IO.get_sound_position(self._id)

    def set_position(self, spot):
        """
        info: will set the spot of the sound
        :param spot: int
        :return: None
        """
        IO.set_sound_position(self._id, spot)

    def rest(self):
        """
        info: will reset sound
        :return: None
        """
        IO.reset_sound(self._id)
