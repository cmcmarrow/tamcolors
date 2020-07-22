# tamcolors libraries
from tamcolors import tam_io


"""
TAMFilm
Can move through TAMBuffers like film
"""


class TAMFilmError(Exception):
    pass


class TAMFilm:
    def __init__(self, tam_buffers=None, circular=False):
        """
        info: makes TAMFilm object
        :param tam_buffers: TAMBuffer
        :param circular: bool: if true will loop around frames
        """
        if tam_buffers is None:
            tam_buffers = []

        if isinstance(tam_buffers, tam_io.tam_buffer.TAMBuffer):
            tam_buffers = [tam_buffers]
        else:
            tam_buffers = list(tam_buffers)

        self.__buffer_list = tam_buffers
        self.__list_at = 0
        self.__circular = circular

    def __setitem__(self, spot, tam_buffer):
        """
        info: sets a frame
        :param spot: int: 0 - len(self.__buffer_list)
        :param tam_buffer: TAMBuffer
        :return:
        """
        self.set(spot, tam_buffer)

    def __getitem__(self, spot):
        """
        info: will get a TAMBuffer
        :param spot: int: 0 - len(self.__buffer_list)
        :return: TAMBuffer
        """
        return self.get(spot)

    def __next__(self):
        """
        info will get the next TAMBuffer
        :return: TAMBuffer
        """
        ret = self.slide()
        if ret is None:
            raise StopIteration()
        return ret

    def __len__(self):
        """
        info: returns the number of TAMBuffer in the film
        :return: int
        """
        return len(self.__buffer_list)

    def set(self, spot, tam_buffer):
        """
        info: sets a frame
        :param spot: int: 0 - len(self.__buffer_list)
        :param tam_buffer: TAMBuffer
        :return:
        """
        try:
            if abs(spot) != spot:
                raise TAMFilmError()
            self.__buffer_list[spot] = tam_buffer
        except TypeError as error:
            raise TAMFilmError(error)
        except IndexError as error:
            raise TAMFilmError(error)

    def get(self, spot):
        """
        info will get a TAMBuffer
        :param spot: int: 0 - len(self.__buffer_list)
        :return: TAMBuffer
        """
        try:
            return self.__buffer_list[spot]
        except TypeError as error:
            raise TAMFilmError(error)
        except IndexError as error:
            raise TAMFilmError(error)

    def slide(self):
        """
        info will get the next TAMBuffer
        :return: TAMBuffer or None
        """
        if len(self.__buffer_list) == 0:
            return None
        elif self.done():
            if not self.__circular:
                return self.__buffer_list[-1]
            self.__list_at = 0

        ret = self.__buffer_list[self.__list_at]
        self.__list_at += 1
        return ret

    def peak(self):
        """
        info: gets the current frame
        :return: TAMBuffer or None
        """
        if len(self.__buffer_list) == 0:
            return None
        elif self.done():
            if not self.__circular:
                return self.__buffer_list[-1]
            return self.__buffer_list[0]

        return self.__buffer_list[self.__list_at]

    def append(self, tam_buffer):
        """
        info
        :param tam_buffer:
        :return:
        """
        self.__buffer_list.append(tam_buffer)

    def pop(self):
        """
        info: will pop the last TAMBuffer
        :return: TAMBuffer or None
        """
        if len(self.__buffer_list) != 0:
            return self.__buffer_list.pop()

    def get_circular(self):
        """
        info: gets the circular value
        :return: bool
        """
        return self.__circular

    def set_circular(self, circular):
        """
        info: can set circular value
        :param circular: True
        :return:
        """
        self.__circular = circular

    def done(self):
        """
        info: returns true if film is done
        :return: bool
        """
        return len(self.__buffer_list) <= self.__list_at
