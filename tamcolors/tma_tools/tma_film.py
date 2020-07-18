# Charles McMarrow libraries
from tamcolors import checks
from tamcolors import tma

# Charles McMarrow

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

        # checks
        checks.checks.in_instances_check(tma_buffers, (tma.tma_buffer.TMABuffer, list, tuple), TMAFilmError)

        if isinstance(tma_buffers, tma.tma_buffer.TMABuffer):
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
        # checks
        checks.checks.instance_check(spot, int, TMAFilmError)
        checks.checks.instance_check(tma_buffer, tma.tma_buffer.TMABuffer, TMAFilmError)

        self.set(spot, tma_buffer)

    def __getitem__(self, spot):
        """
        info: will get a TMABuffer
        :param spot: int: 0 - len(self.__buffer_list)
        :return: TMABuffer
        """
        # checks
        checks.checks.instance_check(spot, int, TMAFilmError)

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
        # checks
        checks.checks.range_check(spot, 0, len(self.__buffer_list), TMAFilmError)
        checks.checks.instance_check(tma_buffer, tma.tma_buffer.TMABuffer, TMAFilmError)
        self.__buffer_list[spot] = tma_buffer

    def get(self, spot):
        """
        info will get a TMABuffer
        :param spot: int: 0 - len(self.__buffer_list)
        :return: TMABuffer
        """
        # checks
        checks.checks.range_check(spot, 0, len(self.__buffer_list), TMAFilmError)
        return self.__buffer_list[spot]

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
        # checks
        checks.checks.instance_check(tma_buffer, tma.tma_buffer.TMABuffer, TMAFilmError)
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
        # checks
        checks.checks.instance_check(circular, bool, TMAFilmError)

        self.__circular = circular

    def done(self):
        """
        info: returns true if film is done
        :return: bool
        """
        return len(self.__buffer_list) <= self.__list_at
