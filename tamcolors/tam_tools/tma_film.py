# tamcolors libraries
from tamcolors import tam


"""
TMAFilm
Can move through TMABuffers like film
"""


class TMAFilmError(Exception):
    pass


class TMAFilm:
    def __init__(self, tma_buffers=None, circular=False):
        """
        info: makes TMAFilm object
        :param tma_buffers: TMABuffer
        :param circular: bool: if true will loop around frames
        """
        if tma_buffers is None:
            tma_buffers = []

        if isinstance(tma_buffers, tam.tma_buffer.TMABuffer):
            tma_buffers = [tma_buffers]
        else:
            tma_buffers = list(tma_buffers)

        self.__buffer_list = tma_buffers
        self.__list_at = 0
        self.__circular = circular

    def __setitem__(self, spot, tma_buffer):
        """
        info: sets a frame
        :param spot: int: 0 - len(self.__buffer_list)
        :param tma_buffer: TMABuffer
        :return:
        """
        self.set(spot, tma_buffer)

    def __getitem__(self, spot):
        """
        info: will get a TMABuffer
        :param spot: int: 0 - len(self.__buffer_list)
        :return: TMABuffer
        """
        return self.get(spot)

    def __next__(self):
        """
        info will get the next TMABuffer
        :return: TMABuffer
        """
        ret = self.slide()
        if ret is None:
            raise StopIteration()
        return ret

    def __len__(self):
        """
        info: returns the number of TMABuffer in the film
        :return: int
        """
        return len(self.__buffer_list)

    def set(self, spot, tma_buffer):
        """
        info: sets a frame
        :param spot: int: 0 - len(self.__buffer_list)
        :param tma_buffer: TMABuffer
        :return:
        """
        try:
            if abs(spot) != spot:
                raise TMAFilmError()
            self.__buffer_list[spot] = tma_buffer
        except TypeError as error:
            raise TMAFilmError(error)
        except IndexError as error:
            raise TMAFilmError(error)

    def get(self, spot):
        """
        info will get a TMABuffer
        :param spot: int: 0 - len(self.__buffer_list)
        :return: TMABuffer
        """
        try:
            return self.__buffer_list[spot]
        except TypeError as error:
            raise TMAFilmError(error)
        except IndexError as error:
            raise TMAFilmError(error)

    def slide(self):
        """
        info will get the next TMABuffer
        :return: TMABuffer or None
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
        :return: TMABuffer or None
        """
        if len(self.__buffer_list) == 0:
            return None
        elif self.done():
            if not self.__circular:
                return self.__buffer_list[-1]
            return self.__buffer_list[0]

        return self.__buffer_list[self.__list_at]

    def append(self, tma_buffer):
        """
        info
        :param tma_buffer:
        :return:
        """
        self.__buffer_list.append(tma_buffer)

    def pop(self):
        """
        info: will pop the last TMABuffer
        :return: TMABuffer or None
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
