# tamcolors libraries
from tamcolors import tam_io


"""
TAMFilm
Can move through TAMSurfaces like film
"""


class TAMFilmError(Exception):
    pass


class TAMFilm:
    def __init__(self, tam_surfaces=None, circular=False):
        """
        info: makes TAMFilm object
        :param tam_surfaces: TAMSurface
        :param circular: bool: if true will loop around frames
        """
        if tam_surfaces is None:
            tam_surfaces = []

        if isinstance(tam_surfaces, tam_io.tam_surface.TAMSurface):
            tam_surfaces = [tam_surfaces]
        else:
            tam_surfaces = list(tam_surfaces)

        self._surface_list = tam_surfaces
        self._list_at = 0
        self._circular = circular

    def __setitem__(self, spot, tam_surface):
        """
        info: sets a frame
        :param spot: int: 0 - len(self._surface_list)
        :param tam_surface: TAMSurface
        :return:
        """
        self.set(spot, tam_surface)

    def __getitem__(self, spot):
        """
        info: will get a TAMSurface
        :param spot: int: 0 - len(self._surface_list)
        :return: TAMSurface
        """
        return self.get(spot)

    def __next__(self):
        """
        info will get the next TAMSurface
        :return: TAMSurface
        """
        ret = self.slide()
        if ret is None:
            raise StopIteration()
        return ret

    def __len__(self):
        """
        info: returns the number of TAMSurface in the film
        :return: int
        """
        return len(self._surface_list)

    def set(self, spot, tam_surface):
        """
        info: sets a frame
        :param spot: int: 0 - len(self._surface_list)
        :param tam_surface: TAMSurface
        :return:
        """
        try:
            if abs(spot) != spot:
                raise TAMFilmError()
            self._surface_list[spot] = tam_surface
        except TypeError as error:
            raise TAMFilmError(error)
        except IndexError as error:
            raise TAMFilmError(error)

    def get(self, spot):
        """
        info will get a TAMSurface
        :param spot: int: 0 - len(self._surface_list)
        :return: TAMSurface
        """
        try:
            return self._surface_list[spot]
        except TypeError as error:
            raise TAMFilmError(error)
        except IndexError as error:
            raise TAMFilmError(error)

    def slide(self):
        """
        info will get the next TAMSurface
        :return: TAMSurface or None
        """
        if len(self._surface_list) == 0:
            return None
        elif self.done():
            if not self._circular:
                return self._surface_list[-1]
            self._list_at = 0

        ret = self._surface_list[self._list_at]
        self._list_at += 1
        return ret

    def peak(self):
        """
        info: gets the current frame
        :return: TAMSurface or None
        """
        if len(self._surface_list) == 0:
            return None
        elif self.done():
            if not self._circular:
                return self._surface_list[-1]
            return self._surface_list[0]

        return self._surface_list[self._list_at]

    def append(self, tam_surface):
        """
        info
        :param tam_surface:
        :return:
        """
        self._surface_list.append(tam_surface)

    def pop(self):
        """
        info: will pop the last TAMSurface
        :return: TAMSurface or None
        """
        if len(self._surface_list) != 0:
            return self._surface_list.pop()

    def get_circular(self):
        """
        info: gets the circular value
        :return: bool
        """
        return self._circular

    def set_circular(self, circular):
        """
        info: can set circular value
        :param circular: True
        :return:
        """
        self._circular = circular

    def done(self):
        """
        info: returns true if film is done
        :return: bool
        """
        return len(self._surface_list) <= self._list_at
