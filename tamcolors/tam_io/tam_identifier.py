# built in library
import platform

# tamcolors libraries
from tamcolors.tam_io import any_drivers
from tamcolors.tam_io import win_drivers
from tamcolors.tam_io import uni_drivers
from tamcolors.tam_io import ansi_true_color_drivers
from tamcolors.tam_io import ansi_256_drivers


"""
TAMIdentifier
finds the best tam drivers for the current environment
"""


class TAMIdentifier:
    def __init__(self,
                 name,
                 *drivers):
        """
        info: Makes a TAMIdentifier Object
        :param name:
        :param drivers:
        """

        self._name = name
        self._drivers = list(drivers)
        self._system = platform.system()
        self._environment_io = self._build_io()

    def __str__(self):
        output = ""
        info = self.get_info_dict()
        for key in info:
            data = info[key]
            if isinstance(data, (list, tuple)):
                data = "\n\t".join(data)
            output += "{}:\n\t{}\n".format(key, data)

        if len(output) != 0:
            output = output[:-1]
        return output

    def get_name(self):
        """
        info: Get the general name of the drivers
        :return: str
        """
        return self._name

    def get_all_drivers(self):
        """
        info: Get a list of all the tam drivers being used
        :return: list
        """
        return self._drivers.copy()

    def get_system(self):
        """
        info: Get the system
        :return: str
        """
        return self._system

    def stable(self):
        """
        info: Sees if this IO is able to execute
        :return: bool
        """
        if self._environment_io is None:
            return False
        return self._environment_io.able_to_execute()

    def get_info_dict(self):
        """
        info: Get raw info about this identifier
        :return: dict
        """
        return {"name": self.get_name(),
                "drivers": [driver.__name__ for driver in self.get_all_drivers()],
                "system": self.get_system(),
                "stable": self.stable()}

    @classmethod
    def identify(cls):
        """
        info: Will find the best drivers for current environment
        :return: TAMIdentifier
        """
        if platform.system().lower() == "windows":
            io_identifier = cls("WIN_DRIVERS",
                                win_drivers.WINFullColorDriver,
                                win_drivers.WINKeyDriver,
                                win_drivers.WINUtilitiesDriver)
            if io_identifier.stable():
                return io_identifier

        if platform.system().lower() == "linux":
            io_identifier = cls("UNI_TRUE_COLOR_DRIVERS",
                                uni_drivers.UNIKeyDriver,
                                uni_drivers.UNIUtilitiesDriver,
                                ansi_true_color_drivers.ANSITrueFullColorDriver)
            if io_identifier.stable():
                return io_identifier

        if platform.system().lower() == "darwin":
            io_identifier = cls("UNI_256_DRIVERS",
                                uni_drivers.UNIKeyDriver,
                                uni_drivers.UNIUtilitiesDriver,
                                ansi_256_drivers.ANSI256ColorDriver,
                                ansi_256_drivers.ANSI256ChangerDriver)
            if io_identifier.stable():
                return io_identifier

        return ANY_IO_IDENTIFIER

    def _build_io(self):
        """
        info: Will build an IO with selected drivers
        :return: IO
        """
        class EnvironmentIO(*self.get_all_drivers()):
            pass

        return EnvironmentIO(identifier=self)

    def get_io(self):
        """
        info: Gets the IO that the selected drivers made
        :return: IO
        """
        return self._environment_io


ANY_IO_IDENTIFIER = TAMIdentifier("ANY_DRIVERS",
                                  any_drivers.ANYKeyDriver,
                                  any_drivers.ANYColorDriver,
                                  any_drivers.ANYColorChangerDriver,
                                  any_drivers.ANYUtilitiesDriver)

ANY_IO = ANY_IO_IDENTIFIER.get_io()
IO = TAMIdentifier.identify().get_io()
